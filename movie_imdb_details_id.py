# Get IMDB Movie details by using IMDBID
import re
import requests
import urllib
import json
import os
from sys import argv
from os.path import exists

script, source_file, to_file  = argv
 
BASE_URL = 'http://www.imdbapi.com/?'
#NAME_LIST = file('5000UniqueIMDBidTest.txt','r')
 
def get_movie_info(imdb_id):
	query = {'i':imdb_id,'t':'','tomatoes':'true'}
	part = urllib.urlencode(query)
	url = BASE_URL + part
	response = requests.get(url)
	movie_info  = json.loads(response.content)
 	
	return movie_info
		
def get_movi_name():
	if exists(to_file):
    	    if os.stat(to_file).st_size > 0:
        	open(to_file, 'w').close()
	else:
    	    print "Enter a file that exists to write data"
    	    return 
        
        out_file = open(to_file, 'w')
        counter = 0
        movie_details_list = []
        name_list = open(source_file).readlines()
        #print name_list
	for imdb_id in name_list:
		print "Getting Movie %s " % imdb_id
                movie_details = get_movie_info(imdb_id.rstrip())
		#json.dump(movie_details,out_file)
		#print movie_details
		movie_details_list.append(movie_details)
		counter = counter + 1
	json.dump(movie_details_list,out_file)
	#print out_file
	return counter

	
if __name__=='__main__':
	counter = get_movi_name()
        print "Total movies %s" %counter
