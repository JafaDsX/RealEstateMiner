
import numpy as np
import pandas as pd
import random


class RandomDatasetGenerator:
    
    def __init__(self, sample_size=100, *args, **kwargs):
        self.sample_size = sample_size
    
    @property
    def generator(self):
        
        data = {
            "num_rooms": np.array(random.choices(np.arange(1, 5), k=self.sample_size)),
            "area": np.array(random.choices(np.arange(50, 300), k=self.sample_size)),
            "age": np.array(random.choices(np.arange(1, 40), k=self.sample_size)), # age -> apartment
            "distance_city_center": np.array(random.choices(np.arange(5, 50), k=self.sample_size)),
            "price": np.array(random.choices(np.arange(100000, 1000000), k=self.sample_size))
        }
        
        self.data = pd.DataFrame(data)
        
    @property
    def save(self):
        self.data.to_csv("../data/raw/random-generated.csv", index=False)
    
    def run(self):
        self.generator
        self.save
    
    
if __name__ == "__main__":
    main = RandomDatasetGenerator(sample_size=10000)
    main.run()