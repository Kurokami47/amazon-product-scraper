import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from logger import logging

class AmazonScraper:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }
        self.soup = None  # Initialize the soup attribute

    def _create_dataframe(self, product_title, price, description):
        data = {
            'Title': [product_title],
            'Price': [price],
            'Description': [description]
        }
        df = pd.DataFrame(data)
        return df

    def scrape_product_data(self):
        MAX_RETRIES = 5
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(self.url, headers=self.headers)
                response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                self.soup = BeautifulSoup(response.text, 'html.parser')  # Store the soup object as an attribute
                element = self.soup.find('span', class_='a-size-large product-title-word-break', id='productTitle')
                # Extract the text content
                if element:
                    logging.info('product elements found')
                    
                    #save the soup if required to check errors

                    # html = soup.prettify("utf-8")
                    # with open("mydemo.html", "wb") as file:
                    #     file.write(html)
                    price_element = self.soup.find("span", class_="a-offscreen")
                    description_element = self.soup.find("ul", class_="a-unordered-list a-vertical a-spacing-mini")

                    product_title = element.text.strip()
                    price = price_element.text.strip()
                    price = price.replace(',','.') #use if the amount is in pounds as they have used ',' to represent fractions on website

                    description = description_element.text.strip()
                    description = description.replace("\n", "")
                    description = description.replace("    ", " ")
                    description = description.replace("***", "")
                    df = self._create_dataframe(product_title, price, description)
                    return df

                else:
                    logging.error('Element not found. Retrying...')
                    time.sleep(5)  # Wait for a few seconds before retrying
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching data: {e}")
                if attempt < MAX_RETRIES - 1:
                    logging.error("Retrying...")
                    time.sleep(5)  # Wait for a few seconds before retrying
                else:
                    logging.error("Max retries reached. Unable to fetch data.")
                    return None

    def scrape_reviews_from_soup(self):
        if self.soup is None:
            logging.error("Error: Soup not found. Please run scrape_product_data() first.")
            return None

        # Find all review blocks with data-hook="review" class
        review_blocks = self.soup.find_all('div', {'data-hook': 'review'})

        # Create a list to store the segregated review data as dictionaries
        segregated_reviews = []

        # Extract the name, rating, and review from each review block
        for review_block in review_blocks:
            name = review_block.find('span', {'class': 'a-profile-name'}).get_text(strip=True)
            rating = review_block.find('span', {'class': 'a-icon-alt'}).get_text(strip=True).split()[0]

            review_text = review_block.find('span', {'data-hook': 'review-body'}).get_text(strip=True)
            # Remove the "Verified Purchase" part and the leading "Reviewed in Country on Date" part
            review_text = review_text.replace('Verified Purchase', '').split('Reviewed in ')[0].strip()
            
            # Remove the "Read more" part from the end of the review text
            review_text = review_text.split('Read more')[0].strip()

            review_data = {
                'Name': name,
                'Rating': rating,
                'Review': review_text
            }

            segregated_reviews.append(review_data)

            # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(segregated_reviews)

        return df