#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep
#from nltk.stem import PorterStemmer

class DistinctWords (MRJob):
  
  page = ""
  title = ""
  subtitle = ""

  def steps(self):
    return [MRStep(mapper = self.mapper, combiner = self.combiner, reducer = self.reducer)]
  

  def mapper2(self, data):
    if isinstance(data, dict):
      if "url" in data:
        self.page = ""
        self.title = ""
        self.subtitle = ""
        self.page = "'"+data["url"]+"'"+",'"+data["mainTitle"]["string"]+"'"
      for key, value in data.items():
          if key not in ["url", "uses", "tag", "string", "references"]:
            yield from self.mapper2(value)
    elif isinstance(data, list):
      for result in data:
        if isinstance(result, dict):
          if "titulo" in result:
            if isinstance(result["titulo"], dict):
              self.title = ""
              self.subtitle = ""
              self.title = "'"+result["titulo"]["string"]+"'"
          if "subtitulo" in result:
            if isinstance(result["subtitulo"], dict):
              self.subtitle = ""
              self.subtitle = "'"+result["subtitulo"]["string"]+"'"
          for k, v in result.items():
            if k not in ["url", "tag", "string"]:
              yield from self.mapper2(v)
    else:
      if data not in ["-", "", " "] and self.page not in ["-", "", " "]: 
        yield "'pagina',"+self.page+'::'+data.lower(), 1
        if self.title not in ["-", "", " "]:
          yield self.page.split(',')[0]+'::'+"'titulo',"+self.title+'::'+data.lower(), 1
        if self.subtitle not in ["-", "", " "]:
          yield self.page.split(',')[0]+'::'+"'subtitulo',"+self.subtitle+'::'+data.lower(), 1
    
  def mapper(self, _, line):
    import json
    data = json.loads(line)
    yield from self.mapper2(data)

  def combiner(self, key, values):
    keys = key.split('::')
    if len(keys) == 3: 
      if keys[1] != "" and keys[1] != "'titulo'" and keys[1] != "'subtitulo'":
        yield keys[0]+','+keys[1], 1
    else:
      yield keys[0], 1

  def reducer(self, key, values):
    count = 0
    for i in values:
      count += i
    yield (key+','+"'"+str(count)+"'"), None

if __name__ == '__main__':
  DistinctWords.run()
