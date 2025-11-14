from requests_html import HTMLSession
import os
from storage import Storage
from time import sleep


class Base:

    def __init__(self, *args, **kwargs):
        self.base_url = 'https://www.realestate.com.au/international/{country}/rent/p{page_number}'
        self.session = HTMLSession()
        self.base_storage = Storage()
        super().__init__(*args, **kwargs)
    
    def print(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)
    
    @property
    def clean_screen(self):
        os.system("clear")

    @property
    def get_html(self):
        # set self.url = ''

        sleep(1)
        
        if not self.url:
            print("please set self.url")
            return None

        try:
            self.print(self.url)
            response = self.session.get(self.url)
            if response.status_code == 200:
                return response.text
            else:
                print('status code error: ', self.url)
                return None
        except:
            print(f"Connection Error...")
            return None
    