import csv
import datetime
import hashlib
import math
import os
import pickle
import numpy
from textblob import TextBlob

# wine id --> comments -> vector --ML--> wine id
class wineClassifier:
    # dict to put serialized file
    storage = {}
    wines = {}
    distance_grid = {}
    # input file
    storage_file = "storage.pkl"  # location for the stored data
    input_file = "test_part1.csv"  # raw data file

    def normalize(self, score, low, high): #  possible function to scale sentiment
        return  (float(score)-low)/(high-low)

    def sigmoid(self, x): # possible function to scale sentiment
      return 1 / (1 + math.exp(-x))

    def __init__(self):
        # load pickled file
        if os.path.isfile(self.storage_file):
            self.storage = pickle.load(open(self.storage_file, "rb"))
            self.wines = self.storage["wines"]
            self.distance_grid = self.storage["distance_grid"]


        # check if the file is different
        sha1 = hashlib.sha1()
        with open(self.input_file, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha1.update(data)
        input_hash = sha1.hexdigest()

        # input file is same as last time, stop init
        if self.storage.get("hash") and input_hash == self.storage["hash"]:
            print("same input file as last run")
            return

        # read from scrapped data into wines list
        with open(self.input_file, "r" , encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                if row[0] == "wine_id":  # skip top row
                    continue
                wine_id = row[0]
                if self.wines.get(wine_id):  # key exists in file, skip
                    continue
                name = row[1]
                # print(row)
                avg_rating = float(row[2])
                price = float(row[3])
                variance = row[4]
                vineyard = row[5]
                region = row[6]
                comments_detailed = row[7:]
                comments = comments_detailed[2::3]
                # print(comments)
                comment_score = 0
                comment_count = 0
                # parse each comment
                for comment in comments:
                    # sentiment analysis
                    test = TextBlob(comment)
                    comment_score += test.sentiment.polarity
                    comment_count += 1
                avg_sentiment = comment_score / comment_count

                self.wines[wine_id] = {}
                self.wines[wine_id]["name"] = name
                self.wines[wine_id]["rating"] = avg_rating
                self.wines[wine_id]["price"] = price
                self.wines[wine_id]["sentiment"] = self.normalize(avg_sentiment, -1, 1)
                self.wines[wine_id]["variance"] = variance
                self.wines[wine_id]["vineyard"] = vineyard
                self.wines[wine_id]["region"] = region

            #  store evaluated data in file
            self.generateDistanceGrid()
            self.storage["wines"] = self.wines
            self.storage["distance_grid"] = self.distance_grid
            self.storage["hash"] = input_hash
            pickle.dump(self.storage, open(self.storage_file, 'wb'))

    """
            this function generates a dict of dict that sorts all the wine based on its similarity to the current one
             eg self.distance_grid[1][2] give the relative distance between wine 1 and wine 2
    """
    def generateDistanceGrid(self):
        for wine_id, values in self.wines.items():
            for test_id, test_values in self.wines.items():
                if test_id == wine_id:  # skip the current one
                    continue

                if not self.distance_grid.get(wine_id):  # if new wine is loaded
                    self.distance_grid[wine_id] = {}
                if not self.distance_grid.get(test_id):  # fill in the opposite side of the matrix
                    self.distance_grid[test_id] = {}
                if self.distance_grid[wine_id].get(test_id): # skip if result exists
                    continue

                difference = self.getWineDifference(wine_id, test_id)
                self.distance_grid[wine_id][test_id] = difference
                self.distance_grid[test_id][wine_id] = difference

    """
      measure the difference between two wines by calcuating the norm, conditions can be changed to match under other 
      conditions
    """
    def getWineDifference(self, a_id, b_id):
        if a_id == b_id:
            return 0
        wine_a = self.getWineInfo(a_id)
        wine_b = self.getWineInfo(b_id)
        # find the difference in other factors
        d_variance = 0
        d_vineyard = 0
        d_region = 0

        if not wine_a["variance"] == wine_b["variance"]:
            d_variance = 1
        if not wine_a["region"] == wine_b["region"]:
            d_region = 1
        if not wine_a["vineyard"] == wine_b["vineyard"]:
            d_vineyard = 1

        a_array = numpy.array((wine_a["rating"],wine_a["sentiment"], 0, 0, 0))
        b_array = numpy.array((wine_b["rating"],wine_b["sentiment"],d_variance,d_vineyard,d_region))
        weights = numpy.array((0.2, 10, 0.3, 0.1, 0.2))
        return numpy.linalg.norm(weights*(a_array - b_array))

    def getWineID(self,wineName):
        wineID = 0
        for key,value in self.wines.items():
            if value["name"]==str(wineName):
                wineID = key
                break
        return wineID
    def getClosestMatch(self, wineName): 
        wineID = self.getWineID(wineName)
        if wineID == 0:
            return []
        return sorted(self.distance_grid[wineID], key=self.distance_grid[wineID].get)

    def getWineInfo(self, wineiD):
        return self.wines.get(wineiD)
