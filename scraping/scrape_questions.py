from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

driver = webdriver.Chrome()

url = "https://surveybanken.sikt.no/no/study/NSD3134?file=9b4a622d-85a2-4667-9ddf-4e7ac2791941/10&type=studyMetadata"
driver.get(url)

# Wait for the content to load (adjust the waiting condition as needed)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "app"))
    )
    time.sleep(3)  # Additional wait time to ensure all content is loaded

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser', from_encoding="utf-8")
    
    # Find all divs with the attribute 'data-v-1534d4dd'
    category_divs = soup.find_all('div', {'data-v-1534d4dd': True})
    
    # Initialize an empty dictionary to store the categories and question IDs
    categories_dict = {}
    
      # Loop through each category div
    for category_div in category_divs:
        # Extract the category title from the first span with 'data-v-1534d4dd'
        category_title = category_div.find('span', {'data-v-1534d4dd': True})
        
        if category_title:
            category_title_text = category_title.get_text(strip=True)
            
            # Find all question ID divs within the current category div
            #print(category_div)
            question_id_divs = category_div.find_all('div', class_='text-sm xs:text-xs group-hover:text-brand-primary')
            print(category_title_text)
            print(question_id_divs)
            # Extract the text from each question ID div
            question_ids = [qid_div.get_text(strip=True) for qid_div in question_id_divs]

            # Add the category and its question IDs to the dictionary
            if category_title_text in categories_dict:
                categories_dict[category_title_text] += question_ids
            else:
                categories_dict[category_title_text] = question_ids


    print(categories_dict)
    with open('questions.json', 'w', encoding="utf-8") as file:
        json.dump(categories_dict, file, ensure_ascii=False)

finally:
    driver.quit()


    
