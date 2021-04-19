# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class BbcscraperPipeline:
    def __init__(self):
        # Connect to the Mongo Db server
        # The format was "mongodb+srv://enrich:<password>@cluster0.mri6u.mongodb.net/<name_of_database>?retryWrites=true&w=majority"
        self.conn = pymongo.MongoClient(
            "mongodb+srv://enrich:enrich@cluster0.mri6u.mongodb.net/Articledatabase?retryWrites=true&w=majority"
        )
        # give the name to our database
        db = self.conn['Articledatabase']
        # Define the table name we want to create in our database
        self.collection = db['Article_tb']

    def process_item(self, item, spider):
        # Convert our item object to a dictionary and insert in the table of database
        self.collection.insert(dict(item))
        return item
