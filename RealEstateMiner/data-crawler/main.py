from base import Base
from get_urls import GetPageURLs
from get_content import GetPageContent
from argparse import ArgumentParser
from storage import Storage
import pycountry


class Main(GetPageURLs, GetPageContent, Storage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def country_to_code(self):
        try:
            country = pycountry.countries.lookup(self.country)
            return country.alpha_2
        except:
            return None
    
    @property
    def get_user_arguments(self):
        parser = ArgumentParser()

        parser.add_argument(
            '-fu', '--fetch-urls',
            help='Get All Advertising URLs',
            action='store_true',
            default=False
        )

        parser.add_argument(
            '-fc', '--fetch-contents',
            help='Get All Advertising Contents',
            type=str,
        )
        parser.add_argument(
            '-c', '--country',
            help='Country Name',
            type=str,
            default='all'
        )
        parser.add_argument(
            '-s', '--storage',
            help='Save Links Or Contents',
            action='store_true',
            default=True
        )
        parser.add_argument(
            '-v', '--verbose',
            help='Verbosity',
            action='store_true',
            default=True
        )

        self.fetch_urls = parser.parse_args().fetch_urls
        self.fetch_contents = parser.parse_args().fetch_contents
        self.storage = parser.parse_args().storage
        self.country = parser.parse_args().country
        self.verbose = parser.parse_args().verbose

        self.country_code = self.country_to_code

        if self.fetch_urls is None and self.country_code is None:
            print(f"Invalid Country Name: {self.country}")
            exit()

        if not self.fetch_urls and not self.fetch_contents:
            parser.print_help()
        
        if not self.storage:
            print("Storage is false. Are you sure? y/n")
            input("/> ")
        

    def run(self):
        self.get_user_arguments

        if self.fetch_urls:
            self.clean_screen
            self.get_latest_page_number
            self.build_main_page_urls()
            self.get_advertise_url(storage=self.storage)
    
        if self.fetch_contents:
            self.clean_screen
            print("Fetch Contents")
            self.fetch_content(storage=self.storage)

        


if __name__ == "__main__":
    main = Main()
    main.run()