import pymongo

class Mongo:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.container_db = self.myclient["test_db"]

    def has_database(self, db):
        dblist = self.myclient.list_database_names()
        if db in dblist:
            print("The database exists.")

    def has_container_db_collection(self, collection):
        collist = self.container_db.list_collection_names()
        if collection in collist:
            print("The collection exists.")

    def insert_mtd_data(self, web_server, wait_time, server_up_time, start_time, end_time):
        rotation_elapsed_time = end_time - start_time #time in seconds
        mycol = self.container_db["rotation"]
        mydict = {"live_web_server":web_server,
                  "wait_time":wait_time,
                  "server_up_time":server_up_time,
                  "start_time":start_time,
                  "end_time":end_time,
                  "rotation_elapsed_time":rotation_elapsed_time}
        x = mycol.insert_one(mydict)
        print("Database ID: ",x.inserted_id)