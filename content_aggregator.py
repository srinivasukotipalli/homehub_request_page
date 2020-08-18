import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import ast
import os
from urllib.request import Request, urlopen

# For ignoring SSL certificate errors

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Input from user

url = input('Enter Zillow House Listing Url- ')

# Making the website believe that you are accessing it using a mozilla browser

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

# Creating a BeautifulSoup object of the html page for easy extraction of data.

soup = BeautifulSoup(webpage, 'html.parser')
html = soup.prettify('utf-8')
property_json = {}
property_json['Details_Broad'] = {}
property_json['Address'] = {}

# Extract Title of the property listing

for title in soup.findAll('title'):
    property_json['Title'] = title.text.strip()
    break

for meta in soup.findAll('meta', attrs={'name': 'description'}):
    property_json['Detail_Short'] = meta['content'].strip()

for div in soup.findAll('div', attrs={'class': 'character-count-truncated'}):
    property_json['Details_Broad']['Description'] = div.text.strip()

for (i, script) in enumerate(soup.findAll('script',attrs={'type': 'application/ld+json'})):
    if i == 0:
        json_data = json.loads(script.text)
        property_json['Details_Broad']['Number of Rooms'] = json_data['numberOfRooms']
        property_json['Details_Broad']['Floor Size (in sqft)'] = json_data['floorSize']['value']
        property_json['Address']['Street'] = json_data['address']['streetAddress']
        property_json['Address']['Locality'] = json_data['address']['addressLocality']
        property_json['Address']['Region'] = json_data['address']['addressRegion']
        property_json['Address']['Postal Code'] = json_data['address']['postalCode']

    if i == 1:
        json_data = json.loads(script.text)
        property_json['Price in $'] = json_data['offers']['price']
        property_json['Image'] = json_data['image']
    break

with open('data.json', 'w') as outfile:
    json.dump(property_json, outfile, indent=4)

with open('output_file.html', 'wb') as file:
    file.write(html)

print ('———-Extraction of data is complete. Check json file.———-')


# CODE EXPLAINATION:

# In this code, we first hit the URL given and capture the entire HTML which we convert into beautiful soup object.
# Once that is done, we extract specific divs, scripts, titles, and other tags with specific attributes.
# This way we are able to pinpoint specific information that we may want to extract from a page.
# You can see that we have also extracted an image link for each property.
# This has been done deliberately since for something like real estate, images are just as much value as other information.
# While we have indeed extracted several fields from the real estate listing pages,
# it is to be noted that the HTML page does contain many more data points.
# Hence we are also saving the HTML content locally so that you can go through it and crawl more information.


# Some of the house listings that we scraped :

# Like we mentioned before, we actually scraped a few property listings for you to show you how the scraped data would
# look in JSON format. Also, we have mentioned the property for which a particular JSON is,
# under the JSON. Now let’s talk about the data points that we scraped.

# We got an image of the property (although many images for each property is available on a listing page,
# we got one for each- that is the top image for each listing). We also got the price (in $) that it is listed at,
# the title for the property, and a description of it that would help you create a mental picture of the property.

# Along with this, we scraped the address, broken down into four separate parts: the street, the locality,
# the region, and the postal code. We have another details field that has multiple subfields,
# such as the number of rooms, the floor size, and a long description.
# In certain cases, the description is missing as we found out once we scraped multiple pages.

# [code language=”python”] {
# "Details_Broad": {
# "Number of Rooms": 4,
# "Floor Size (in sqft)": "1,728"
# },
# "Address": {
# "Street": "638 Grant Ave",
# "Locality": "North baldwin",
# "Region": "NY",
# "Postal Code": "11510"
# },
# "Title": "638 Grant Ave, North Baldwin, NY 11510 | MLS #3137924 | Zillow",
# "Detail_Short": "638 Grant Ave , North baldwin, NY 11510-1332 is a single-family home listed for-sale at $299,000. The 1,728 sq. ft. home is a 4 bed, 2.0 bath property. Find 31 photos of the 638 Grant Ave home on Zillow. View more property details, sales history and Zestimate data on Zillow. MLS # 3137924",
# "Price in $": 299000,
# "Image": "https://photos.zillowstatic.com/p_h/ISzz1p7wk4ktye1000000000.jpg"
# }
# [/code] [code language=”python”] {
# "Details_Broad": {
# "Description": "Three dormer single family home situated in Arlington’s Brattle neighborhood between Arlington Heights and Arlington Center. Built in the 1920s this home offers beautiful period details, hard wood floors, beamed ceilings, fireplaced living room with private sunroom, a formal dining room, three large bedrooms, an office and two full baths. The potential of enhancing this property to expand living space and personalize to your personal taste is exceptional. Close to Minuteman Commuter Bikeway, Rt 77 and 79 Bus lines, schools, shopping and restaurants. Virtual staging and virtual renovation photos provided to help you visualize.",
# "Number of Rooms": 4,
# "Floor Size (in sqft)": "2,224"
# },
# "Address": {
# "Street": "10 Walnut St",
# "Locality": "Arlington",
# "Region": "MA",
# "Postal Code": "02476"
# },
# "Title": "10 Walnut St, Arlington, MA 02476 | MLS #72515880 | Zillow",
# "Detail_Short": "10 Walnut St , Arlington, MA 02476-6116 is a single-family home listed for-sale at $725,000. The 2,224 sq. ft. home is a 4 bed, 2.0 bath property. Find 34 photos of the 10 Walnut St home on Zillow. View more property details, sales history and Zestimate data on Zillow. MLS # 72515880",
# "Price in $": 725000,
# "Image": "https://photos.zillowstatic.com/p_h/ISifzwig3xt2re1000000000.jpg"
# }
# [/code] [code language=”python”] {
# "Details_Broad": {
# "Number of Rooms": 4,
# "Floor Size (in sqft)": "1,728"
# },
# "Address": {
# "Street": "638 Grant Ave",
# "Locality": "North baldwin",
# "Region": "NY",
# "Postal Code": "11510"
# },
# "Title": "638 Grant Ave, North Baldwin, NY 11510 | MLS #3137924 | Zillow",
# "Detail_Short": "638 Grant Ave , North baldwin, NY 11510-1332 is a single-family home listed for-sale at $299,000. The 1,728 sq. ft. home is a 4 bed, 2.0 bath property. Find 31 photos of the 638 Grant Ave home on Zillow. View more property details, sales history and Zestimate data on Zillow. MLS # 3137924",
# "Price in $": 299000,
# "Image": "https://photos.zillowstatic.com/p_h/ISzz1p7wk4ktye1000000000.jpg"
# }
