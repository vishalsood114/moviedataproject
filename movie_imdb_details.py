# Get IMDB Movie details by setting movie name
import re
import requests
import urllib
import json
import os
from sys import argv
from os.path import exists

script, to_file  = argv
 
BASE_URL = 'http://www.imdbapi.com/?'
NAME_LIST = file('IMDBMovieName.txt','r')
 
def get_movie_info(movi_name):
	query = {'i': '', 't': movi_name ,'tomatoes':'true'}
	part = urllib.urlencode(query)
	url = BASE_URL+part
	response = requests.get(url)
	movie_info  = json.loads(response.content)
 
	return movie_info
		
def get_movi_name(name_list):
	if exists(to_file):
    	    if os.stat(to_file).st_size > 0:
        	open(to_file, 'w').close()
	else:
    	    print "Enter a file that exists to write data"
    	    return 
        
        out_file = open(to_file, 'w')
        counter = 0
        movie_details_list = []
	for name in name_list:
		print "Getting Movie %s " % name
                movie_details = get_movie_info(name)
                #print type(movie_details)
		#json.dump(movie_details,out_file)
		movie_details_list.append(movie_details)
		counter = counter + 1
	json.dump(movie_details_list,out_file)
	#print out_file
	return counter

	
if __name__=='__main__':
	counter = get_movi_name(NAME_LIST)
        print "Total movies %s" %counter
