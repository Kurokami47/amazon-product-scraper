from entity.amazon_product_scraper import AmazonScraper
from logger import logging

if __name__ == "__main__":
    try:
        url = ' https://www.amazon.it/Electrolux-EP81UB25UG-Aspirapolvere-Portatile-accessori/dp/B09C62DKN2/'
        scraper = AmazonScraper(url)
        product_df = scraper.scrape_product_data()
        logging.info("Scraping initiated")

        if product_df is not None:
            logging.info("Scraping Finished Successfully")
            product_df.to_csv('product_df1.csv', index=False)
            logging.info("Product data saved to csv")
            # Use the soup object from the product scrape to get reviews
            reviews_df = scraper.scrape_reviews_from_soup()
            reviews_df.to_csv('reviews_scraped1.csv', index=False)
            logging.info("Reviews data saved to csv")
        else:
            logging.error('Failed to fetch product data.')

    except Exception as e:
        logging.error("An unexpected error occurred:")
        logging.exception(e)
