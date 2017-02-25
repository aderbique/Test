
import urllib
import json
####################################
# Used to determine location
import requests

send_url = 'http://freegeoip.net/json' #Gets a json list of IP information to locate you
r = requests.get(send_url)
j = json.loads(r.text)

locationLat = j['latitude']
locationLong = j['longitude']

#print locationLat #used for testing latitude coordinates
#print locationLong #used for testing longitude coordinates

#########################################

#locationLat = 41.745161 #lat and long for Logan, Ut
#locationLong = -111.8119312

########################################
#Yelp API for Yelp URL
import rauth
def get_search_parameters(lat,lng):
  #See the Yelp API for more details
  params = {}
  params["term"] = "restaurant"
  params["ll"] = "{},{}".format(str(lat),str(lng))
  params["radius_filter"] = "25"
  params["limit"] = "15"
  return params

def get_results(params):
 
  #Obtain these from Yelp's manage access page
  consumer_key = "KdToqI0MOZpwy__h9P0G5Q"
  consumer_secret = "gyLFUGT8qdPx5s0Y7-DuwPjW1pY"
  token = "5shzFD20R6U7veZrMKUU8I0CwVD_qcEC"
  token_secret = "Tlu11jZiJhgapgW1WEZD3Yf4A3U"
   
  session = rauth.OAuth1Session(
    consumer_key = consumer_key
    ,consumer_secret = consumer_secret
    ,access_token = token
    ,access_token_secret = token_secret)
     
  request = session.get("http://api.yelp.com/v2/search",params=params)
   
  #Transforms the JSON API response into a Python dictionary
  data = request.json()
  session.close()
   
  return data

def get_yelp_url(lat,lng):
    try:
        yelpData = get_results(get_search_parameters(lat,lng))
        if yelpData is not None:
            if yelpData['businesses'] is not None:
                if yelpData['businesses'][0] is not None:
                    if yelpData['businesses'][0]['url'] is not None:
                        yelpURL = yelpData['businesses'][0]['url']
                        return yelpURL
    except:
        pass

#########################################


radius = 8000

searchType = 'restaurant' #configure this from one here: https://developers.google.com/places/supported_types
encodedType = urllib.quote(searchType)

searchKeyWord = 'burger' #Use this to search for a keyword. I.e Burger
encodedKeyWord = urllib.quote(searchKeyWord)


rawData = urllib.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(locationLat) + ',' + str(locationLong) + '&radius=' + str(radius) + '&type=' + encodedType + '&keyword=' + encodedKeyWord + '&key=AIzaSyBueezSv1I_p8lywu8vm88YevVptloCcjo')

#rawData = urllib.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=41.745161,-111.8119312&radius=8000&type=bar&keyword=&key=AIzaSyBueezSv1I_p8lywu8vm88YevVptloCcjo

jsonData = json.load(rawData)
searchResults = jsonData['results']


for er in searchResults:
    name = er['name']
    restaurantRating = er['rating']
    vicinity = er['vicinity']
    types = er['types']
    print 'The name of restaurant is: ' + name
    print 'The restaurant rating is: ' + str(restaurantRating)
    print 'Location: ' + vicinity
    #print types

    lat = er['geometry']['location']['lat']
    lng = er['geometry']['location']['lng']

    yelpURL = get_yelp_url(lat,lng)
    if yelpURL is not None: print yelpURL
    print '''

            '''

