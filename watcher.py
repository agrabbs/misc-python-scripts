# State-less list tracker 
from urllib.request import Request, urlopen
from time import sleep
import re

class Watcher:
  # Config
  URL = ''
  REGEX = 'detLink.*?>(.*?)<'
  USER_AGENT = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
  WAIT = 1800

  current_list = list()
  temp_list = list()

  def __init__(self):
    print('Spinning up!')
    self.main()

  def compare_lists(self):
    # List everything that has fell off the list:
    for x in list(set(self.current_list) - set(self.temp_list)):
      print('-- {}'.format(x))

    # Look for changes in the list
    for item in self.temp_list:
      if item in self.current_list:
        # If the position has not changed:
        if self.temp_list.index(item) == self.current_list.index(item):
          pass
        # If the position has changed:
        else:
          diff = self.current_list.index(item) - self.temp_list.index(item)
          if self.temp_list.index(item) < diff:
            print('+{} {}'.format(abs(diff),item))
          else:
            print('-{} {}'.format(abs(diff), item))
      else:
        print('++ {} (pos: {})'.format(item,self.temp_list.index(item)+1))

  def update_list(self):
    req = Request(self.URL, None, self.USER_AGENT)
    content = urlopen(req).read().decode('utf-8')
    self.temp_list = re.findall(self.REGEX, content)
    if len(self.temp_list) > 0:
      pass
      #print(self.temp_list)
    else:
      print('Error: Unable to match defined regex in url.')
    self.compare_lists()
    self.current_list = self.temp_list

  def main(self):
    while True:
      self.update_list()
      sleep(self.WAIT)

if __name__ == "__main__":
  watcher = Watcher()
