# import working libraries
import requests
from bs4 import BeautifulSoup
import json, re

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

def get_table(table):
    thead = table.find("thead")
    tbody = table.find("tbody")
    label = thead.find("tr").find_all("th")[1].text.strip()
    values = {}
    for tr in tbody.find_all("tr"):
        td = tr.find_all("td")
        name = td[0].text.strip()
        value = td[1].text.strip()
        values.update({name:value})
    return label, values

def scraper(src,html):

    # convert the html file into bs4 object
    page = BeautifulSoup(html,"html.parser")
    
    # check if it has nutriscore word
    if "nutriscore" in html.lower():
        it_has_nutriscore = True
    else:
        it_has_nutriscore = True
    
    # find script tag
    try:
        script = page.find("script",{"type":"application/ld+json"})
        raw = json.loads(script.text)
    except: raw = None
    
    if raw != None:
        
        # find product name
        try: name = raw[2]['name']
        except: name = None

        # find product brand
        try: brand = raw[2]['brand']['name']
        except: brand = None

        # find product image url
        try: img_url = raw[2]['image'][0]
        except: img_url = None

        # find product categories
        try: categories = "; ".join([e['item']['name'] for e in raw[3]['itemListElement'][1:]]) + ";"
        except: categories = None
        
        # find product barcode gtin
        try: code = raw[2]['gtin13']
        except: code = None
        
    else:
        name = brand = img_url = categories = code = None

    # find product calories information
    try:
        product_info = page.find("div",{"class":["grocery-product","grocery-product__product-desc"]})
    except:
        product_info = None

    try:
        nutritions_table = product_info.find("section",{"class":"tabularContent"}).find("table")
        label, values = get_table(nutritions_table)
        try:
            calories = " = ".join([label,values["-"]])
        except:
            calories = " = ".join([label,values["Energy"]])
    except:
        calories = None

    # find product ingerdients information
    try:
        ingredients = product_info.find("div",{"class":"product-info-block","id":"ingredients"}).text.strip()
    except:
        ingredients = None

    # find product origin information
    try:
        origin = product_info.find("div",{"class":"product-info-block","id":"manufacturer-address"}).find("li").text.strip().strip(",")
    except:
        origin = None
        
    product_data = {
        'url': src,
        'image_url': img_url,
        'name': name,
        'brand': brand,
        'nutriscore': None,
        'categories': categories,
        'ingredients': ingredients,
        'calories': calories,
        'manufactured_at': origin,
        "it_has_nutriscore": it_has_nutriscore,
        'code': code
    }

    if len([v for v in product_data.values() if v == None]) != 9:
        return product_data
    else:
        return None

if __name__ == "__main__":

    url = "https://www.tesco.com/groceries/en-GB/products/303004400"
    req = requests.get(url, headers=headers)
    data = scraper(url, req.text)
    print(data)