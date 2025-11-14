
import os
from base import Base
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

class GetPageContent(Base):
    
    def __init__(self, *args ,**kwargs):
        super().__init__(*args, **kwargs)

    def load_urls(self, file_name):
        self.path = os.path.join(os.getcwd(), '../data/raw/', file_name)
        if not os.path.exists(self.path):
            print("Please get links first...!")
            exit()

        with open(self.path, 'r') as file:
            urls = file.read()
            self.urls = urls.split('\n')
    
    @property
    def property_id(self):
        match = self.url.split('-')[-1].replace("/","")
        return match if match else None

    @property
    def address(self):
        tag = self.soup.find('h1') or self.soup.find('span', class_='property-header__title')
        return tag.get_text().split(",") if tag else None

    @property
    def property_type(self):
        tag = self.soup.select_one("div.sc-12iqlu8-2")
        return tag.get_text(strip=True) if tag else None

    @property
    def price_aud(self):
        tag = self.soup.find(text=re.compile(r'AUD\s*\$\s*[\d,]+', re.I))
        return tag if tag else None

    @property
    def price_usd(self):
        tag = self.soup.find(text=re.compile(r'USD\s*\$\s*[\d,]+', re.I))
        return tag

    @property
    def published_date(self):
        tag = self.soup.select_one('div.data > div')
        return tag.get_text(strip=True) if tag else None

    @property
    def last_update_date(self):
        tag = self.soup.select_one('div.data > div')
        try:
            second_div = tag.find_next_sibling('div')
        except:
            second_div = None
        return second_div.get_text(strip=True) if second_div else None

    @property
    def building_size(self):
        tag = self.soup.select_one("div.sc-12iqlu8-2 > span")
        return tag.get_text(strip=True) if tag else None

    @property
    def bedrooms(self):
        tag = self.soup.select_one("div.rooms > div.sc-12iqlu8-2")
        if tag and (text := tag.get_text(strip=True)):
            try:
                bedroom_text = text.split(",")[0].strip()
                return bedroom_text
            except:
                return None
        return None

    @property
    def bathrooms(self):
        tag = self.soup.select_one("div.rooms > div.sc-12iqlu8-2")
        if tag and (text := tag.get_text(strip=True)):
            bedroom_text = text.split(",")[1].strip()
            return bedroom_text
        return None

    @property
    def parking_spaces(self):
        tag = self.soup.select_one("div.parkingSpaces > div.sc-12iqlu8-2")
        if tag and (text := tag.get_text(strip=True)):
            spaces = text.split(",")[0].strip()
            return spaces
        return None

    # ---------------- Features ----------------
    @property
    def features(self):
        feature_tags = self.soup.select('div.feature > span')
        if not feature_tags:
            return None
        feature_list = [f.get_text(strip=True) for f in feature_tags if f.get_text(strip=True)]
        return feature_list if feature_list else None

    # ---------------- Agent info ----------------
    @property
    def agent_name(self):
        tag = self.soup.select_one('.agent-name')
        return tag.get_text(strip=True) if tag else None

    @property
    def agency(self):
        tag = self.soup.select_one('.agency-name')
        return tag.get_text(strip=True) if tag else None

    @property
    def agent_phone(self):
        tag = self.soup.select_one('div.yy9d2l-0 > a')
        if tag:
            tag = tag.get("href").replace("tel:", "")
            return tag
        return None

    @property
    def agent_email(self):
        tag = self.soup.select_one('a.agent-email')
        return tag.get('href').replace('mailto:', '') if tag else None

    # ---------------- Description ----------------
    @property
    def description(self):
        tag = self.soup.select_one('.property-description')
        return tag.get_text(strip=True) if tag else None

    # ---------------- Images ----------------
    @property
    def images(self):
        tags = self.soup.select('.media-gallery img')
        return [t.get('src') for t in tags if t.get('src')] if tags else None

    # ---------------- Similar properties ----------------
    @property
    def similar_properties(self):
        props = []
        tags = self.soup.select('.similar-properties a')
        for t in tags:
            link = t.get('href')
            title = t.get_text(strip=True)
            if link:
                props.append({'title': title, 'url': link})
        
        if props:
            return props
        return None

    # ---------------- All data ----------------
    def get_all_data(self):
        return {
            'propertyID': self.property_id,
            'address': self.address,
            'propertyType': self.property_type,
            'priceAUD': self.price_aud,
            'priceUSD': self.price_usd,
            'publishedDate': self.published_date,
            'lastUpdateDate': self.last_update_date,
            'buildingSize': self.building_size,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'parkingSpaces': self.parking_spaces,
            'features': self.features,
            'agentName': self.agent_name,
            'agency': self.agency,
            'agentPhone': self.agent_phone,
            'agentEmail': self.agent_email,
            'description': self.description,
        }


    def fetch_content(self, storage=True):
        self.load_urls(file_name=self.fetch_contents)
        all_data = []
        print(f"Start Crawling {len(self.urls)} URL")
        
        for url in self.urls:
            try:
                self.url = url
                html = self.get_html
                if html is None:
                    continue

                self.soup = BeautifulSoup(html, 'html.parser')
                data = self.get_all_data()
                
                for key, value in data.items():
                    if isinstance(value, list) or isinstance(value, dict):
                        data[key] = json.dumps(value)  
                    elif value is None:
                        data[key] = None
                all_data.append(data)
            except:
                continue
            
        df = pd.DataFrame(all_data, columns=data.keys())
        path = self.path[:-4] + '.csv'
        df.to_csv(path, index=False)

