import os
import io
import json
from bs4 import BeautifulSoup
import requests
from sys import argv
from os.path import exists

script, servicefilter, to_file, json_file = argv

if exists(to_file):
    if os.stat(to_file).st_size > 0:
        open(to_file, 'w').close()
else:
    print "Enter a file that exists to write data"
    sys.exit(0)

out_file = io.open(to_file, 'w', encoding='utf8')
json_file = open(json_file,'w')
#def get_moviename_imglink(soup):

START_URL= "http://www.yidio.com/ajax_base_dir_movies_new.php?filter="
START_LI_URL="&genres=&rating=&start_limit="
END_LI_URL = "&end_limit="
LAST_URL = "&letter=All"

start_limit = str(1)
end_limit = str(24)

BASE_URL = START_URL + servicefilter + START_LI_URL+ start_limit + END_LI_URL + end_limit + LAST_URL
page = requests.get(BASE_URL)
movie_dict_list =[]
counter = 0
while len(page.text) != 0:
    soup = BeautifulSoup(page.text)
    for atags in soup.find_all('a'):
        movie_dict ={}
        movie = list(atags.descendants)
        movieimg = movie[3].get('src')
        movie_dict["imgLink"] = movieimg
        moviename = movie[7]
        movie_dict["movieName"] = moviename
        print moviename + "|" + movieimg
        out_file.write( moviename + "|" + movieimg + "\n")
        movie_dict_list.append(movie_dict)
        counter = counter + 1
    start_limit = int(start_limit) + int(end_limit)
    start_limit = str(start_limit)
    BASE_URL = BASE_URL = START_URL + servicefilter + START_LI_URL+ start_limit + END_LI_URL + end_limit + LAST_URL
    page = requests.get(BASE_URL)

json.dump(movie_dict_list,json_file)

json_file.close()
out_file.close()

print counter
