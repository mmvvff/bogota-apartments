# Import necessary libraries for browser automation
from selenium.webdriver.chrome.options import Options  # For configuring Chrome browser options
from fake_useragent import UserAgent  # For generating random user agents to avoid detection
from selenium import webdriver  # For browser automation
from datetime import datetime  # For timestamping data
import json  # For parsing JSON responses

# Import Scrapy-specific components
from bogota_lotes.items import ApartmentsItem  # Custom item class for structured data storage
from scrapy.selector import Selector  # For parsing HTML responses
from scrapy.loader import ItemLoader  # For loading data into the item
import scrapy  # Main Scrapy framework
import logging  # For logging events and errors

class MetrocuadradoSpider(scrapy.Spider):
    """
    Spider to scrape apartment data from metrocuadrado.com
    
    This spider extracts detailed information about apartments in Bogotá
    including prices, features, location data, and more from metrocuadrado.com
    """
    name = 'metrocuadrado'  # Unique identifier for the spider
    allowed_domains = ['metrocuadrado.com']  # Restricts crawling to these domains
    base_url = 'https://www.metrocuadrado.com/rest-search/search'  # API endpoint for search results
    logger = logging.getLogger(__name__)  # Initialize logger for this spider

    def __init__(self):
        """
        Initializes the spider with a headless Chrome browser instance
        
        Sets up Chrome with specific options for web scraping:
        - Headless mode (no visible browser)
        - Window size to mimic a real browser
        - Random user agent to avoid detection
        - Disk cache for performance
        """
        # Configure Chrome options for headless operation
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run browser in headless mode (no GUI)
        chrome_options.add_argument('--headless=new')  # Use new headless implementation
        chrome_options.add_argument('--window-size=1920x1080')  # Set window size to avoid responsive design issues
        chrome_options.add_argument(f'user-agent={UserAgent().random}')  # Use random user agent to avoid bot detection
        chrome_options.add_argument('--disk-cache=true')  # Enable disk cache for better performance

        # Initialize Chrome WebDriver with the configured options
        self.driver = webdriver.Chrome(options=chrome_options)

    def start_requests(self):
        """
        Generates the initial requests to scrape apartment data
        
        Creates requests to the API endpoint for both sale and rent listings,
        paginating through results in batches of 50 up to a maximum of 9950 results.
        Each request includes appropriate headers including an API key.
        """
        # Set up headers for API requests
        headers = {
            'X-Api-Key': 'P1MfFHfQMOtL16Zpg36NcntJYCLFm8FqFfudnavl',  # API key for authorization
            'User-Agent': UserAgent().random  # Random user agent to avoid detection
        }

        # Iterate through both property types (sale and rent)
        for type in ['venta', 'arriendo']:
            # Paginate through results in batches of 50
            for offset in range(0, 9950, 50):
                self.logger.info(f'Getting {type} apartments from offset {offset}')
                # Construct URL with proper parameters for filtering apartments in Bogotá
                url = f'{self.base_url}?realEstateTypeList=apartamento&realEstateBusinessList={type}&city=bogot%C3%A1&from={offset}&size=50'

                # Yield a request to the constructed URL
                yield scrapy.Request(url, headers=headers, callback=self.parse)

        
    def parse(self, response):
        """
        Parses the response from the initial requests and generates requests to scrape detailed apartment pages
        
        Extracts apartment listings from the JSON response and creates
        a new request for each individual apartment detail page.
        """
        logging.info('Parsing response')
        # Parse JSON response and extract results array
        result = json.loads(response.body)['results']
        self.logger.info(f'Found {len(result)} apartments')

        # For each apartment in the results, request its detail page
        for item in result:
            yield scrapy.Request(
                url=f'https://metrocuadrado.com{item["link"]}',  # Construct full URL to detail page
                callback=self.details_parse  # Use details_parse method to handle the response
            )

    def details_parse(self, response):
        """
        Parses the response from the apartment detail pages and extracts comprehensive data
        
        Uses Selenium to load the page (necessary for JavaScript content),
        then extracts data from the page's React state stored in a script tag.
        Populates an ApartmentsItem with the extracted data.
        """
        # Load the page with Selenium to render JavaScript content
        self.driver.get(response.url)   
        
        self.logger.info(f'Getting details from {response.url}')

        # Extract the React app state data from __NEXT_DATA__ script tag
        script_data = Selector(text=self.driver.page_source).xpath(
            '//script[@id="__NEXT_DATA__"]/text()'
        ).get()

        # If script data not found, retry with an implicit wait
        if not script_data:
            self.logger.error('No script data found')
            self.driver.get(response.url)
            self.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to load
            script_data = Selector(text=self.driver.page_source).xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        # Parse the JSON data from the script tag
        try:
            script_data = json.loads(script_data)['props']['initialProps']['pageProps']['realEstate']
        except json.JSONDecodeError as e:
            logging.error(f'Error decoding JSON: {e}')

        # Process each apartment item from the script data
        for item in script_data:
            # Initialize an ItemLoader with the ApartmentsItem
            loader = ItemLoader(item=ApartmentsItem(), selector=item)

            # Add all the extracted data to the ItemLoader
            #codigo - Unique identifier for the apartment
            loader.add_value('codigo', script_data['propertyId'])
            
            #tipo_propiedad - Type of property (apartment, house, etc.)
            loader.add_value('tipo_propiedad', script_data['propertyType']['nombre'])
            
            #tipo_operacion - Type of operation (sale, rent)
            loader.add_value('tipo_operacion', script_data['businessType'])
            
            #precio_venta - Sale price
            loader.add_value('precio_venta', script_data['salePrice'])
            
            #precio_arriendo - Rent price
            loader.add_value('precio_arriendo', script_data['rentPrice'])
            
            #area - Area in square meters
            loader.add_value('area', script_data['area'])
            
            #habitaciones - Number of rooms
            loader.add_value('habitaciones', script_data['rooms'])
            
            #banos - Number of bathrooms
            loader.add_value('banos', script_data['bathrooms'])
            
            #administracion - Monthly administration fee
            loader.add_value('administracion', script_data['detail']['adminPrice'])
            
            #parqueaderos - Number of parking spaces
            loader.add_value('parqueaderos', script_data['garages'])
            
            #sector - Neighborhood/sector
            loader.add_value('sector', self.try_get(script_data, ['sector', 'nombre']))
            
            #estrato - Socioeconomic stratum (Colombian classification system)
            loader.add_value('estrato', script_data['stratum'] if 'stratum' in script_data else None)
            
            #antiguedad - Age of the property
            loader.add_value('antiguedad', script_data['builtTime'])
            
            #estado - State of the property (new, used)
            loader.add_value('estado', script_data['propertyState'])
            
            #longitud - Longitude coordinate
            loader.add_value('longitud', script_data['coordinates']['lon'])
            
            #latitud - Latitude coordinate
            loader.add_value('latitud', script_data['coordinates']['lat'])
            
            #featured_interior - Interior features
            loader.add_value('featured_interior', self.try_get(script_data, ['featured', 0, 'items']))
            
            #featured_exterior - Exterior features
            loader.add_value('featured_exterior', self.try_get(script_data, ['featured', 1, 'items']))
            
            #featured_zona_comun - Common area features
            loader.add_value('featured_zona_comun', self.try_get(script_data, ['featured', 2, 'items']))
            
            #featured_sector - Sector/neighborhood features
            loader.add_value('featured_sector', self.try_get(script_data, ['featured', 3, 'items']))
            
            #Imagenes - List of image URLs
            try:
                imagenes = []
                for img in script_data['images']:
                    imagenes.append(img['image'])

                loader.add_value('imagenes', imagenes)
            except:
                pass
                
            #compania - Company or real estate agency listing the property
            loader.add_value('compañia', script_data['companyName'] if 'companyName' in script_data else None)
            
            #descripcion - Full description of the property
            loader.add_value('descripcion', script_data['comment'])
            
            #website - Source website
            loader.add_value('website', 'metrocuadrado.com')
            
            # last_view - Last time the scraper visited this listing
            loader.add_value('last_view', datetime.now())
            
            #datetime - Timestamp of when the data was scraped
            loader.add_value('datetime', datetime.now())

        # Yield the populated item
        yield loader.load_item()

    def try_get(self, dictionary, keys: list):
        """
        Safely accesses nested dictionary or list values by path
        
        Tries to get a value from a nested data structure and returns
        None if the key is not found or if an index is out of range.
        
        Args:
            dictionary: The dictionary or list to extract value from
            keys: A list representing the path to the desired value
            
        Returns:
            The value at the specified path or None if not found
        """
        try:
            value = dictionary
            for key in keys:
                if isinstance(value, list) and isinstance(key, int) and 0 <= key < len(value):
                    # If value is a list and key is a valid index, get the value at that index
                    value = value[key]
                elif isinstance(value, dict) and key in value:
                    # If value is a dict and key is present, get the value for that key
                    value = value[key]
                else:
                    # Key or index is not valid
                    return None
            return value
        except (KeyError, TypeError, IndexError):
            # Handle any exceptions that might occur during lookup
            return None