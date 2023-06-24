'''

This is a data set generator.
Note that this script is made only for the following website:

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

SEARCH_URL = "https://baghyra.com/product-category/women/" 

#Intiallizing a Chrome web-driver.
def create_web_driver():
	global chrome_driver
	current_path = os.getcwd()
	driver_name = "chromedriver"
	driver_path = os.path.join(current_path, driver_name)
	driver_options = webdriver.ChromeOptions()
	chrome_driver = webdriver.Chrome(driver_path, options=driver_options)

# Generating the dataset in the desired format.
def create_csv_file(items):
	with open("baghyra_items.csv", "w", newline="", encoding='utf-8') as file:
		title = "item_id,item_name,item_img,item_price,category_id".split(",")
		writer = csv.DictWriter(file, title, delimiter=';')
		writer.writeheader()
		writer.writerows(items)

def main():
	items_imgs_url = []
	items_imgs_url_lst = []
	items_names_lst = []
	items_prices = []
	items_names = []
	items = []

	# Creating a Chrome web driver.
	create_web_driver()
	# Getting the desired page source (HMTL) of the search url.
	chrome_driver.get(SEARCH_URL)

	# Loading all items.
	for i in range(0, 3):
		chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(20)

	# Get item's images url.
	items_imgs_url_lst = chrome_driver.find_elements_by_xpath("//div[contains(@class, 'product-element-top')]/a/img")
	for i in range(0,len(items_imgs_url_lst)):
		if str(items_imgs_url_lst[i].get_attribute('data-src')) == 'None':
			items_imgs_url.append(items_imgs_url_lst[i].get_attribute('src'))
		else:
			items_imgs_url.append(items_imgs_url_lst[i].get_attribute('data-src'))

	# Get item's names.
	items_names_lst = chrome_driver.find_elements_by_xpath("//h3[contains(@class, 'product-title')]/a")
	for i in range(0,len(items_names_lst)):
		items_names.append(items_names_lst[i].get_attribute('innerHTML'))

	# Get item's prices	
	items_prices_lst = chrome_driver.find_elements_by_xpath("//div[contains(@class, 'swap-elements')]")
	for i in range(0,len(items_prices_lst)):
		if items_prices_lst[i].get_attribute('outerHTML').find("<ins>") > 0:
			if items_prices_lst[i].get_attribute('outerHTML').split('>EGP</span>')[2][0:6].find(',') > 0:
				price = items_prices_lst[i].get_attribute('outerHTML').split('>EGP</span>')[2][0:6].split(',')
				items_prices.append(price[0] + price[1])
			else:
				items_prices.append(items_prices_lst[i].get_attribute('outerHTML').split('>EGP</span>')[2][0:6])
		elif items_prices_lst[i].get_attribute('outerHTML').find("Read more about “Givenchy Ange Ou Etrange”") > 0:
			items_prices.append("no price")
		else:
			if items_prices_lst[i].get_attribute('outerHTML').split('>EGP</span>')[1][0:5].find(',') > 0:
				price = items_prices_lst[i].get_attribute('outerHTML').split('>EGP</span>')[1][0:5].split(',')
				items_prices.append(price[0] + price[1])
			else:
				items_prices.append(items_prices_lst[i].get_attribute('outerHTML').split('>EGP</span>')[1][0:5])
				
	# Merge all data in one array.			
	for i in range(0,73):
		items.append({
			'item_id':i,
			'item_name':items_names[i], 
			'item_img':	items_imgs_url[i],
			'item_price': items_prices[i],
			'category_id':0
		})
	# Creating the data set csv file.
	create_csv_file(items)
	
if __name__ == '__main__':
	main()
			

