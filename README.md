# Geocoding Service

This is a simple network service that can retrieve the lattitude and longitude of a given address. The service takes in an address and request for the location form Google Map server or HERE Map server.

## Dependencies

This module uses the python library ```requests``` library for send HTTP requests.
The following link provides instructions on how to install requests on Mac, Windows and Linux

`https://programminghistorian.org/lessons/installing-python-modules-pip`

## Usage

### In Python Command Line

By default, the service uses Google Map to retrieve locations

First open a terminal and open Python (Python 2.7 was used in this demo)

```
$python
Python 2.7.10 (default, Jul 15 2017, 17:16:57) 
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Then import the module (make sure to be in the directory that contains the module)

```
>>> import GeocodingService as gs
>>> geo_service = gs.GeocodingService()
>>> geo_service.Get("San Francisco, CA")
Getting Lattitude and Longitude from Google Map

Given Address: San Francisco, CA

Formatted Address: San Francisco, CA, USA

Location: (37.7749295, -122.4194155)

(37.7749295, -122.4194155)
>>>
```

In the case that the service cannot retrieve data from Google Map for some reason, for example a Google Developer Key is not available (this can be tested by moving the file google_dev_key.txt outside of the directory). The service would retrieve data from HERE Map.

The program would prompt the user the missing key and switch to using HERE Map.

```
>>> geo_service = gs.GeocodingService()
Error obtaining Google Map Developer Key from google_dev_key.txt

WARNING: Google Developer Key not found, the servie will not be able to retrieve data from Google Map

>>> geo_service.Get("San Francisco, CA")
Getting Lattitude and Longitude from Google Map

Google Map requires a developer key in order to obtain data. Please provide a developer key

Getting Lattitude and Longitude from HERE Map

Given Address: San Francisco, CA

Formatted Address: San Francisco, CA<br/>USA

Location: (37.77713, -122.41964)

(37.77713, -122.41964)
>>>
```

### In Software Development

If the service is to be used in another piece of code, simply import the module and instatiate the object before use

```
import GeocodingService as gs

my_service = gs.GeocodingService()

address = "Worcester, MA"

lat_long = my_service.Get(address)
```