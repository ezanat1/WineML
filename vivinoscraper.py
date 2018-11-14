import requests
import json
import csv
import threading
import time

def testfunc(wine_id):
  part1 = 'https://www.vivino.com/api/wines/'
  wine = wine_id
  part2 = '/wine_page_information'
  url = part1 + str(wine) + part2
  r = requests.get(url)
  info = r.json()

  L = []
  avg_rating = info['wine_page_information']['vintage']['statistics']['ratings_average']
  price = info['wine_page_information']['highlights'][0]['metadata']['price']['amount']
  varietal = info['wine_page_information']['highlights'][0]['metadata']['style']['grapes'][0]['name']
  vineyard =info['wine_page_information']['vintage']['wine']['winery']['name']
  region =info['wine_page_information']['vintage']['wine']['region']['name']
  L += [str(wine),avg_rating,price,varietal,vineyard,region]

  webpage1 = 'https://www.vivino.com/api/wines/'
  wine = wine_id
  webpage2 = '/reviews?per_page=10&page='
  i = 1

  combined = webpage1 + str(wine) + webpage2 + str(i)
  while (requests.get(combined).status_code==200 and i < 20):
    rcom = requests.get(combined)
    rcom_json = rcom.json()
    for j in range(0,len(rcom_json['reviews'])):
      comm_id = rcom_json["reviews"][j]["id"]
      comm_rating = rcom_json["reviews"][j]["rating"]
      comm_note = rcom_json["reviews"][j]["note"].replace(",","")
      L += [comm_id,comm_rating,comm_note]
    i = i+1
    combined = webpage1 + str(wine) + webpage2 + str(i)
  return L

success = 0
failures = 0

with open('test.csv', 'a') as csvfile:
  derpwriter = csv.writer(csvfile)
  derpwriter.writerow(['wine_id','avg_rating','price','varietal','vineyard','region','comm_id','comm_rating','comm_note'])

  for i in range(1213337, 1400000):
    try:
      print(i)
      time.sleep(1)
      output = testfunc(i)
      try:
        derpwriter.writerow(output)
      except Exception as ee:
        print('fail to write')
        failures += 1
    except Exception as e:
      print ('id not valid')
      failures += 1
    else:
      success += 1


print ('success: ',str(success))
print ('failures: ',str(failures))

