# Author: Erik Garcia (@erik172)
# Version: Unreleased

# Import datetime for timestamping the pipeline execution
from datetime import datetime
# Import subprocess to run external commands (like Scrapy crawl)
import subprocess
# Import logging to track progress and errors during execution
import logging

# Define log file path with descriptive name
filename = f'logs/data_pipeline.log'

# Configure logging to write to file with timestamps and log levels
# This helps in debugging and monitoring the pipeline execution
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename=filename)

def run_data_pipeline():
    """
    Main function that orchestrates the complete data pipeline:
    1. Web scraping data from HABI and METROCUADRADO
    2. Processing and transforming the scraped data
    3. Saving the processed data to MongoDB
    """
    # Log the pipeline start time for tracking execution duration
    logging.info(f'Start data pipeline at {datetime.now()}')

    # ---- WEB SCRAPING PHASE ----
    # Log the start of HABI scraping process
    logging.info('Start web scraping HABI')
    # Run the HABI spider using Scrapy's crawl command
    # This will extract apartment data from habi.co
    subprocess.run(['scrapy', 'crawl', 'habi'])
    
    # Log the start of METROCUADRADO scraping process
    logging.info('Start web scraping METROCUADRADO')
    # Run the METROCUADRADO spider using Scrapy's crawl command
    # This will extract apartment data from metrocuadrado.com
    subprocess.run(['scrapy', 'crawl', 'metrocuadrado'])
    
    # Log completion of web scraping phase
    logging.info('End web scraping')

    # ---- DATA PROCESSING PHASE ----
    # Log the start of data processing
    logging.info('Start data processing')
    
    # Run initial transformations script
    # This script connects to MongoDB, retrieves data, and performs basic transformations
    # such as exploding images and extracting features from apartment characteristics
    subprocess.run(['python3.11', 'ETL/01_initial_transformations.py'])
    
    # Run data correction script
    # This script performs geographical data correction and enrichment
    # including adding/correcting locality and neighborhood information
    subprocess.run(['python3.11', 'ETL/02_data_correction.py'])
    
    # Run data enrichment script
    # This script adds additional information like nearby TransMilenio stations 
    # and parks, with calculated distances
    subprocess.run(['python3.11', 'ETL/03_data_enrichment.py'])
    
    # Log completion of data processing phase
    logging.info('End data processing')

    # ---- DATA SAVING PHASE ----
    # Log the start of data saving process
    logging.info('Start data saving')
    # Run the data saving script which stores processed data back to MongoDB
    # in the processed collection
    subprocess.run(['python3.11', 'ETL/04_data_save.py'])
    # Log completion of data saving phase
    logging.info('End data saving')

    # Log the pipeline end time to track total execution duration
    logging.info(f'End data pipeline at {datetime.now()}')

# Standard Python idiom to allow the file to be imported or run directly
if __name__ == '__main__':
    # Execute the data pipeline when this script is run directly
    run_data_pipeline()