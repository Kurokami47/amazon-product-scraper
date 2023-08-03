Since amazon was only accepting a few number of requests from the same ip address i used a reattemping logic so it retries till
the access to site is provided so the scraping time can vary a bit.


Amazon Product Scraper

This is a Python script to scrape product data and reviews from an Amazon product page using the AmazonScraper class. 
It uses the requests, beautifulsoup4, and pandas libraries for web scraping and data manipulation.


How to Use

Make sure you have installed the required packages listed in requirements.txt. You can install them using:
pip install -r requirements.txt


Import the AmazonScraper class from entity.amazon_product_scraper and the logging module.

Initialize the AmazonScraper with the desired product URL.

Use the scrape_product_data() method to scrape product details (title, price, and description) and save the data to a 
CSV file.

Use the scrape_reviews_from_soup() method to scrape the product reviews and save them to a separate CSV file.