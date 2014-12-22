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
	output  = json.dumps(response.content, separators=(',',':'))
	movie_info = {}
	info_list = ['Title','Year', 'Rated', 'Released', 'Runtime','Genre', 'Director','Writer', 'Actors', 'Plot','Language', 'Country','Awards','Poster','Metascore', 'Rating', 'imdbVotes', 'imdbID','tomatoMeter','tomatoImage','tomatoRating','tomatoReviews', 'tomatoFresh', 'tomatoRotten', 'tomatoConsensus', 'tomatoUserMeter', 'tomatoUserRating']
	for info in info_list:
                if info == 'Rating':
		    movie_info['IMDB Rating'] = get_and_clean_data(info, output)
		movie_info[info] = get_and_clean_data(info, output)
 
	return movie_info
	
def get_and_clean_data(tag,data):
	try:
	    temp_data = data.split(tag)[1].split(",")[0]
	    data = re.sub(r':\\"+','',temp_data).replace('\\"','')
	except IndexError,e:
            print "Error Occured! %s" %e
	    return ""	
	
        return data
	
def get_movi_name(name_list):
	if exists(to_file):
    	    if os.stat(to_file).st_size > 0:
        	open(to_file, 'w').close()
	else:
    	    print "Enter a file that exists to write data"
    	    return 
        
        out_file = open(to_file, 'w')
        counter = 0
	for name in name_list:
		print "Getting Movie %s " % name
                movie_details = get_movie_info(name)
		json.dump(movie_details,out_file)
		counter = counter + 1
	return counter
	
if __name__=='__main__':
	counter = get_movi_name(NAME_LIST)
        print "Total movies %s" %counter
