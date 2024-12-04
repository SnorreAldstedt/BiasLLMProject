import json
import requests
from bs4 import BeautifulSoup

url = "https://surveybanken.sikt.no/no/study/NSD3134/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    category_divs = soup.find_all('div', {'data-v-1534d4dd': True})

    category_dict = {}

    for div in category_divs:
        title = div.find('span', {'data-v-1534d4dd': True})
        if title:
            title_text = title.get_text(strip=True)
            q_divs = div.find_all('div', class_='text-sm xs:text-xs group-hover:text-brand-primary')
            q_ids = [q_div.get_text(strip=True) for q_div in q_divs]

            category_dict[title_text] = q_ids
    
    print(category_dict)
    with open("questions.json", "w") as outfile:
        json.dump(category_dict, outfile)

