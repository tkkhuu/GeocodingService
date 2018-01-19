import requests
import json

class GeocodingService(object):
    
    def __init__(self, google_api_key="", app_code="", app_id=""):
        
        '''Constructor for the GeocodingService class
        The constructor takes in a Google Developer Key (google_api_key) in order to send request to the Google Map server.
        The constructor also takes in the HERE authentication keys (app_code and app_id) in order to send request to the HERE Map server.
        
        If no Google Developer Key is given as a parameter, 
        the constructor will look for the key in the file 'google_dev_key.txt' and 
        this file should be stored in the same directory as this file.
        The format of 'google_dev_key.txt' is as follow:
        
        "
        AIzaSyAtlkaToj19XyzrRQxRiblaIBJ2fvDzNgk
        "
        
        Similarly, if no HERE authentication keys are provided as a parameter, 
        the constructor will look for the keys in the file 'here_dev_key.txt' 
        and this file should be stored in the same directory as this file. 
        The format of 'here_dev_key.txt' should be as follow:
        
        "
        app_id:
        OH2hXeK7Ryp87WsLqw0u
        app_code: 
        nGzzG4bQvPkxDi5af5x0OQ
        "
        
        '''
        
        # Retrieving keys from parameter
        self.__google_dev_key = google_api_key
        self.__here_app_code = app_code
        self.__here_app_id = app_id
        
        # If google dev key not found, look for google_dev_key.txt
        if (self.__google_dev_key==""):
            try:
                f = open("google_dev_key.txt", "r")
                self.__google_dev_key = f.readline()
                f.close()
            except:
                print "Error obtaining Google Map Developer Key from google_dev_key.txt\n"
        
        # If Google key cannot be retrieved from google_dev_key.txt, print a warning
        if (self.__google_dev_key==""):
            print "WARNING: Google Developer Key not found, the servie will not be able to retrieve data from Google Map\n"
        
        # If HERE dev key not found, look for google_dev_key.txt
        if (self.__here_app_code=="" or self.__here_app_id==""):
            try:
                f = open("here_dev_key.txt","r")
                lines = f.read().splitlines()
                self.__here_app_id = lines[1]
                
                self.__here_app_code = lines[3]
                
                f.close()
                
            except:
                print "Error obtaining HERE developer authentication from here_dev_key.txt\n"
                
        # If HERE key cannot be retrieved from google_dev_key.txt, print a warning
        if (self.__here_app_code=="" or self.__here_app_id==""):
            print "WARNING: HERE developer authentication not found, the service will not be able to retrieve datat from HERE map\n"

    
    # ============ Helper Functions ============
    def __CreateJSONFromAddress(self, addr, service = "Google"):
        '''
        This is a helper function that takes an address string and a service type and output a json object for query.
        '''
        if (service == "Google"):
            return {
                'address': addr,
                'key': self.__google_dev_key 
            } 
        else:
            return {
                'at': '0.0000,0.0000',
                'q': addr,
                'app_id': self.__here_app_id,
                'app_code': self.__here_app_code
            }
        
    
    def __LocationFromGoogleMap(self, addr):
        '''
        This is a helper function that takes an address and send a query request to the Google Map to retrieve lat and lng.
        '''
        
        print "Getting Lattitude and Longitude from Google Map\n"
        
        # If no developer key found, data can't be retrieved, prompt the user and return
        if (self.__google_dev_key == ""):
            print "Google Map requires a developer key in order to obtain data. Please provide a developer key\n"
            return
        
        # The Google Map server URL
        google_map_url = "https://maps.googleapis.com/maps/api/geocode/json"
        
        # The JSON object that represents the data to be queried
        json_object = self.__CreateJSONFromAddress(addr, service="Google")
        
        # A tuple to be returned
        lat_long = (0, 0)
        
        try:
            # Use the module requests in send a GET request
            r = requests.get(google_map_url, params=json_object)
            
            # Convert the response into json using the json module and enter the results field
            results = r.json()['results']
        
            # Enter the location field of the response
            location = results[0]['geometry']['location']
        
            # update output tuple
            lat_long = (location['lat'], location['lng'])
            
            # Print out the input address and the address that Google Map used for query
            print "Given Address: " + addr + "\n"
            print "Formatted Address: " + results[0]['formatted_address'] + "\n"
            
        except:
            # If something goes wrong prompt the user and return NULL
            print "Unable to retrieve data from Google Map\n"
            lat_long = None
            
        return lat_long
    
    
    def __LocationFromHEREMap(self, addr):
        '''
        This is a helper function that takes an address and send a query request to the HERE Map to retrieve lat and lng.
        '''
        
        print "Getting Lattitude and Longitude from HERE Map\n"
        
        # If no developer key found, data can't be retrieved, prompt the user and return
        if (self.__here_app_id == "" or self.__here_app_code == ""):
            print "HERE Map requires an app_id and app_code in order to obtain data. Please make sure to provide these values\n"
            return
        
        # The HERE Map server URL
        here_map_url = "https://places.cit.api.here.com/places/v1/discover/search"
        
        # The JSON object that represents the data to be queried
        json_object = self.__CreateJSONFromAddress(addr, service ="HERE")
        
        # A tuple to be returned
        lat_long = (0, 0)
        
        try:
            # Use the module requests in send a GET request
            r = requests.get(here_map_url, params=json_object)

            # Convert the response into json using the json module and enter the results field
            results = r.json()['results']
        
            # Update the returned tuple
            lat_long = (results['items'][0]['position'][0], results['items'][0]['position'][1])
        
            # Print out the input address and the address that HERE Map used for query
            print "Given Address: " + addr + "\n"
            print "Formatted Address: " + results['items'][0]['title'] + ", " + results['items'][0]['vicinity'] + "\n"
       
        except:
            # If something goes wrong prompt the user and return NULL
            print "Unable to retrieve data from HERE Map\n"
            lat_long = None
        
        return lat_long
        
        
    
    
    # ============ Main Functions ============
    def Get(self, addr):
        '''This function is used to retrieve the lattitude and longitude of a given address.
        
        Args:
            addr (str): Raw string of an address.
                        Example:    "San Francisco, CA", 
                                    "100 Institute Rd, Worcester, MA"
        
        Returns:
            (double, double): tuple of lat and long is returned if one is found
            
            None: Null if there is no match or something went wrong
        '''
        lat_long = self.__LocationFromGoogleMap(addr)
        
        if (lat_long is None):
            lat_long = self.__LocationFromHEREMap(addr)
        
        if (lat_long is None):
            print "Unable to retrieve location from Google Map and HERE Map, please check connection\n"
            return
        
        print "Location: " + str(lat_long) + "\n"
        
        return lat_long
    

