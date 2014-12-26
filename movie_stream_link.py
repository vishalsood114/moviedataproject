import os
import io
import time
import json
from sys import argv
from os.path import exists
from urllib2 import urlopen


script, raw_file, to_file, json_file = argv


BASE_URL = "http://www.canistream.it/search/movie/"

if exists(to_file):
    if os.stat(to_file).st_size > 0:
        open(to_file, 'w').close()
else:
    print "Enter a file that exists to write data"
    sys.exit(0)

out_file = open(to_file, 'w')
json_file = open(json_file, 'w')
counter = 0


def get_movie_id(html):
	start_search_m = html.find('div class="search-result row" rel=')
    	if start_search_m == -1: 
        	return None, None,None,0
    	start_movie_id = html.find('rel', start_search_m)
    	end_movie_id = html.find('"', start_movie_id + 5)
    	movie_id = html[start_movie_id + 5:end_movie_id]

    	start_movie_name = html.find('data1', end_movie_id)
    	end_movie_name = html.find('"', start_movie_name + 7)
    	movie_name = html[start_movie_name + 7:end_movie_name]

    	start_canis_link = html.find('data2', end_movie_name)
    	end_canis_link = html.find('"', start_canis_link + 7)
    	canis_link = html[start_canis_link + 7:end_canis_link]

    	return movie_id, movie_name, canis_link, end_canis_link

def get_imdb_link(html,start_search_from):
	start_search = html.find('<a class="imdb-link sprite" href=', start_search_from)
    	if start_search == -1: 
        	return None, 0
    	start_imdb_link = html.find('href', start_search)
    	end_imdb_link = html.find('"', start_imdb_link + 6)
    	imdb_link = html[start_imdb_link + 6:end_imdb_link]
    	return imdb_link, end_imdb_link

def get_rt_link(html,start_search_from):
	start_search = html.find('<a class="rt-link sprite" href=')
   	if start_search == -1: 
        	return None, 0
    	start_rt_link = html.find('href', start_search)
    	end_rt_link = html.find('"', start_rt_link + 6)
    	rt_link = html[start_rt_link + 6:end_rt_link]
    	return rt_link, end_rt_link

movie_price_list =[]
with open(raw_file) as f:
    moviename = f.readlines()
    for movienid in moviename:
        movie_dict = {}
        movie = movienid.split('|')[1]
        print "Reading Movie: " + movie
        movie_dict["imdbID"] = movienid.split('|')[0]
        movie_dict["nameMovie"] = movie 
        out_file.write("\n"+ movie)
        out_file.write("----------------------------------------------------" + "\n")
        query_url = movie.replace(' ','%20')
        # time.sleep(1)
        html = urlopen(BASE_URL + query_url).read()
        movieid, movie_name, canis_link, end_canis_link = get_movie_id(html)
        if not movieid:
            continue
        out_file.write("MovieId : " + movieid + "\n")
        movie_dict["CanMovieId"] = movieid
        movie_dict["CanMovieLink"] = canis_link
        if canis_link:
	    out_file.write ("Canistream.it link : " + canis_link + "\n")

        
	imdb_link, end_imdb_link = get_imdb_link(html,end_canis_link)
        if imdb_link: 
	    out_file.write("IMDB Link: " + imdb_link + "\n")

	rt_link, end_rt_link = get_rt_link(html,end_imdb_link)
        movie_dict["rtLink"] = rt_link
	if rt_link:
            out_file.write("Rotten Tomato Link: " + rt_link + "\n")

	# preparing to get prices from different services stream data
	streaming_types = ['streaming','rental','purchase','dvd', 'xfinity']
	PRICE_URL = "http://www.canistream.it/services/query?movieId="
	PART_URL = "&attributes=1&mediaType="

	for s in streaming_types:
	    sLink = s + "Link"
            FINAL_URL=PRICE_URL+movieid+PART_URL+s
            movie_dict[sLink]= FINAL_URL
	    out_file.write("\n" +FINAL_URL + "\n")
	    data = urlopen(FINAL_URL).read()
	    movie_dict[s]=json.loads(data)
            if data != '[]':
		price_data = json.loads(urlopen(FINAL_URL).read())
		json.dump(price_data,out_file)
        
        movie_price_list.append(movie_dict)
        counter = counter + 1

json.dump(movie_price_list,json_file)
json_file.close()
out_file.close()

#print movie_price_list
print counter

