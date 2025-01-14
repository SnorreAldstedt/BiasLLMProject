from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import copy

driver = webdriver.Chrome()

url = "https://surveybanken.sikt.no/no/study/NSD3134?file=9b4a622d-85a2-4667-9ddf-4e7ac2791941/10&type=studyMetadata"
driver.get(url)

with open('combined_questions.json', encoding="utf-8") as f:
    question_dict = json.load(f)

new_question_dict = copy.deepcopy(question_dict)

# Wait for the content to load (adjust the waiting condition as needed)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "app"))
    )
    time.sleep(3)  # Additional wait time to ensure all content is loaded

    target_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-v-27594830]"))
    )

    # Click the button to reveal the hidden content
    target_button.click()

    #sibling_div = WebDriverWait(driver, 10).until(
    #    EC.presence_of_element_located((By.CSS_SELECTOR, "div#accordion-ub8wjyqaf-content"))
    #)

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser', from_encoding="utf-8")

    for key in new_question_dict.keys():
        target_button = soup.find(
            lambda tag: tag.name == "button" and tag.find("div", string=key) is not None
        )
        print(target_button)
# Use find_next_sibling to get the immediate sibling <div>
        sibling_div = target_button.find_next_sibling("div")

        second_last_div = sibling_div.find("div", class_="p-tiny")
        question_text = second_last_div.find("div").get_text()
        new_question_dict[key]["question"] = question_text

    print(new_question_dict)
finally:
    driver.quit()
