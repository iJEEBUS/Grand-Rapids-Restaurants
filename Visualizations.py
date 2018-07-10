import csv
import pandas
import matplotlib
from ScrapeData import *


file = './RestaurantData.txt'
csvfile = open('RestaurantData.txt', 'rb')

restaurant_data = Scrape()
restaurant_data = Clean(restaurant_data)

data = makeDF(restaurant_data)
