# -*- coding: utf-8 -*-
'''
WARNING: Use this code at your own risk, scraping is against Zillow's TOC.

Zillow home listings scraper, using Selenium.  The code takes as input search 
terms that would normally be entered on the Zillow home page.  It creates 11 
variables on each home listing from the data, saves them to a data frame, 
and then writes the df to a CSV file that gets saved to your working directory.

Software requirements/info:
- This code was written using Python 3.5.
- Scraping is done with Selenium v3.0.2, which can pip installed, or downloaded
  here: http://www.seleniumhq.org/download/
- The selenium package requires a webdriver program. This code was written 
  using Chromedriver v2.25, which can be downloaded here: 
  https://sites.google.com/a/chromium.org/chromedriver/downloads
  
'''

import time
import pandas as pd
import zillow_functions as zl
from bs4 import BeautifulSoup
import numpy as np
from selenium.webdriver.common.by import By
import tax_functions as tx

# Create list of search terms.
# Function zipcodes_list() creates a list of US zip codes that will be 
# passed to the scraper. For example, st = zipcodes_list(["10", "11", "606"])  
# will yield every US zip code that begins with "10", begins with "11", or 
# begins with "606", as a list object.
# I recommend using zip codes, as they seem to be the best option for catching
# as many house listings as possible. If you want to use search terms other 
# than zip codes, simply skip running zipcodes_list() function below, and add 
# a line of code to manually assign values to object st, for example:
# st = ["Chicago", "New Haven, CT", "77005", "Jacksonville, FL"]
# Keep in mind that, for each search term, the number of listings scraped is 
# capped at 520, so in using a search term like "Chicago" the scraper would 
# end up missing most of the results.
# Param st_items can be either a list of zipcode strings, or a single zipcode 
# string.

#st = ["85201"]

# Initialize the webdriver.
driver = zl.init_driver("C:\webdrivers\chromedriver.exe")

# Go to www.zillow.com/homes
zl.navigate_to_website(driver, "http://www.google.com")
print("Enter a zip code")
time.sleep(30.091)


# Initialize list obj that will house all scraped data.
output_data = []

raw_data = zl.get_html(driver)
print("%s pages of listings found" % str(len(raw_data)))

    # Take the extracted HTML and split it up by individual home listings.
listings = zl.get_listings(raw_data)
print("%s home listings scraped\n***" % str(len(listings)))

# For each home listing, extract the 11 variables that will populate that
# specific observation within the output dataframe.

for home in listings:
    new_obs = []
    parser = zl.html_parser(home)

    # Street Address
    address = parser.get_street_address()
    new_obs.append(address)
        
    # City
    new_obs.append(parser.get_city())
        
    # State
    new_obs.append(parser.get_state())
        
    # Zipcode
    new_obs.append(parser.get_zipcode())
        
    # Price
    new_obs.append(parser.get_price())
        
    # Sqft
    new_obs.append(parser.get_sqft())
        
    # Bedrooms
    new_obs.append(parser.get_bedrooms())
        
    # Bathrooms
    new_obs.append(parser.get_bathrooms())
        
    # Days on the Market/Zillow
    new_obs.append(parser.get_days_on_market())
        
    # Sale Type (House for Sale, New Construction, Foreclosure, etc.)
    new_obs.append(parser.get_sale_type())
        
    # URL for each house listing
    url = parser.get_url()
    new_obs.append(url)

    property_tax = tx.get_tax(address)
    new_obs.append(property_tax)

    try:
        zl.navigate_to_website(driver, url)
        time.sleep(5)
        html = driver.page_source
        driver.find_element_by_xpath("//*[text()='Home Value']").click()
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        zestimate_tag = soup.find("div", {"class": "secondary-zestimate-items"}).find("div", {"class": "zestimate-value"})
        if zestimate_tag:
            zestimate = zestimate_tag.text.strip()
        else:
            zestimate = None
    except:
        zestimate = "Capcha'd"
    new_obs.append(zestimate)

    # Append new_obs to list output_data.
    output_data.append(new_obs)

# Close the webdriver connection.
zl.close_connection(driver)

# Write data to data frame, then to CSV file.
file_name = "%s_%s.csv" % (str(time.strftime("%Y-%m-%d")), 
                           str(time.strftime("%H%M%S")))
columns = ["address", "city", "state", "zip", "price", "sqft", "bedrooms", 
           "bathrooms", "days_on_zillow", "sale_type", "url", "property_tax", "zestimate"]
pd.DataFrame(output_data, columns = columns).drop_duplicates().to_csv(
    file_name, index = False, encoding = "UTF-8"
)
