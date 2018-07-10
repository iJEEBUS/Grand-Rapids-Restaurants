#!/usr/bin/env python
"""
A script that scrapes, cleans, generates a CSV file, and transforms the restaurant
inspection data of Grand Rapids into a pandas dataframe.
"""
__author__ = 'Ronald Rounsifer'
__version__ = '7.10.2018'
__license__ = 'MIT License'

import re
import csv
import urllib2
import pandas as pd
from bs4 import BeautifulSoup

def Scrape():
	'''
	Scrapes the table data from the 'city-data.com' website for restaurant
	inspections in Grand Rapids, MI
	
	Returns:
		list -- all of the data from the website in an array
	'''
	page = 1
	__URL = "http://www.city-data.com/kent-county-mi-restaurants/index-grand-rapids-" + str(page) + ".html"
	all_data = []
	reformatted_data = []

	# Loop through all 12 pages of Grand Rapids restaurants
	while page < 12:

		# Open and read pages
		content = urllib2.urlopen(__URL).read()
		soup = BeautifulSoup(content, "lxml")

		# Extract only the restaurant data, add to array
		table_data = [tables for tables in soup.find_all("tbody")]
		table_data = table_data[7]
		table_rows = [rows for rows in table_data]
		all_data.append(table_rows)
		page += 1

	# combine arrays from created list into one list
	for array in all_data:
		for data in array:
			if len(data) == 1:
				pass
			else:
				reformatted_data.append(data)

	return reformatted_data

def Clean(data):
	'''
	Cleans the data extracted from the previous scrape before it can be
	converted into a Pandas DataFrame.
	
	Arguments:
		data {list} -- the data to be cleaned
	
	Returns:
		list -- the final cleaned data list
	'''
	first_clean = []
	second_clean = []
	third_clean = []
	final_clean = []

	# Use regex to remove the unwanted tags
	regex = re.compile('(>.*?<)')
	try:
		# create a of list for each restaurant and its data
		for cell in data:
			first_clean.append(cell)

		# create a second list of only useful information
		for cell in first_clean:
			if str(cell) == "<tr>" or str(cell) == "</tr>":
				pass
			else:
				second_clean.append(str(cell))

		# create new list of only needed text in strings
		for cell in second_clean:
			match = regex.findall(cell)
			if match:
				third_clean.append(match)
			else:
				print "not working"

		# drop the > and < characters in each string
		for cell in third_clean:
			for specifics in cell:
				if specifics != '><' and specifics != '>n/a<':
					final_clean.append(specifics[1:-1])

		return final_clean

	except Exception as e:
		print e

def makeDF(data):
	'''
	Generates a pandas DataFrame from the scraped data.

	Arguments:
		data {list} -- the data to input into the DataFrame
	
	Returns:
		pandas.core.frame.DataFrame -- final DataFrame of data
	'''
	headers = ['Name', 'Address', 'City', 'Inspection Date', 'Inspection Score', 'Critical Violations', 'Total Violations']
	temp = []
	final_list = []

	# Split the data into arrays for each restaurant
	for info in range(0, len(data), 7):
		restaurant_data = ', '.join(data[info:info + 7])
		temp.append([restaurant_data])

	# Combines columns if the "The" in some names was separated.
	# Combines the two date columns to look like "Mar 1, 2012"
	for info in temp:
		for token in info:

			# Name fix
			data = token.split(',')
			if len(data) == 9:
				data[0] = data[1].strip() + ' ' + data[0].strip()
				del data[1]

			# Date fix
			data[3] = data[3].strip() + ', ' + data[4].strip()
			del data[4]

			final_list.append(data)
	return pd.DataFrame(final_list, columns=headers)

def makeCSV(data, **directory):
	'''
	Takes the scraped data and generates a text file in the CSV format.
	
	Arguments:
		data {list} -- the data to input into the CSV
		directory {string} -- the absolute path to the file to write
	'''
	# path and strings to enter into the file
	if directory:
		absolute_path = directory + "RestaurantData.txt"
	else:
		absolute_path = "./RestaurantData.txt"
	headers = ['Name', 'Rating', 'Address', 'City', 'Last Inspection', 'Last Score', 'Critical Violations', 'Total Violations']
	with open(absolute_path, 'wb') as file:
		wr = csv.writer(file, quoting=csv.QUOTE_ALL)
		wr.writerow(data)