# State-less top 100 tracker
# Eventually for Discord bot. 
from urllib.request import Request, urlopen
from time import sleep
import re

class c:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class Watcher:
  URL = ''
  REGEX = 'detLink.*?>(.*?)<'
  USER_AGENT = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
  WAIT = 600

  current_list = list()
  temp_list = list()

  def __init__(self):
    print('{}Spinning up!{}'.format(c.OKBLUE,c.ENDC))
    self.main()

  def compare_lists(self):
    # List everything that has fell off the list:
    for x in list(set(self.current_list) - set(self.temp_list)):
      print('{}{}--\t{}{}'.format(c.FAIL, c.BOLD, x, c.ENDC))

    # Look for changes in the list
    for item in self.temp_list:
      if item in self.current_list:
        # If the position has not changed:
        if self.temp_list.index(item) == self.current_list.index(item):
          pass
        # If the position has changed:
        else:
          diff = (self.current_list.index(item)+1) - (self.temp_list.index(item)+1)
          if diff > 0:
          #if self.temp_list.index(item) < self.current_list.index(item):
            print('{}\u2191{}{}[{}{}{}]\t{}'.format(c.OKGREEN,abs(diff),c.ENDC, c.WARNING, self.temp_list.index(item)+1, c.ENDC, item))
          else:
            print('{}\u2193{}{}[{}{}{}]\t{}'.format(c.FAIL, abs(diff), c.ENDC, c.WARNING, self.temp_list.index(item)+1, c.ENDC, item))
          diff = None
      else:
        print('{}{}++{}[{}{}{}]\t{})'.format(c.OKBLUE,c.BOLD, c.ENDC, c.WARNING, self.temp_list.index(item)+1, c.ENDC, item))

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
