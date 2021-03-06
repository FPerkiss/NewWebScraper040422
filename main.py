# Import stuff to make it all work! [Libraries]
import requests as r
from bs4 import BeautifulSoup
import pandas as pd
#from numpy import random  # Adding sleep (prevent DDOS)
#from time import sleep  # Adding sleep (prevent DDOS)

# Store the data we want [Location, price, property type, property ID] after scraping/
prop_location = []
prop_price = []
prop_type = []
prop_id = []
url_pageNo = 0
prop_NoOfListings = None
prop_listings = None

# User selected variables [No of bedrooms, property type, location]
userSelected_rooms = None
userSelected_type = None
UserSelected_location = None

# User inputs [They select prop type, location and number of bedrooms.]
print("Please type one of the following 'detached', 'semi-detached', 'terraced', 'flat', 'bungalow', 'park-home':")
userSelected_type = input()
userSelected_rooms = int(input("Please enter the amount of bedrooms you have: "))

# When a place it entered it converts it to a code used on the rightmove website If it does not match then it will trow an error and ask again.
location_codes = {
    "canterbury": "5E279", "faversham": "5E507", "kent": "5E61307"
}
locationTrue = 0
while locationTrue == 0:
    userSelected_location = input("Please enter location: ").lower()
    panda_location = userSelected_location
    if userSelected_location in location_codes:
        userSelected_location = location_codes[userSelected_location]
        locationTrue = 1
    else:
        print("Please try a different location.")

# This url is used to get the properties with the parameters we want.
URL = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{userSelected_location}&maxBedrooms={userSelected_rooms}&minBedrooms={userSelected_rooms}&radius=0.0&index={url_pageNo}&propertyTypes={userSelected_type}&secondaryDisplayPropertyType=detachedshouses&includeSSTC=true&mustHave=&dontShow=&furnishTypes=&keywords="
page = r.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# Gets us the number of listings:
prop_NoOfListings = soup.find("span", {"class": "searchHeader-resultCount"})
prop_NoOfListings = prop_NoOfListings.get_text()
prop_NoOfListings = int(prop_NoOfListings.replace(",", ""))
print(prop_NoOfListings)

prop_search = soup.find(id="propertySearch")
container = prop_search.find(id="propertySearch-results-container")
search_results = container.find(id="l-searchResults")
prop_listings = search_results.find_all('div', class_="l-searchResult is-list")

for prop_listing in prop_listings:
    soupLocation = prop_listing.find('meta', itemprop="streetAddress")
    soupPrice = prop_listing.find("div", class_="propertyCard-priceValue")
    soupID = prop_listing.find('a', "propertyCard-anchor", "id")
    soupID = soupID.attrs['id']



    if soupID not in prop_id:
        prop_location.append(soupLocation['content'])
        prop_price.append(soupPrice.text)
        prop_id.append(soupID)


# Data export to a .CSV file using the Pandas library.
data = {
    "Location": panda_location,
    "Price": prop_price,
    "Type": userSelected_type,
    "rooms": userSelected_rooms,
    "Property ID": prop_id,
}
df = pd.DataFrame.from_dict(data)
df.to_csv(r"TestDataNEW.csv", encoding="utf-8")

