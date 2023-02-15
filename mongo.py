import pymongo
import scrapper
import logging

logging.basicConfig(filename="mongo_db.log", level=logging.DEBUG, filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")


class Mongo_DB:

    def __init__(self, clienturl):
        self.clienturl = clienturl
        try:
            self.client = pymongo.MongoClient(self.clienturl)
        except Exception as e:
            print("Connection not established", e)
            logging.error("Connection not established", e)
        else:
            print("Connection to MongoDB is successful")
            logging.info("Connection to MongoDB is successful")

    def create_database(self, db_name):
        try:
            self.database = self.client[str(db_name)]
        except Exception as e:
            print("Error while creating Database", e)
            logging.error("Error while creating Database", e)
        else:
            print("Database has been created successfully")
            logging.info("Database has been created successfully")

    def create_collection(self, collection_name):
        try:
            self.collection = self.database[str(collection_name)]
        except Exception as e:
            print("Error while creating collection", e)
            logging.error("Error while creating collection", e)
        else:
            print("collection has been created successfully")
            logging.info("Collection has been created successfully")

    def insert_data(self, document):
        try:
            if type(document) == dict:
                self.collection.insert_one(document)
            elif type(document) == list:
                self.collection.insert_many(document)
        except Exception as e:
            print("Error while inserting data", e)
            logging.error("Error while inserting data", e)
        else:
            print("Data insertion successful")
            logging.info("Data insertion successful")

    def show_data(self):
        try:
            for i in self.collection.find():
                print(i)
        except Exception as e:
            print("There's an error showing data", e)
            logging.error("There's an error showing data", e)



obj = scrapper.Ineuron_Scrapping()
obj.ineuron_course_data()
obj.get_all_course_titles()
courses_info = obj.scrap_all_course()

url = "mongodb+srv://mongodb:mongodb@cluster0.qg6hnmq.mongodb.net/?retryWrites=true&w=majority"
mongo = Mongo_DB(url)

mongo.create_database("ineuron_courses")
mongo.create_collection("courses_collection")
mongo.insert_data(courses_info)

