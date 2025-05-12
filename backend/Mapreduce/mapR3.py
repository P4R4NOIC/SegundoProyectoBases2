#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep
import requests

class ReferenceCountActive (MRJob):

  def steps(self):
    return [MRStep(mapper = self.mapper, reducer = self.reducer)]

  def activeChecker(self, url):
    try:
      response = requests.get(url)
      if response.status_code in [200, 401, 403]:
        return True
      else:
        return False
    except requests.exceptions.RequestException as e:
      False

  def mapper2(self, data):
    page = ""
    counter = 0
    for pageInfo in data.values():
      if "references" in pageInfo["referencias"]:
        for ref in pageInfo["referencias"]["references"]:
          if page != pageInfo["url"]:
            page = pageInfo["url"]
            counter = 0
          direccion = ref["url"]
          if (direccion not in ["-", ""]):
            counter += 1
            if self.activeChecker(direccion):
              yield "'"+pageInfo["url"]+"',"+"'active'", 1
              yield "'"+pageInfo["url"]+"','"+direccion+"','"+str(counter)+"','active'", 1
            else:
              yield "'"+pageInfo["url"]+"',"+"'inActive'", 1
              yield "'"+pageInfo["url"]+"','"+direccion+"','"+str(counter)+"','inActive'", 1

  def mapper(self, _, line):
    import json
    data = json.loads(line)
    for page in data:
      yield from self.mapper2(page)

  def reducer(self, key, values):
    count = 0
    for i in values:
      count += i
    yield (key+','+"'"+str(count)+"'"), None

if __name__ == '__main__':
  ReferenceCountActive.run()
