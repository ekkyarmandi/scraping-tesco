# import libraries
import asyncfunctions as af
import os, sys, json, time
import numpy as np
import requests

# import logic libraries
import logic
from printer import print_green, print_red, print_yellow

# get the start input
try: st = int(sys.argv[1])
except: st = 0

# clear the terminal
os.system("cls")
beginning = time.time()

# prepare the destionation folder
dest_folder = "./data/"
speed = [] # timespeed variable

# read all the product urls
urls = json.load(open("./urls/product_urls.json"))
urls = list(dict.fromkeys(urls))

# iterate the scraping process in batches
index = list(range(st,len(urls)))

# filter the scraped urls
root = "./data/"
for file in os.listdir(root):
    if file.endswith("json"):
        i = int(file.replace(".json",""))
        data = json.load(open(root+file))
        if data != None:
            url = data['url']
            urls.remove(url)
            index.remove(i)
        elif data == None:
            os.remove(root+file)

print(f"total data {len(urls)}")
j = 1
for i,url in zip(index,urls):
    dest_file = dest_folder + f"{i:05d}.json"
    try:
        start = time.time()
        req = requests.get(url,headers=logic.headers)
        result = logic.scraper(url, req.text)
        if not os.path.exists(dest_file) and result != None:
            json.dump(result,open(dest_file,"w"))
        end = time.time()
        speed.append(end-start)
        est = af.sec2hms(int(np.mean(speed)*(len(index)-j)))
        print_green(f"{i:05d}: {end-start:.2f} sec (est. {est} left)")
    except:
        print_red("failed")
    j += 1

# end statement
end = time.time()
time_str = f"{af.sec2hms(end-beginning)}"
print_yellow("done in " + time_str)