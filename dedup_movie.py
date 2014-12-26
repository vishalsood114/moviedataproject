import os
from sys import argv
from os.path import exists

script, file1, file2, to_file = argv

if exists(to_file):
    if os.stat(to_file).st_size > 0:
        open(to_file, 'w').close()
else:
    print "Enter a file that exists to write data"
    sys.exit(0)

out_file = open(to_file, 'w')
counter = 0

file1data = open(file1).read()
#print file1data

with open(file2) as f:
    moviename = f.readlines()
    for movie in moviename:
        if movie.rstrip() in file1data :
            continue
        out_file.write(movie)
        #print movie[7:39]
        #out_file.write(movie.split('|')[0]+ "\n")
        #out_file.write(movie[7:39] + "\n")
        counter = counter + 1

out_file.close()



print counter