import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


addresses = ['9766 E Friess Dr, Scottsdale, AZ 85260',
             '16230 N 99th Way, Scottsdale, AZ 85260',
             '13048 N Hayden Rd, Scottsdale, AZ 85260',
             '16801 N 94th St APT 1011, Scottsdale, AZ 85260']


def get_tax(address):
    driver = webdriver.Chrome(executable_path="C:\webdrivers\chromedriver.exe")
    driver.wait = WebDriverWait(driver, 10)

    driver.get("https://mcassessor.maricopa.gov/")

    if not isinstance(address, str):
        address = str(address)
    address = address.strip()
    try:
        search_bar = driver.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "homeSearchField")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "homeSearchBtn")))
        search_bar.clear()
        time.sleep(6.32167)
        search_bar.send_keys(address)
        time.sleep(3.871534)
        button.click()
        time.sleep(10.98987)

        driver.find_element_by_xpath("//a[@title='View parcel details.']").click()
        time.sleep(10)
        tax_page_url = driver.find_element_by_id("taxes-button").get_attribute("href")
        driver.get(tax_page_url)

        #  site attempted to 'confuse' scraper by using two different ways to display property tax, lol.
        if len(driver.find_elements_by_id("cphMainContent_cphRightColumn_taxDue1")) != 0:
            tax = driver.find_element_by_xpath(
                '//table[@id="cphMainContent_cphRightColumn_taxDue1"]//td[2]').text.strip()
        else:
            tax = driver.find_element_by_xpath(
                '//ul[@id="cphMainContent_cphRightColumn_taxDue2"]//li[2]').text.strip()

    except:
        print("Property Tax for that address not found. Try manual query")
        return None

    driver.quit()
    return tax
