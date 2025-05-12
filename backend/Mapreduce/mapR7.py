#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class WordInPages (MRJob):

  page = ""

  def steps(self):
    return [MRStep(mapper = self.mapper, combiner = self.combiner, reducer = self.reducer)]
  

  def mapper2(self, data):
    if isinstance(data, dict):
      if "url" in data:
        self.page = ""
        self.page = "'"+data["url"]+"'"
      for key, value in data.items():
        if key not in ["url", "uses", "tag", "string", "references"]:
          yield from self.mapper2(value)
    elif isinstance(data, list):
      for result in data:
        if isinstance(result, dict):
          for k, v in result.items():
            if k not in ["url", "tag", "string"]:
              yield from self.mapper2(v)
        else:
          yield self.page+"::'"+result.lower()+"'", 1
    else:
      yield self.page+"::'"+data.lower()+"'", 1
    
  def mapper(self, _, line):
    import json
    data = json.loads(line)
    yield from self.mapper2(data)

  def combiner(self, key, values):
    keys = key.split('::')
    if keys[1] not in ["", "''", "'-'","' '"]:
      yield keys[1]+","+keys[0], sum(values)

  def reducer(self, key, values):
    count = 0
    for i in values:
      count += i
    yield (key+','+"'"+str(count)+"'"), None

if __name__ == '__main__':
  WordInPages.run()
