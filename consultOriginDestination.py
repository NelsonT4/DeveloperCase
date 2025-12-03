import json
import time
from itertools import cycle
import cloudscraper
from filePrograms import get_programs
from fileOriginDestination import get_origin_destination

def travels_origin_destination( url_api, query):
    program_list = get_programs()
    routes = get_origin_destination()
    subfolder = "search_partial?"
    travel_origin_destination=[]


    for route in routes:
        origin= "&origins=" + route['origin']
        destination= "&destinations=" + route['destination']
        url = url_api + subfolder + query + origin + destination
        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            try :
                #time.sleep(3)

                scraper = cloudscraper.create_scraper(
                    # Proxy rotation
                    interpreter='js2py',
                    delay=5,

                    # Browser emulation
                    browser='chrome',

                    # Debug mode
                    #debug=True
                )
                response= scraper.get(url)
                data = response.json()
                metadata = data["metadata"]
                break

            except ValueError as e:
                attempts += 1
                print(response)
                print(f"Error: {e}. Trying again in 5 seconds... (Attempt {attempts}/{max_attempts})")
                if attempts < max_attempts:
                    time.sleep(5)
                else:
                    print("The maximum number of retries was reached when querying origin_Destination. Aborting.")

        for data in metadata:
            source= data["source"]
            if (source in program_list):
                travel_origin_destination.append({
                    "id": data.get("id"),
                    "source": data.get("source"),
                    "date": data.get("date"),
                    "oa": data.get("oa"),
                    "da": data.get("da")
                })

    return travel_origin_destination

if __name__ == "__main__":
    result = travels_origin_destination()
    print(result)