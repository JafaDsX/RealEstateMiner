import os

class Storage:

    def __init__(self, *args, **kwargs):
        self.storage_path = os.path.join(os.getcwd(), '../', 'data/raw')
        print(self.storage_path) 
        super().__init__(*args, **kwargs)

    def url_storage(self, url_list, country_code):
        file_name = f'{country_code}-advertise-urls.txt'
        os.makedirs(self.storage_path, exist_ok=True)  # make sure folder exists
        with open(os.path.join(self.storage_path, file_name), 'w') as file:
            file.write("\n".join(url_list))

    
    def content_storage(self):
        pass
