#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class WordInTags (MRJob):
  
  tag = ""

  def steps(self):
    return [MRStep(mapper = self.mapper, combiner = self.combiner, reducer = self.reducer)]
  
  def mapperTag(self, data):
    if isinstance(data, dict):
      if "tag" in data:
        self.tagT = ""
        self.tagT = "'"+data["tag"]+"'"
        yield self.tagT, 1
      for key, value in data.items():
        if key not in ["url", "uses", "tag", "references", "string"]:
          yield from self.mapperTag(value)
    elif isinstance(data, list):
      for result in data:
        if isinstance(result, dict):
          if "tag" in result:
            self.tagT = ""
            self.tagT = "'"+result["tag"]+"'"
            yield self.tagT, 1
          for k, v in result.items():
            if k not in ["url", "tag", "string"]:
              yield from self.mapperTag(v)
    else:
      pass

  def mapper2(self, data):
    if isinstance(data, dict):
      if "tag" in data:
        self.tag = ""
        self.tag = "'"+data["tag"]+"'"
        yield self.tag+"::'tag'", 1
      for key, value in data.items():
        if key not in ["url", "uses", "tag", "references", "string"]:
          yield from self.mapper2(value)
    elif isinstance(data, list):
      for result in data:
        if isinstance(result, dict):
          if "tag" in result:
            self.tag = ""
            self.tag = "'"+result["tag"]+"'"
            yield self.tag+"::'tag'", 1
          for k, v in result.items():
            if k not in ["url", "tag", "string"]:
              yield from self.mapper2(v)
    else:
      #yield self.tag+"::"+data.lower(), 1
      if data not in ["'-'", "''"] :
        yield self.tag+"::'"+data.lower()+"'", 1
    
  def mapper(self, _, line):
    counterTag = {}
    import json
    for tk, tv in self.mapperTag(json.loads(line)):
      if tk not in counterTag.keys():
        counterTag[tk] = 0
      counterTag[tk] += tv
    data = json.loads(line)
    for k, v in self.mapper2(data):
      keys = k.split("::")
      yield k, round((v/counterTag[keys[0]])*100, 4)

  def combiner(self, key, values):
    keys = key.split('::')
    if keys[1] not in ["''", "'-'", "' '"]:
      yield keys[1]+","+keys[0], sum(values)

  def reducer(self, key, values):
    count = 0
    for i in values:
      count += i
    yield (key+','+"'"+str(count)+"'"), None

if __name__ == '__main__':
  WordInTags.run()
