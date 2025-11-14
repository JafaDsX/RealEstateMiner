
import os
from base import Base
from bs4 import BeautifulSoup
import re
import pandas as pd

class GetPageContent(Base):
    
    def __init__(self, *args ,**kwargs):
        super().__init__(*args, **kwargs)

    def load_urls(self, country_code):
        file_name = f'{country_code}-advertise-urls.txt'
        path = os.path.join(os.getcwd(), '../data/raw/', file_name)
        print(path)
        if not os.path.exists(path):
            print("Please get links first...!")
            exit()

        with open(path, 'r') as file:
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
        tag = self.soup.find(text=re.compile(r'(Unit|House|Apartment|Villa|Townhouse)', re.I))
        tag = tag.split(",")
        return tag if tag else None

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
        tag = self.soup.find('span', class_='property-published-date')
        return tag.get_text(strip=True) if tag else None

    @property
    def last_update_date(self):
        tag = self.soup.find('span', class_='property-last-updated')
        return tag.get_text(strip=True) if tag else None

    @property
    def building_size(self):
        tag = self.soup.find(text=re.compile(r'\d+\s*m²|\d+\s*sq\.ft', re.I))
        return tag.strip() if tag else None

    @property
    def bedrooms(self):
        tag = self.soup.find(text=re.compile(r'\d+\s*bed', re.I))
        return tag.strip() if tag else None

    @property
    def bathrooms(self):
        tag = self.soup.find(text=re.compile(r'\d+\s*bath', re.I))
        return tag.strip() if tag else None

    @property
    def parking_spaces(self):
        tag = self.soup.find(text=re.compile(r'\d+\s*parking', re.I))
        return tag.strip() if tag else None

    # ---------------- Features ----------------
    @property
    def indoor_features(self):
        tags = self.soup.select('.indoor-features li')
        return [t.get_text(strip=True) for t in tags] if tags else None

    @property
    def outdoor_features(self):
        tags = self.soup.select('.outdoor-features li')
        return [t.get_text(strip=True) for t in tags] if tags else None

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
            'indoorFeatures': self.indoor_features,
            'outdoorFeatures': self.outdoor_features,
            'agentName': self.agent_name,
            'agency': self.agency,
            'agentPhone': self.agent_phone,
            'agentEmail': self.agent_email,
            'description': self.description,
            'images': self.images,
            'similarProperties': self.similar_properties
        }


    def fetch_content(self, storage=True):
        self.load_urls(country_code=self.country_code)
        i = 0
        for url in self.urls:
            self.url = url
            html = self.get_html
            if html is None:
                continue

            self.soup = BeautifulSoup(html, 'html.parser')
            all_data = self.get_all_data()
            import pprint
            # pprint.pprint(all_data)
            # df = pd.DataFrame(all_data)
            # print(df)
            for key, value in all_data.items():
                print(key)
                print("\n")
                print(value)
                print("-"*50)
            input("Enter")
            # df = pd.DataFrame(all_data)
            # print(df)
            print("-"*10)
            i +=1
            if i == 3:
                break


