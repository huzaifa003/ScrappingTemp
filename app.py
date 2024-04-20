from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import webdriver_manager
import webdriver_manager.chrome 
app = Flask(__name__)

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def initialize_driver():
    # Configure ChromeOptions with desired arguments
    
    chrome_options = webdriver.ChromeOptions()
    user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    chrome_options.add_argument(f"user-agent={user_agent_string}")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--enable-logging=stderr")
    chrome_options.add_argument("--v=1")

    # chrome_options.add_argument("--user-data-dir=/abc/profile")

    # Initialize ChromeDriver using ChromeDriverManager to handle driver installation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


# Initialize drivers and set global variables
driver1 = initialize_driver()
driver2 = initialize_driver()

# # Example usage of the initialized drivers
# driver1.get('https://www.facebook.com')
# print("Title of Page 1:", driver1.title)

# driver2.get('https://www.google.com')
# print("Title of Page 2:", driver2.title)



# Example scraping logic, replace with actual scraping logic
driver1.get("https://www.investing.com/crypto/bitcoin/technical")
print(driver1.title)
driver2.get("https://www.tradingview.com/symbols/BTCUSD/technicals/?exchange=CRYPTO")
    
# Global variables to store scraped data
dict1 = {}
dict2 = {}

matching_values = {}


@app.route("/", methods=['GET'])
def home():
    return "Hello, World From Scrapping Server!"
@app.route('/scrape', methods=['GET'])
def scrape():
    # This function will be called when the user makes a GET request to '/scrape'
    scrape_both(driver1, driver2)
    return jsonify({
        'dict1': dict1,
        'dict2': dict2,
        'matching_values': matching_values
    })

