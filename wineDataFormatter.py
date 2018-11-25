import csv
import math

import numpy
from textblob import TextBlob

# wine id --> comments -> vector --ML--> wine id
class wineClassifier:
    wines = {}
    # input file
    file = "test_part1.csv"

    def normalize(self, score, low, high):
        return  (float(score)-low)/(high-low)

    def sigmoid(self, x):
      return 1 / (1 + math.exp(-x))

    def __init__(self):
        # read from scrapped data into wines list
        with open(self.file, "r" , encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                if row[0] == "wine_id":
                    continue
                wine_id = row[0]
                avg_rating = row[1]
                price = row[2]
                variance = row[3]
                vineyard = row[4]
                region = row[5]
                comments_detailed = row[6:]
                comments = comments_detailed[2::3]
                # print(comments)
                comment_score = 0
                comment_count = 0
                for comment in comments:
                    test = TextBlob(comment)
                    comment_score += test.sentiment.polarity
                    comment_count += 1
                avg_sentiment = comment_score / comment_count
                self.wines[wine_id] = (float(price), float(avg_rating), float(avg_sentiment))

    # sorts the list of wine
    def sortClosest(self, wineID):
        recommendationList = {}
        current_wine = numpy.array(self.wines[wineID])
        for id, values in self.wines.items():
            if id == wineID:  # skip the current one
                continue
            test_wine = numpy.array(values)
            difference = numpy.linalg.norm(current_wine - test_wine)
            recommendationList[id] = difference
        return  sorted(recommendationList, key=recommendationList.get)




a = wineClassifier()
print(a.sortClosest("90577"))

        

