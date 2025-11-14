
from base import Base
from bs4 import BeautifulSoup


class GetPageURLs(Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def get_latest_page_number(self):
        # get the number of pages

        self.url = self.base_url.format(country=self.country_code, page_number=1)
        html = self.get_html

        if not html:
            print("We can't get latest page number!")
            exit()

        soup = BeautifulSoup(html, 'html.parser')
        content = soup.select('li.ant-pagination-item > a')
        if content:
            self.last_page_number = int(content[-1].get_text())
            self.clean_screen
            self.print(f"find {self.last_page_number} page in {self.url}")

    def build_main_page_urls(self):
        # building urls from page 1 to last page
        self.urls = [self.base_url.format(country=self.country_code, page_number=i) for i in range(1, self.last_page_number)]            

    def get_advertise_url(self, storage=True):
        advertise_urls = []

        for url in self.urls:
            self.url = url
            html = self.get_html
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.select('div.sc-1dun5hk-0 > a')
            if content:

                links = [f'https://www.realestate.com.au{i.get("href")}' for i in content]
                advertise_urls.extend(links)
        
        if storage:
            self.base_storage.url_storage(advertise_urls, country_code=self.country_code)
            print("Saved!")