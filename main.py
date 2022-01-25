# import libraries
import asyncfunctions as af
import os, sys, json, time
import numpy as np
import requests
import asyncio

# import logic libraries
import logic
from printer import print_green, print_red, print_yellow

# get the start input
try: st = int(sys.argv[1])
except: st = 0

# clear the terminal
os.system("cls")
beginning = time.time()
print("program start..")

# prepare the destionation folder
dest_folder = "./Tesco/data/"
speed = [] # timespeed variable

# read all the product urls
urls = json.load(open("./Tesco/urls/product_urls.json"))
urls = list(dict.fromkeys(urls))

# iterate the scraping process in batches
index = list(range(0,len(urls)))

# filter the scraped urls
root = "./Tesco/data/"
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

x, R = af.batchers(urls,80)
print(f"{len(urls)} data will be devided into {R} batch")
for r in range(st,R):
    print(f">> batch{r:03d}", end=" ")
    try:
        start = time.time()
        a, b = x[r], x[r+1]
        # results = asyncio.run(af.render_all(logic.scraper,urls[a:b]))
        # for i, result in zip(index[a:b],results):
        #     if result != None:
        #         dest_file = dest_folder + f"{i:05d}.json"
        #         if not os.path.exists(dest_file):
        #             json.dump(result,open(dest_file,"w"))
        results = []
        for i,url in zip(index[a:b],urls[a:b]):
            dest_file = dest_folder + f"{i:05d}.json"
            req = requests.get(url,headers=logic.headers)
            result = logic.scraper(url, req.text)
            if not os.path.exists(dest_file):
                json.dump(result,open(dest_file,"w"))
                print(i,end=" ")
        end = time.time()
        speed.append(end-start)
        est = af.sec2hms(int(np.mean(speed)*(R-r)))
        print_green(f"{end-start:.2f} sec (est. {est} left)")
    except:
        print_red("failed")
    break

# end statement
end = time.time()
time_str = f"{af.sec2hms(end-beginning)}"
print_yellow("done in " + time_str)