def scrape_both(driver1, driver):
    # Clear previous data
    dict1.clear()
    dict2.clear()
    matching_values.clear()
    


    # Replace with the actual URL where the tables are located
    # driver.get("https://www.tradingview.com/symbols/BTCUSD/technicals/?exchange=CRYPTO")
    driver.find_element(By.ID, "1m").click()

    # Replace with the actual URL where the tables are located
    # driver1.get("https://www.investing.com/crypto/bitcoin/technical")
    # driver1.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    print(driver1.title)
    button = driver1.execute_script('return document.querySelector("[data-test=\'1m\']");')
    # dynamic_table_body = WebDriverWait(driver1, timeout=50).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, '.datatable_body__tb4jX'))
    # )
    

	# You can now interact with 'element' as a Selenium WebElement object
	# For example, to get text from the element:from selenium.webdriver.common.action_chains import ActionChains
    #WebDriverWait(driver,50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > div.desktop\:relative.desktop\:bg-background-default > div.relative.flex > div.grid.flex-1.grid-cols-1.px-4.pt-5.font-sans-v2.text-\[\#232526\].antialiased.xl\:container.sm\:px-6.md\:grid-cols-\[1fr_72px\].md\:gap-6.md\:px-7.md\:pt-10.md2\:grid-cols-\[1fr_420px\].md2\:gap-8.md2\:px-8.xl\:mx-auto > div.min-w-0 > div:nth-child(5) > div > div.mb-14.md\:mb-16 > div > button.relative.inline-flex.items-center.justify-center.whitespace-nowrap.rounded-sm.p-1\.5.text-xs.font-bold.leading-tight.text-primary.no-underline.disabled\:text-disabled.text-xs.text-v2-gray-dark.bg-v2-gray-light-2.py-2.px-4.\!rounded-\[3px\].ml-2.first\:ml-0.\!text-v2-blue.\!bg-v2-blue-dark')))
    #target_button = WebDriverWait(driver, 50).until(
     #   EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="1m"]')))
    if button:
        actions = ActionChains(driver1)
        actions.move_to_element(button).click().perform()
    
       
    simple_keys_dict1 = {
        'Relative Strength Index (14)': 'RSI(14)', 
        'Commodity Channel Index (20)': 'CCI(14)', 
        'Average Directional Index (14)': 'ADX(14)', 
        'Stochastic RSI Fast (3, 3, 14, 14)': 'STOCHRSI(14)', 
        'Williams Percent Range (14)': 'Williams %R', 
        'Bull Bear Power': 'Bull/Bear Power(13)', 
        'Ultimate Oscillator (7, 14, 28)': 'Ultimate Oscillator', 
        'Simple Moving Average (10)': 'MA10', 
        'Simple Moving Average (20)': 'MA20', 
        'Simple Moving Average (50)': 'MA50'
    }


    vals_to_get_1 = ['Relative Strength Index (14)', 'Commodity Channel Index (20)', 'Average Directional Index (14)', 'Stochastic RSI Fast (3, 3, 14, 14)', 'Williams Percent Range (14)', 'Ultimate Oscillator (7, 14, 28)', 'Bull Bear Power', 'Simple Moving Average (10)', 'Simple Moving Average (20)', 'Simple Moving Average (50)' ]
    
    vals_to_get_2 = ['RSI(14)', 'CCI(14)', 'ADX(14)', 'STOCHRSI(14)', 'Williams %R', 'Ultimate Oscillator', 'Bull/Bear Power(13)', 'MA10', 'MA20', 'MA50']
    

    
    tables_trading = driver.find_elements(By.CLASS_NAME, "table-hvDpy38G")[:2]

    # Iterate through each table
    for table_index, table in enumerate(tables_trading, start=1):
        # print(f"Table {table_index}:")

        # Find all rows in this table
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Iterate through each row
        for row in rows:
            # Find all cells within this row
            cells = row.find_elements(By.TAG_NAME, "td")

            # Extract and print the text from each cell
            cell_texts = [cell.text for cell in cells]
            

            if(len(cell_texts) > 0):
                if (cell_texts[0] in vals_to_get_1):
                    dict1[cell_texts[0]] = cell_texts[2]
    

        # print("----- End of Table -----")


    print(dict1)
    print("------------ TradingView.com Ended--------------")
    WebDriverWait(driver1, timeout=50).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div[1]/div[2]/div/div/div[2]'))
    )
    technical_pass = driver1.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div[1]/div[3]/div/div/div[2]')
    moving_pass = driver1.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div[1]/div[2]/div/div/div[2]')

    # print(technical_pass.text, moving_pass.text)
    # Find all tables by class name
    # Use WebDriverWait to wait for the tables with class 'datatable_body__tb4jX' to appear
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary
    # Wait for the tbody within the dynamic table to be present
    dynamic_table_body = WebDriverWait(driver1, timeout = 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.datatable_body__tb4jX'))
    )

    # Now that the div is loaded, find the first two tables within this div
    tables= driver1.find_elements(By.CSS_SELECTOR, ".datatable_body__tb4jX")[3:5]  # Adjust if you want more tables
    # print(tables)

    dynamic_table_body = WebDriverWait(driver1, timeout=50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.datatable_body__tb4jX'))
    )

    tables= driver1.find_elements(By.CSS_SELECTOR, ".datatable_body__tb4jX")[3:5]  # Adjust if you want more tables
    # Iterate through the first two tables
    for table_index, table in enumerate(tables, start=1):
        # print(f"Table {table_index}:")

        # Find all rows in this table
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Iterate through each row
        for row in rows:
            # Find all cells within this row
            cells = row.find_elements(By.TAG_NAME, "td")
            
            # Extract and print the text from each cell
            cell_texts = [cell.text for cell in cells]
            if (cell_texts[0] in vals_to_get_2):
                dict2[cell_texts[0]] = cell_texts[2]
        

        # print("----- End of Table -----")
    
    for key1, key2 in simple_keys_dict1.items():
        if key2 in dict2 and dict1[key1] == dict2[key2]:
            matching_values[key2] = dict1[key1]
    
    print(dict2)

    print("------------ Investing.com Ended--------------")
    print(matching_values)
    print("------------ SAME VALUES ENDED --------------")
    

    # Simulate scraping into dict1 and dict2
    dict1['key'] = 'value from driver1'
    dict2['key'] = 'value from driver2'
    if dict1['key'] == dict2['key']:
        matching_values['key'] = dict1['key']

if __name__ == '__main__':
    app.run(debug=True)
