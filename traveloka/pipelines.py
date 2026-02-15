"""
Pipeline to process and save scraped items
"""
import json
from pathlib import Path


class TravelokaPipeline:
    def __init__(self):
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
        
    def process_item(self, item, spider):
        return item
