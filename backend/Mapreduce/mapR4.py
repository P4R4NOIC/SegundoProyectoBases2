#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class ReferenceUsed (MRJob):

  def steps(self):
    return [MRStep(mapper = self.mapper, reducer = self.reducer)]
    
  def mapper2(self, data):
    for page in data:
      for pageInfo in page.values():
        if "uses" in pageInfo["referencias"]:
          for use in pageInfo["referencias"]["uses"]:
            yield "'"+pageInfo["url"]+"','"+use["id"]+"'", 1

  def mapper(self, _, line):
    import json
    data = json.loads(line)
    pageActual = ""
    cite = {}
    counter = 0
    for k, v in self.mapper2(data):
      key = k.split(',')
      if key[0] != pageActual:
        pageActual = key[0]
        cite = {}
        counter = 0
      if key[1] not in cite:
        counter += 1
        cite[key[1]] = counter
      yield k+",'"+str(cite[key[1]])+"'", v 

  def reducer(self, key, values):
    count = 0
    for i in values:
      count += i
    yield (key+','+"'"+str(count)+"'"), None

if __name__ == '__main__':
  ReferenceUsed.run()
