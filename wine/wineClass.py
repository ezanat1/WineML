import csv
from fuzzywuzzy import fuzz
import datetime
import hashlib
import math
import os
import pickle
import numpy
from textblob import TextBlob
from wine import db
from wine.models import Wine
from wine import routes
from wine import pairings

# wine id --> comments -> vector --ML--> wine id
class wineClassifier:

    # input file
    storage_file = "storage.pkl"  # location for the stored data
    input_file = "test_part1.csv"  # raw data file
    input_hash = ""

    def normalize(self, score, low, high): #  possible function to scale sentiment
        return  (float(score)-low)/(high-low)

    def sigmoid(self, x): # possible function to scale sentiment
      return 1 / (1 + math.exp(-x))

    def __init__(self):

        print("begin init wineClassifier")
        # load pickled file
        if os.path.isfile(self.storage_file):
            self.input_hash = pickle.load(open(self.storage_file, "rb"))

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
        if self.input_hash and input_hash == self.input_hash:
            print("same input file as last run")
            return
        else:
            print("different file detected, updating")
            self.input_hash = input_hash

        # read from scrapped data into wines list
        with open(self.input_file, "r" , encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            count = 0
            for row in spamreader:
                count += 1
                if row[0] == "wine_id":  # skip top row
                    continue
                wine_id = row[0]

                if Wine.query.get(wine_id):
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
                new_wine = Wine(id=wine_id,name=name,rating=avg_rating,price=price,sentiment=avg_sentiment,
                                 variance=variance,vineyard=vineyard,region=region)
                db.session.add(new_wine)

        db.session.commit()
        pickle.dump(self.input_hash, open(self.storage_file, 'wb'))
        print("end init wineClassifier")

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
        wine_a = Wine.query.filter_by(id=a_id).first()
        wine_b = Wine.query.filter_by(id=b_id).first()
        # find the difference in other factors
        d_variance = 0
        d_vineyard = 0
        d_region = 0

        if not wine_a.variance == wine_b.variance:
            d_variance = 1
        if not wine_a.region == wine_b.region:
            d_region = 1
        if not wine_a.vineyard == wine_b.vineyard:
            d_vineyard = 1

        a_array = numpy.array((wine_a.rating,wine_a.sentiment, 0, 0, 0))
        b_array = numpy.array((wine_b.rating,wine_b.sentiment,d_variance,d_vineyard,d_region))
        weights = numpy.array((0.2, 10, 0.3, 0.1, 0.2))
        return numpy.linalg.norm(weights*(a_array - b_array))

    def getIdByName(self,wineName):
        score = 0
        wineID = -1
        matchName = ""
        for row in Wine.query.all():
            if wineName == row.name:
                wineID = row.id
                matchName = row.name
                break
            new_score = fuzz.partial_ratio(wineName, row.name)
            if new_score > score:
                score = new_score
                wineID = row.id
                matchName = row.name
        print("User wine input",wineName,"Best match is",matchName)
        return wineID

    def getWineByPairing(self, wineID):
        print(pairings.wines)

    """
        This method takes in a probable food name, first finds the food that matches the input
         then returns the type of wines that matches the food 
    """
    def getPairingByName(self,food_name):

        score = 0
        index = -1
        matchName = ""

        if food_name.lower() == "chicken":  # hard code entries
            food_name = "Poultry"


        if food_name in pairings.ref:
            matchName = food_name
            index = pairings.ref.index(matchName)
        else:
            for ref_name in pairings.ref:
                new_score = fuzz.partial_ratio(food_name,ref_name)
                if new_score > score:
                    score = new_score
                    matchName = ref_name
                    index = pairings.ref.index(matchName)
        print("User food input", food_name, "Best match is", matchName)
        # name found, find pairing wines

        match_wines = []
        for wine, match_board in pairings.wines.items():
            if match_board[index] == 1:
                match_wines.append(wine)
        return match_wines


    def getClosestMatch(self, wineID, pairings = None):
        wine_type = []
        result = {}
        if wineID == -1:
            return []

        # iterate through the list of pairings
        if pairings:
            for p in pairings:
                temp_match = self.getPairingByName(p)
                wine_type += temp_match # merge wine lists

        wine_type = list(set(wine_type)) # remove duplicates

        for row in Wine.query.all():
            if not wine_type: # if no pairing info given
                result[row.id] = self.getWineDifference(wineID, row.id)
            else: # user request pairing:
                if row.variance in wine_type: # only add when the variance of the wine matches
                    result[row.id] = self.getWineDifference(wineID, row.id)
        return sorted(result, key=result.get)


    def getWineInfo(self, wineID):
        targetWine = Wine.query.get(wineID)
        result = {}
        result["name"] = targetWine.name
        result["rating"] = targetWine.rating
        result["price"] = targetWine.price
        result["sentiment"] = targetWine.sentiment
        result["variance"] = targetWine.variance
        result["vineyard"] = targetWine.vineyard
        result["region"] = targetWine.region
        result["id"] = targetWine.id
        return result
