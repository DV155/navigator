import urllib.request, urllib.parse
import json, ssl
import math

url = "https://api.geoapify.com/v1/geocode/search?"
apiKey = "c4c54e3132cf4ce4becca78b555da324"
radius = 6371 #Earth's radius for haversine formula
distanceWarning = "WARNING! Adresses in different countries, likely too long to walk"
countryCheck = False

def locationFinder(): 
    countryCheck = False
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
        print(f"Retrieving location of {locationOne} and {locationTwo}")
        uhO = urllib.request.urlopen(urlOrigin)
        uhD = urllib.request.urlopen(urlDestination)
        dataO = uhO.read().decode()
        dataD = uhD.read().decode()
        try:
            jsO = json.loads(dataO)
            #print("\n--- ORIGIN ---")
            #print(json.dumps(jsO, indent=2))
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
            #print("\n--- DESTINATION ---")
            #print(json.dumps(jsD, indent=2))
        except:
            jsD = None
            if not jsD or 'features' not in jsD:
                print('==== Destination Download error ===')
                print(dataD)
            elif len(jsD['features']) == 0:
                print('==== Destination Object not found ====')
                print(dataD)
        latO = jsO['features'][0]['properties']['lat']
        landO = jsO['features'][0]['properties']['country']
        landD = jsD['features'][0]['properties']['country']
        lonO = jsO['features'][0]['properties']['lon']
        latD = jsD['features'][0]['properties']['lat']
        lonD = jsD['features'][0]['properties']['lon']
        newLatO = math.radians(float(latO))
        newLonO = math.radians(float(lonO))
        newLatD = math.radians(float(latD))
        newLonD = math.radians(float(lonD))
        latDiff = newLatD - newLatO
        lonDiff = newLonD - newLonO
        a = (math.sin(latDiff / 2) ** 2) + math.cos(newLatO ) * math.cos(newLatD) * (math.sin(lonDiff / 2) ** 2)      #square of half of chord length
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) #central angle
        distance = radius * c
        time = distance / 4.8
        units = "hours"
        strDistance = str(distance)
        if time > 8760:
            time = time / 8760
            units = "years"
        elif time > 730:
            time = time / 730
            units = "months"
        elif time > 24:
            time = time / 24
            units = "days"
        if landO != landD:
            countryCheck = True
            print("WARNING! Adresses in different countries, likely too long to walk")
        print("The distance is", strDistance[:4] , "kilometres")
        print("Approximate walking time in a straight line should be", f"{time:.3g}", units)
        with open('index.html', 'r') as f: #HTML handle + editing
            html_content = f.read()
            centerLat = (latO + latD) / 2
            centerLon = (lonO + lonD) / 2
            html_content = html_content.replace('{{INITIAL-LOCATION}}', locationOne)
            html_content = html_content.replace('{{FINAL-LOCATION}}', locationTwo)
            if countryCheck:
                html_content = html_content.replace('{{DISTANCE}}', f'{strDistance[:4]} km {distanceWarning}' )
            else:
                html_content = html_content.replace('{{DISTANCE}}', f'{strDistance[:4]} km' )
            html_content = html_content.replace('{{UNITS}}', f'{units}')
            html_content = html_content.replace('{{WALKING-TIME}}', f'{time:.3g}')
            html_content = html_content.replace('{{CENTER_LAT}}', str(centerLat))
            html_content = html_content.replace('{{CENTER_LON}}', str(centerLon))
            html_content = html_content.replace('{{ZOOM_LEVEL}}', '4')  # Adjust zoom as needed
            html_content = html_content.replace('{{LAT_O}}', str(latO))
            html_content = html_content.replace('{{LON_O}}', str(lonO))
            html_content = html_content.replace('{{LAT_D}}', str(latD))
            html_content = html_content.replace('{{LON_D}}', str(lonD))
        with open('distance-map.html', 'w') as f:
            f.write(html_content)

        anotherOne = input("Do you want to check another location? Input something to continue")
        if len(anotherOne) > 0:
            locationFinder()
    except Exception as e:
        print(f"Error: {e}")
        tryAgain = input("Wanna try again? Input something to continue")
        if len(tryAgain) > 0:
            locationFinder()

locationFinder()