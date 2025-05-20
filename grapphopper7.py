import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "c5daa5d0-4eea-430a-ab49-a037e7775e92"  # Replace with your API key

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    try:
        replydata = requests.get(url)
        replydata.raise_for_status()  # Raise an error for HTTP issues
        json_status = replydata.status_code

        if json_status == 200:
            json_data = replydata.json()
            if not json_data["hits"]:
                print(f"No results found for {location}.")
                return json_status, "null", "null", location

            lat = json_data["hits"][0]["point"]["lat"]
            lng = json_data["hits"][0]["point"]["lng"]
            name = json_data["hits"][0]["name"]
            value = json_data["hits"][0]["osm_value"]

            country = json_data["hits"][0].get("country", "")
            state = json_data["hits"][0].get("state", "")

            if state and country:
                new_loc = f"{name}, {state}, {country}"
            elif state:
                new_loc = f"{name}, {state}"
            else:
                new_loc = name

            print(f"Geocoding API URL for {new_loc} (Location Type: {value})\n{url}")
            return json_status, lat, lng, new_loc
        else:
            print(f"Error: Received status code {json_status} for {location}.")
            return json_status, "null", "null", location
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "error", "null", "null", location

if __name__ == "__main__":
    while True:
        print("\n+++++++++++++++++++++++++++++++++++++++++++++")
        print("Vehicle profiles available on Graphhopper:")
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print("car, bike, foot")
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        profile = ["car", "bike", "foot"]
        vehicle = input("Enter a vehicle profile from the list above: ")
        if vehicle.lower() in ["quit", "q"]:
            break
        elif vehicle not in profile:
            print("No valid vehicle profile was entered. Using the car profile.")
            vehicle = "car"

        loc1 = input("Starting Location (type 'quit' or 'q' to exit): ")
        if loc1.lower() in ["quit", "q"]:
            break
        orig = geocoding(loc1, key)

        loc2 = input("Destination (type 'quit' or 'q' to exit): ")
        if loc2.lower() in ["quit", "q"]:
            break
        dest = geocoding(loc2, key)

        print("================================================")
        if orig[0] == 200 and dest[0] == 200:
            op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
            dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
            paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
            paths_status = requests.get(paths_url).status_code
            paths_data = requests.get(paths_url).json()
            print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
            print("=================================================")
            print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
            print("=================================================")
            if paths_status == 200:
                miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
                km = (paths_data["paths"][0]["distance"]) / 1000
                sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
                min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
                hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
                rendimiento_km_litro = 12.0
                combustible_requerido = km/rendimiento_km_litro
                print("Distance Traveled: {0:.1f} miles / {1:.1f} km".format(miles, km))
                print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
                print("Combustible requerido: {0:.2f} litros".format(combustible_requerido))
                print("=================================================")
                for each in range(len(paths_data["paths"][0]["instructions"])):
                    path = paths_data["paths"][0]["instructions"][each]["text"]
                    distance = paths_data["paths"][0]["instructions"][each]["distance"]
                    print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance / 1000, distance / 1000 / 1.61))
                    print("=============================================")
            else:
                print("Error message: " + paths_data["message"])
                print("*************************************************")