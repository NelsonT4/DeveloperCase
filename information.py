import datetime
import time
import cloudscraper
import random
from consultOriginDestination import travels_origin_destination
from datetime import datetime, UTC


def get_information():
    url_api = "https://seats.aero/_api/"
    subfolder = "enrichment_modern/"
    id_consult = "2sLR0PBuXlADUltse4AnOjGNiEl"
    params_secondary = {"min_seats": "1",
                        "applicable_cabin": "any",
                        "additional_days": "true",
                        "additional_days_num": "14",
                        "max_fees": "100000",
                        "disable_live_filtering": "false",
                        "date": "2026-01-01"}
    query = "&".join([f"{key}={value}" for key, value in params_secondary.items()])
    airlines_origins_destinations = travels_origin_destination(url_api, query)
    user_agents = [
        'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, como Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900 Build/LRX21V) AppleWebKit/537.36 (KHTML, como Gecko) SamsungBrowser/Chrome 2.1/ Mobile 34.0.1847.76 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.0; HTC 10 Build/NRD90M) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.136 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    ]
    selected_user_agent = random.choice(user_agents)
    proxy = {'https1': 'https://162.214.3.183:3128',
             'https2': 'http://88.198.212.91:3128'}
    headers = {'User-Agent': selected_user_agent}
    origin_destination_information = []
    date = datetime.now(UTC)
    date_format = date.isoformat()
    origin_destination_information.append({
        "run_timestamp_utc": str(date_format)
    })
    for airline_origin_destination in airlines_origins_destinations:
        id = airline_origin_destination["id"]
        query_params = "?m=1" + query
        origin = "&origins=" + airline_origin_destination["oa"]
        destination = "&destinations=" + airline_origin_destination["da"]
        url = url_api + subfolder + id + query_params + origin + destination
        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            try:

                time.sleep(20)
                scraper = cloudscraper.create_scraper(
                    interpreter='nodejs',
                    delay=2000,

                    # Browser emulation

                    # Debug mode
                    # debug=True
                )
                selected_user_agent = random.choice(user_agents)

                headers = {'User-Agent': selected_user_agent}
                response = scraper.get(url, headers=headers)
                data = response.json()
                trips = data["trips"]
                # print(response)
                break
            except ValueError as e:
                attempts += 1
                print(response)
                print(f"Error: {e}. Trying again in 41 seconds. Information... (Attempts {attempts}/{max_attempts})")
                if attempts < max_attempts:
                    time.sleep(41)
                else:
                    print("The maximum number of retries has been reached. Aborting.")
            except KeyError as e:
                attempts += 1
                print(response)
                print(f"Error: {e}. Trying again in 50 seconds. Information... (Attempts {attempts}/{max_attempts})")
                if attempts < max_attempts:
                    time.sleep(50)
                else:
                    print("The maximum number of retries has been reached. Aborting.")
            except ConnectionRefusedError:
                print("Error: The connection was rejected. Please ensure the service is working.")
                time.sleep(100)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                time.sleep(100)

        for trip in trips:
            intTotalDuration = int(trip.get("TotalDuration"))
            hour = intTotalDuration // 60
            minutes = intTotalDuration % 60
            legs = trip["AvailabilitySegments"]
            leg_info = []

            for leg in legs:
                leg_info.append({
                    "leg_departure_datetime": leg.get("DepartsAt"),
                    "leg_arrival_datetime": leg.get("ArrivesAt"),
                    "leg_flight_number": leg.get("FlightNumber"),
                    "leg_distance": leg.get("Distance"),
                    "leg_airplane": leg.get("AircraftName"),
                    "leg_class": leg.get("Cabin")

                })
                total_taxes = trip.get("TotalTaxes") / 100
                if trip.get("TotalTaxes") > 0:
                    tax = " + " + " " + str(total_taxes) + trip.get("TaxesCurrency")
                else:
                    tax = ""

            origin_destination_information.append({
                "origin_dest_pair": ({
                    "inputs_from": trip.get("OriginAirport"),
                    "inputs_to": trip.get("DestinationAirport"),
                    "program": trip.get("Source"),
                    "departure_date": str(datetime.fromisoformat(trip.get("DepartsAt").replace('Z', '+00:00')).date()),
                    "duration": f"{hour}h {minutes}m",
                    "class": trip.get("Cabin"),
                    "stop": trip.get("Stop"),
                    "flight_numbers": trip.get("FlightNumbers"),
                    "last_updated": trip.get("UpdatedAt"),
                    "point_price_raw": trip.get("Cabin")
                                       + " ("
                                       + trip.get("AvailabilitySegments", {})[0].get("FareClass")
                                       + str(trip.get("RemainingSeats"))
                                       + ") "
                                       + "{:,.0f}".format(int(trip.get("MileageCost")))
                                       + " pts" + tax,
                    "point_amount": trip.get("MileageCost"),
                    "points_program_currency": trip.get(""),

                    "cash_copay_raw": trip.get("TaxesCurrencySymbol") + str(total_taxes),
                    "cash_copay_amount": total_taxes,
                    "cash_copay_currency": trip.get("TaxesCurrency"),
                    "cents_per_point": 1.6,
                    "total_value_usd": (1.6 / 100) * trip.get("MileageCost"),
                    "legs": leg_info
                })
            })

    # print(origin_destination_information)
    return origin_destination_information


if __name__ == "__main__":
    result = get_information()
    print(result)
