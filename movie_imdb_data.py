import re
import requests
import urllib
import json
BASE_URL = 'http://www.omdbapi.com/?'

movie_name = "The Shawshank Redemption"
query = {'i': '', 't': movie_name ,'tomatoes':'true'}
response = requests.get(BASE_URL+urllib.urlencode(query))
output = json.dumps(response.content, separators=(',',':'))


movie_detail = {}


try:
    temp_data = output.split(",")
    #print temp_data
    for i in temp_data:
        data = re.sub(r'\\+','',i).replace('\\','')
        print data.split(':')[0]
except IndexError,e:
    print "Error Occured! %s" %e


