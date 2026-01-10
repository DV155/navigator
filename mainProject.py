import urllib.request, urllib.parse
import json, ssl
import math

url = "https://api.geoapify.com/v1/geocode/search?"
apiKey = "c4c54e3132cf4ce4becca78b555da324"
radius = 6371 #Earth's radius for haversine formula

def locationFinder(): 
    locationOne = input("What is your first location?")
    locationTwo = input("What is your second location?")

    locationOne = locationOne.strip()
    locationTwo = locationTwo.strip()
    parmsO = dict()
    parmsD = dict()
    parmsO["text"] = locationOne
    parmsO["apiKey"] = apiKey
    parmsD["text"] = locationTwo
    parmsD["apiKey"] = apiKey

    try:
        urlOrigin = url + urllib.parse.urlencode(parmsO)
        urlDestination = url + urllib.parse.urlencode(parmsD)
        print(f"Retrieving: {urlOrigin} and {urlDestination}")
        uhO = urllib.request.urlopen(urlOrigin)
        uhD = urllib.request.urlopen(urlDestination)
        dataO = uhO.read().decode()
        dataD = uhD.read().decode()
        try:
            jsO = json.loads(dataO)
            print("\n--- ORIGIN ---")
            print(json.dumps(jsO, indent=2))
        except:
            jsO = None
            if not jsO or 'features' not in jsO:
                print('==== Origin Download error ===')
                print(dataO)
            elif len(jsO['features']) == 0:
                print('==== Origin Object not found ====')
                print(dataO)
        try:
            jsD = json.loads(dataD)
            print("\n--- DESTINATION ---")
            print(json.dumps(jsD, indent=2))
        except:
            jsD = None
            if not jsD or 'features' not in jsD:
                print('==== Destination Download error ===')
                print(dataD)
            elif len(jsD['features']) == 0:
                print('==== Destination Object not found ====')
                print(dataD)
            latO = jsO['features'][0]['properties']['lat']
            lonO = jsO['features'][0]['properties']['lon']
            latD = jsD['features'][0]['properties']['lat']
            lonD = jsD['features'][0]['properties']['lon']
            newLatO = math.radians(float(latO))
            newLonO = math.radians(float(lonO))
            newLatD = math.radians(float(latD))
            newLonD = math.radians(float(lonD))
            latDiff = newLatD - newLatO
            lonDiff = newLonD - newLonO
            a = (math.sine(latDiff / 2) ** 2) + math.cos(latO ) * math.cos(latD) * (math.sine(lonDiff / 2) ** 2)      #square of half of chord length
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) #central angle
            distance = radius * c
            print("The distance is", distance, "kilometers")
            print("Mean walking time should be", distance / 4.8 )
    except Exception as e:
        print(f"Error: {e}")

locationFinder()