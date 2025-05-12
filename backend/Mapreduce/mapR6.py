#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class CommonWords (MRJob):
  
  page = ""
  title = ""
  subtitle = ""

  def steps(self):
    return [MRStep(mapper = self.mapper, combiner = self.combiner, reducer = self.reducer), MRStep(reducer = self.reducerTop10)]
  

  def mapper2(self, data):
    if isinstance(data, dict):
      if "url" in data:
        self.page = ""
        self.title = ""
        self.subtitle = ""
        self.page = "'"+data["url"]+"','"+data["mainTitle"]["string"]+"'"
      for key, value in data.items():
          if key not in ["url", "uses", "tag", "string", "references"]:
            yield from self.mapper2(value)
    elif isinstance(data, list):
      for result in data:
        if isinstance(result, dict):
          if "titulo" in result:
            if isinstance(result["titulo"], dict):
              for titleWord in result["titulo"]["text"]:
                if isinstance(titleWord, dict):
                  for kt, vt in titleWord.items():
                    yield "'titulo',"+self.page+"::'"+vt.lower()+"'", 1
          for k, v in result.items():
            if k not in ["url", "tag", "string"]:
              yield from self.mapper2(v)
    else:
      if data not in ["-", "", " "] and self.page not in ["-", "", " "]: 
        yield "'pagina',"+self.page+"::'"+data.lower()+"'", 1
    
  def mapper(self, _, line):
    import json
    data = json.loads(line)
    yield from self.mapper2(data)

  def combiner(self, key, values):
    keys = key.split('::') 
    if keys[1] != "" :
        yield keys[0]+','+keys[1], sum(values)
    else:
      yield keys[0], sum(values) 

  def reducer(self, key, values):
    yield None, (key+',', sum(values))

  def reducerTop10(self, _, pair):
    topWords = []
    parameterTop = ("", 0)
    sortedPair = sorted(pair, key=lambda x: (x[0].split(',')[1], x[1]), reverse = True)
    for pair in sortedPair:
      isTitle = pair[0].split(',')
      if isTitle[3] not in ["'de'", "'la'", "'y'","'a'","'lo'","'en'", "'del'", "'el'", "'se'", "'su'", "'que'", "'un'", "'una'", "'cual'", "'por'"]:
        if isTitle[1] != parameterTop[0]:
          parameterTop = (isTitle[1], pair[1])
          topWords = []
        if pair[1] >= parameterTop[1]/2 or isTitle[0] == "'titulo'":
          if isTitle[0] != "'titulo'":
            topWords.append(isTitle[3])
            yield pair[0]+"'"+str(pair[1])+"'", None
          elif isTitle[3] in topWords:
            yield pair[0]+"'"+str(pair[1])+"'", None


if __name__ == '__main__':
  CommonWords.run()
