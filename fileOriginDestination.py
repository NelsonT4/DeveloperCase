
import json

def get_origin_destination():
    with open('origin-destination.json', 'r') as archivo:
        origin_destination = json.load(archivo)
    #print(origin_destination)

    routes = origin_destination["routes"]
    return routes

if __name__ == "__main__":
    result = get_origin_destination()
    print(result)