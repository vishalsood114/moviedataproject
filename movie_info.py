import os
from sys import argv
from os.path import exists

script, raw_file, to_file = argv

if exists(to_file):
    if os.stat(to_file).st_size > 0:
        open(to_file, 'w').close()
else:
    print "Enter a file that exists to write data"
    sys.exit(0)

out_file = open(to_file, 'w')
counter = 0

with open(raw_file) as f:
    moviename = f.readlines()
    for movie in moviename:
        print movie
        out_file.write(movie.split('|')[0]+ "\n")
        counter = counter + 1

out_file.close()

print counter

