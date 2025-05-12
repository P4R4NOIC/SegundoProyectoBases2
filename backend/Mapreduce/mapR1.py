#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class TitlesPage (MRJob):

  def steps(self):
    return [MRStep(mapper = self.mapper, reducer = self.reducer)]
  
  def mapper2(self, content):
    for page in content:
      for titulo in range(len(page["Pagina"]["titulos"])):
        yield "'"+page["Pagina"]["url"]+"','"+page["Pagina"]["mainTitle"]["string"]+"'", 1
  def mapper(self, _, line):
    import json
    data = json.loads(line)
    yield from self.mapper2(data)
    
  def reducer(self, key, values):
    count = 0
    for i in values:
      count += i
    yield (key+','+"'"+str(count)+"'"), None


if __name__ == '__main__':
  TitlesPage.run()
