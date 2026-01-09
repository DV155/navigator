import urllib.request, urllib.parse
import json, ssl

url = "https://api.geoapify.com/v1/geocode/search?"
apiKey = "c4c54e3132cf4ce4becca78b555da324"

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
        except:
            jsD = None
            if not jsD or 'features' not in jsD:
                print('==== Destination Download error ===')
                print(dataD)
            elif len(jsD['features']) == 0:
                print('==== Destination Object not found ====')
                print(dataD)
    except Exception as e:
        print(f"Error: {e}")

locationFinder()