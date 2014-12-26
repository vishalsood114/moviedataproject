import os
import io
from bs4 import BeautifulSoup
import requests
from sys import argv
from os.path import exists

script, to_file = argv

if exists(to_file):
    if os.stat(to_file).st_size > 0:
        open(to_file, 'w').close()
else:
    print "Enter a file that exists to write data"
    sys.exit(0)

out_file = io.open(to_file, 'w', encoding='utf8')
BASE_URL = "http://5000best.com/movies/"
for counter in range (1, 51):
    URL = BASE_URL + str(counter) + "/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text)
    for links in soup.find_all('a'):
        #print links.get('href')
        out_file.write(links.get('href') + "\n")

out_file.close()
