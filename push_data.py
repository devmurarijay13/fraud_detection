import os
import sys
import json
import pandas as pd
import numpy as np
import pymongo

from fraud_detection.exception.exception import FraudDetectionException
from fraud_detection.logging.logger import logging

import certifi ## it provides set of root certificates, veryfying trusted https requests

from dotenv import load_dotenv  ## for calling env variable
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
# print(MONGO_DB_URL)

ca = certifi.where() ## ca = certificate authority

class FraudDetectionDataExtract:
    """
    Aim to read all the data and converts it into json file
    """
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    def csv_to_json_convertor(self,file_path,chunk_size=10000):
        try:
            chunk_reader = pd.read_csv(file_path,chunksize=chunk_size)
            for i,chunk in enumerate(chunk_reader):
                yield chunk.to_dict(orient='records')

        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    # def insert_data_mongodb(self,records,database,collection):
    #     try:
        #     self.database = database
        #     self.collection = collection
        #     self.records = records

        #     self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

        #     self.database = self.mongo_client[self.database]
        #     self.collection = self.database[self.collection]
            
        #     self.collection.insert_many(self.records)

        #     return (len(self.records))
        
        # except Exception as e:
        #     raise FraudDetectionException(e,sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            db = self.client[database]
            coll = db[collection]
            
            coll.insert_many(records)
            
            return len(records)
        except Exception as e:
            raise FraudDetectionException(e,sys)



if __name__ == "__main__":
    FILE_PATH = r"Fraud_Detection_Data/fraud_data_half.csv"
    DATABASE = 'jd_database'
    COLLECTION = 'FraudDetectionData'

    try:
        fraud_detection_obj = FraudDetectionDataExtract()
        
        # 1. This creates the generator.
        records_generator = fraud_detection_obj.csv_to_json_convertor(FILE_PATH, chunk_size=20000)
        
        print("--- 🚀 Starting data insertion... ---")
        total_inserted = 0
        
        # 2. This LOOP is the missing piece.
        #    It pulls one chunk at a time from the generator.
        for records_chunk in records_generator:
            if records_chunk:
                # 3. Insert just one chunk
                inserted_count = fraud_detection_obj.insert_data_mongodb(records_chunk, DATABASE, COLLECTION)
                total_inserted += inserted_count
                        
        print(f"\n--- ✅ FINISHED! Total records inserted: {total_inserted} ---")

    except Exception as e:
        raise FraudDetectionException(e,sys)

        

