from requests_html import HTMLSession
import os
from storage import Storage
from time import sleep
from colorama import Fore
import platform

class Base:

    def __init__(self, *args, **kwargs):
        self.base_url = 'https://www.realestate.com.au/international/{country}/rent/p{page_number}'
        self.session = HTMLSession()
        self.base_storage = Storage()
        self.r = Fore.RED
        self.rt = Fore.RESET
        self.g = Fore.GREEN
        super().__init__(*args, **kwargs)
    
    def print(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)
    
    @property
    def clear_screen():
        current_os = platform.system()  
        
        if current_os == "Windows":
            os.system("cls") 
        elif current_os in ["Linux", "Darwin"]:  
            os.system("clear")
        else:
            print("\n" * 100)

    @property
    def save_dead_links(self):
        try:
            with open("./dead-links.txt", 'a') as file:
                file.write(self.url + '\n')
            
            print(f"{self.g}Saved successfully!{self.rt}")
        except:
            print(f"{self.r}ERROR Saving dead link...{self.rt}")

    @property
    def get_html(self):
        """
        for using this method:
            you have set 'self.url' first
        """
        sleep(1)
        
        if not self.url:
            print(f"{self.r}Please set self.url{self.rt}")
            return None

        try:
            response = self.session.get(self.url)
            if response.status_code == 200:
                return response.text
            else:
                print(f'{self.g}status code error: {self.url}{self.rt}')
                self.save_dead_links
                return None
        except:
            print(f"{self.r}Connection Error...{self.rt}")
            self.save_dead_links
            return None
    