'''

This is a data set generator.
Note that this script is made only for the following website:http://35.192.62.252:8069/shop

'''
import os
import time
import io
import requests
import csv
import selenium
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from PIL import Image
from parsel import Selector 

# Intiallizing a Chrome web-driver.
def create_web_driver():
	global chrome_driver
	current_path = os.getcwd()
	driver_name = "chromedriver"
	driver_path = os.path.join(current_path, driver_name)
	driver_options = webdriver.ChromeOptions()
	chrome_driver = webdriver.Chrome(driver_path, options=driver_options)

# Navigating to the desired search url.
def navigate_to_website(search_url):
	chrome_driver.get(search_url)

	# Set cookies to be able to browse the online shop. 
	chrome_driver.add_cookie({"name": "1P_JAR", "value": "2020-10-01-06"})
	chrome_driver.add_cookie({"name": "visitor_uuid", "value": "25379b1556ae4ac596ff3d7a35166f83"})
	chrome_driver.add_cookie({"name": "frontend_lang", "value": "en_US"})
	chrome_driver.add_cookie({"name": "session_id", "value": "cb459b57dfe49ed30df2c2dab5f74f33c2e8b323"})

	chrome_driver.refresh()

# Scrape items data from page one.
def crawl_items_data_page_one():
	print("page one....")
	global items
	items = []
	items_img_urls_lst = []
	items_names_lst = []
	items_prices_lst = []
	navigate_to_website("http://35.192.62.252:8069/shop")

	# Crawling items image urls.
	items_img_urls = chrome_driver.find_elements_by_xpath("//img[contains(@class, 'img img-fluid')]")
	# Extracting items images url from Selenium objects.
	for i in range(1,21):
		items_img_urls_lst.append(items_img_urls[i].get_attribute('src'))

	# Crawling item's names.
	items_names = chrome_driver.find_elements_by_xpath("//h6[contains(@class, 'o_wsale_products_item_title')]/a")
	# Extracting item's images url from Selenium objects.
	for i in range(0,20):
		items_names_lst.append(items_names[i].get_attribute('innerHTML'))

	# Crawling item's prices.
	items_prices = chrome_driver.find_elements_by_xpath("//span[contains(@class, 'oe_currency_value')]")
	# Extracting item's prices from Selenium objects.
	for i in range(0,40,2):			
		items_prices_lst.append(items_prices[i].get_attribute('innerHTML'))

	# Adding the crawled data in a desired form.
	for i in range(0,20):
		if items_prices_lst[i].find(',') != -1:
			items_prices_lst[i] = items_prices_lst[i].split(',')[0] + items_prices_lst[i].split(',')[1]
		items.append({
			'item_id':i,
			'item_name':items_names_lst[i], 
			'item_img':	items_img_urls_lst[i],
			'item_price': items_prices_lst[i]
		})

# Scrape items data from page two.
def crawl_items_data_page_two():
	print("page two....")
	items_img_urls_lst = []
	items_names_lst = []
	items_prices_lst = []

	# Navigating to page two.
	for i in range(0,8):
		if i == 3:
			chrome_driver.find_elements_by_xpath("//a[contains(@class, 'page-link')]")[i].click()

	# Crawling items prices.
	items_img_urls = chrome_driver.find_elements_by_xpath("//img[contains(@class, 'img img-fluid')]")
	# Extracting items prices from Selenium objects.
	for i in range(1,5):
		items_img_urls_lst.append(items_img_urls[i].get_attribute('src'))

	# Crawling items prices.	
	items_names = chrome_driver.find_elements_by_xpath("//h6[contains(@class, 'o_wsale_products_item_title')]/a")
	# Extracting items prices from Selenium objects.
	for i in range(0,4):
		items_names_lst.append(items_names[i].get_attribute('innerHTML'))

	# Crawling items prices.
	items_prices = chrome_driver.find_elements_by_xpath("//span[contains(@class, 'oe_currency_value')]")
	# Extracting items prices from Selenium objects.
	for i in range(0,8,2):	
		items_prices_lst.append(items_prices[i].get_attribute('innerHTML'))

	# Adding the crawled data in a desired form.
	for i in range(0,4):
		items.append({
			'item_id':i+22,
			'item_name':items_names_lst[i], 
			'item_img':	items_img_urls_lst[i],
			'item_price': items_prices_lst[i]
		})

# Generate the dataset in the desired format.
def create_items_csv():
	with open("items.csv", "w", newline="") as file:
		title = "item_id,item_name,item_img,item_price".split(",")
		writer = csv.DictWriter(file, title, delimiter=';')
		writer.writeheader()
		writer.writerows(items)

def main():
	create_web_driver()
	crawl_items_data_page_one()
	crawl_items_data_page_two()
	create_items_csv()

if __name__ == "__main__":
    main()