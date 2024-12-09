from bs4 import BeautifulSoup
import requests
import time
import json

# Need the path of the local codebook-html file.
path = None #r"C:\Users\snorr\OneDrive\Documents\UiB\Masterfag\Master infovit\Masteroppgave_materiale\diverse\data\2914\2914\Valgundersøkelsen 2021\NSD3134 codebook.html"
HTMLFile = open(path, "r",encoding="utf-8") 
source = HTMLFile.read()

if source:
    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(source, 'html.parser', from_encoding="utf-8")
    
    # Find all divs with the attribute 'data-v-1534d4dd'
    q_divs = soup.select("body > div")
    
    # Initialize an empty dictionary to store the categories and question IDs
    questions_dict = {}

    #print(len(q_divs))
    for div in q_divs:
        spm_id = div.find("h3").get_text()
        title = div.find("div").get_text()
        val_cat_dict = {}
        #table_div = div.find("div", class_="data-table")
        print("Title:")
        print(title)
        tbody = div.find("tbody", class_="codelist")
        if tbody:
            print(tbody)
            rows = tbody.find_all("tr")
        
            for row in rows:
                key = row.find("td", class_="nowrap").get_text()
                value = row.select("td:not(.nowrap)")[0].get_text()
                val_cat_dict[key] = value
        
            questions_dict[spm_id] = {
                "title" : title,
                "category": None,
                "question": None,
                "alternatives": val_cat_dict
                }
    print(questions_dict)
    with open('questions_data.json', 'w', encoding="utf-8") as file:
        json.dump(questions_dict, file, ensure_ascii=False)    

HTMLFile.close()






