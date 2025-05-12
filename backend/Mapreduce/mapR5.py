#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class AltDiferentImages (MRJob):

  def steps(self):
    return [MRStep(mapper = self.mapper, combiner = self.combiner, reducer = self.reducer)]
  
  def mapper2(self, data):
    for pageInfo in data.values():
      for img in pageInfo["images"]:
        if img["text"] != "-":
          yield "'"+pageInfo["url"]+"','pagina'", 1
          for jsonWord in img["text"]:
            if isinstance(jsonWord, dict):
              for word in jsonWord.values():
                yield "'"+pageInfo["url"]+"'::"+word.lower(), 1 

  def mapper(self, _, line):
    import json
    data = json.loads(line)
    for page in data:
      yield from self.mapper2(page)

  def combiner(self, key, values):
    keys = key.split('::')
    if len(keys) == 2:

      yield keys[0], 1
    else:
      yield keys[0], sum(values)

  def reducer(self, key, values):
    count = 0
    for i in values:
      count += i
    yield (key+','+"'"+str(count)+"'"), None

if __name__ == '__main__':
  AltDiferentImages.run()
