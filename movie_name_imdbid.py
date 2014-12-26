import os
import io
import json
from sys import argv
from os.path import exists


script, json_file, to_file = argv

if exists(to_file):
    if os.stat(to_file).st_size > 0:
        open(to_file, 'w').close()
else:
    print "Enter a file that exists to write data"
    sys.exit(0)

out_file = io.open(to_file, 'w', encoding='utf8')
counter = 0

json_data = json.load(open(json_file))

for movie_details in json_data:
    print movie_details["imdbID"] + "|" + movie_details["Title"]
    out_file.write(movie_details["imdbID"] + "|" + movie_details["Title"] + "\n")
    counter = counter + 1

out_file.close()

print counter