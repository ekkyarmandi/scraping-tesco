import requests
from bs4 import BeautifulSoup
from math import ceil
import json, re, os, sys

os.system("cls")

def render(url):
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    req = requests.get(url, headers=headers)
    page = BeautifulSoup(req.text, "html.parser")
    return page

def get_max_page(page):
    nav = page.find("div",{"data-auto":"product-bin-count","role":"status"})
    shown_items, total_items = nav.find("strong").text.strip(), nav.find_all("strong")[-1].text.strip()
    shown_items, total_items = re.findall("\d+",shown_items)[-1], re.findall("\d+",total_items)[-1]
    return ceil(int(total_items)/int(shown_items))

def collect_urls(url,page):
    ref = "https://www.tesco.com"
    container = page.find("div",{"class":"product-list-container"})
    urls = []
    for i in container.find_all("li",{"class":"product-list--list-item"}):
        url = ref + i.find("a")['href']
        urls.append(url)
    return urls

if __name__ == "__main__":

    urls = [
        "https://www.tesco.com/groceries/en-GB/shop/easter/all?include-children=true",
        "https://www.tesco.com/groceries/en-GB/shop/pets/all?include-children=true",
        "https://www.tesco.com/groceries/en-GB/shop/baby/all?include-children=true",
        "https://www.tesco.com/groceries/en-GB/shop/drinks/all?include-children=true",
        "https://www.tesco.com/groceries/en-GB/shop/food-cupboard/all?include-children=true",
        "https://www.tesco.com/groceries/en-GB/shop/frozen-food/all?include-children=true",
        "https://www.tesco.com/groceries/en-GB/shop/bakery/all?include-children=true",
        "https://www.tesco.com/groceries/en-GB/shop/fresh-food/all?include-children=true"
    ]

    product_urls = []
    for url in urls:

        # print
        print(url)

        # render the url
        page = render(url)

        # collect the product urls first page
        purls = collect_urls(url,page)
        product_urls.extend(purls)

        # iterate the process through pages
        max_page = get_max_page(page)
        for i in range(2,max_page+1):

            # render the next page
            next_url = url + f"&page={i:d}"
            page = render(next_url)

            # collect the product urls next page
            purls = collect_urls(next_url,page)
            product_urls.extend(purls)

    # save it as a json file
    product_urls = list(dict.fromkeys(product_urls))
    json.dump(product_urls,open("./Tesco/data/product_urls.json","w"))