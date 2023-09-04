## Apartment Rental Scraper

Scrape and store apartment rental listings from www.otodom.pl into MySQL and Cassandra databases.

## Features

- **Scrapy Spider**: Efficiently scrapes apartment listings.
- **Dynamic Page Handling**: Uses Selenium to interact with dynamic content.
- **Data Processing**: Cleans and processes scraped data for storage.
- **Optional database loading pipelines:**
  - **MySQL Storage**: Batches and inserts data into a MySQL database.
  - **Cassandra Storage**: Inserts data into a Cassandra database.
 

 **Run the Scrapy spider**:
 
   ```scrapy crawl ApartamentRentSpider```
   
   or
   
   `scrapy crawl ApartamentRentSpider -O scrapddata.csv`
   
   If you want to additionally save data to csv file. 
   

**Activating database pipelines:**

Uncomment:
```
ITEM_PIPELINES = {
    # "ApartamentRentScraper.pipelines.MySQLPipeline" : 301,
    # "ApartamentRentScraper.pipelines.CassandraPipeline" : 302,
}
```
**Configuration** 

Filters and start_ulr:
IF you want to scrape only specific locations, or range prices. Replace url in start_urls with one that has applied filters. (Use the website search filter to get the url)
The scraper as of now is only able to scrape from mieszkanie or kawalerka listing sections.
 
