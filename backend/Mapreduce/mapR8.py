#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep
from unidecode import unidecode

class PercentWords (MRJob):
  page = ""
  pageT = ""
  
  #total_words = 0
  def steps(self):
    return [MRStep(mapper = self.mapper, combiner = self.combiner, reducer = self.reducer)]

  def mapperTotal(self, data):
    if isinstance(data, dict):
      if "url" in data:
        self.pageT = ""
        self.pageT = "'"+data["url"]+"'"
      for key, value in data.items():
        if key not in ["url", "uses", "tag", "string", "mainTitle", "references"]:
          yield from self.mapperTotal(value)
    elif isinstance(data, list):
      for result in data:
        if isinstance(result, dict):
          for k, v in result.items():
            if k not in ["url", "tag", "string"]:
              yield from self.mapperTotal(v)
    else:
      if data != "-":
        yield self.pageT, 1

  def mapper2(self, data):
    import json
    if isinstance(data, dict):
      if "url" in data:
        self.page = ""
        self.page = "'"+data["url"]+"'"
      for key, value in data.items():
        if key not in ["url", "uses", "tag", "string", "mainTitle", "references"]:
          yield from self.mapper2(value)
    elif isinstance(data, list):
      for result in data:
        if isinstance(result, dict):
          for k, v in result.items():
            if k not in ["url", "tag", "string"]:
              yield from self.mapper2(v)
    else:
      if data != "-":
        yield self.page+"::'"+data.lower()+"'", 1
    
  def mapper(self, _, line):
    counter = {}
    import json
    for p, w in self.mapperTotal(json.loads(line)):
      if p not in counter.keys():
        counter[p] = 0
      counter[p] += w
    for k, v in self.mapper2(json.loads(line)):
      keys = k.split("::")
      yield k, round((v/counter[keys[0]])*100, 2)
      #yield k, v

  def combiner(self, key, values):
    keys = key.split('::')
    yield keys[0]+","+keys[1], sum(values)

  def reducer(self, key, values):
    count = 0
    for i in values:
      count += i
    yield (key+','+"'"+str(count)+"'"), None



if __name__ == '__main__':
  PercentWords.run()
