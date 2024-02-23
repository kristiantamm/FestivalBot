import requests
import csv
import math
import PySimpleGUI as sg

location = "Pärnu" #input("Asukoht: ")
checkin = "2024-07-11" #input("Check in (yyyy-mm-dd): ")
checkout = "2024-07-13" #input("Check out (yyyy-mm-dd): ")
adults = "6"#input("Adults: ")
festivalCoord = ()

class Listing():
    def __init__(self, id, deeplink, name, beds, coordinates, persons, address, price):
        self.id = id
        self.deeplink = deeplink
        self.name = name
        self.beds = beds
        self.coordinates = coordinates
        self.persons = persons
        self.address = address
        self.price = price


def fetchRawData(location, checkin, checkout, adults):
    url = "https://airbnb13.p.rapidapi.com/search-location"
    querystring = {"location":location,"checkin": checkin,"checkout":checkout,"adults":str(adults),"children":"0","infants":"0","pets":"0","page":"1","currency":"EUR"}
    headers = {
        "X-RapidAPI-Key": "API-key",
        "X-RapidAPI-Host": "airbnb13.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data["results"]

def dataIntoListings(data):
    listingArr = []
    for json in data:
        listingArr.append(Listing(json["id"], json["deeplink"], json["name"], json["beds"],
                                (json["lat"], json["lng"]), json["persons"], json["address"], json["price"]))
        

def euclidean_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Calculate differences in coordinates
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    
    # Calculate Euclidean distance
    distance = math.sqrt(delta_lat**2 + delta_lon**2) * 6371  # Earth's radius in kilometers
    
    return distance


def updateListingCSV(listings):
    # Check if the listing ID already exists in the CSV file
    existing_ids = set()
    try:
        with open('listings.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_ids.add(row['id'])
    except FileNotFoundError:
        pass  # If file not found, it means there are no existing listings

    # Write new listings to the CSV file
    with open('listings.csv', 'a', newline='') as csvfile:
        fieldnames = ['id', 'deeplink', 'name', 'beds', 'coordinates', 'persons', 'address', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for listing in listings:
            if listing.id not in existing_ids:
                writer.writerow({'id': listing.id,
                                 'deeplink': listing.deeplink,
                                 'name': listing.name,
                                 'beds': listing.beds,
                                 'coordinates': listing.coordinates,
                                 'persons': listing.persons,
                                 'address': listing.address,
                                 'price': listing.price})
    print("CSV updated!")


def main():
    layout = [

    ]
    window = sg.Window("TravelBot", layout)

    while True:
        event, values = window.read()

        

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

    window.close()