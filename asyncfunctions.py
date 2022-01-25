# import search_barcode as sb
import asyncio, aiohttp
import json, os
from math import ceil

# ignore event loop policy warnings
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def merge_list(path):
    path = "./" + path.strip("/").replace("\\","/") + "/"
    data = []
    for file in os.listdir(path):
        if file.endswith("json") and file != "old_data.json":
            file_path = os.path.join(path,file)
            data.extend(json.load(open(file_path)))
            os.remove(file_path)

    data = [d for d in data if d != None]
    new_file = os.path.join(path,"data.json")
    json.dump(data,open(new_file,"w"))

def batchers(files,batch_size=80):
    n = len(files)
    z = ceil(n/batch_size)
    x = [i*batch_size for i in range(z+1)]
    x[-1] = n
    return x, len(x)-1

def sec2hms(sec):
    m, s = divmod(sec, 60)
    if m <= 60:
        time_str = f"{int(m):02d}m {int(s):02d}s"
    elif m > 60:
        h, m = divmod(m, 60)
        time_str = f"{int(h):02d}h {int(m):02d}m"
    return time_str

# asynchronous functions
async def render(session, functions, url):
    loop = asyncio.get_event_loop()
    try:
        async with session.get(url) as r:
            result = await loop.run_in_executor(None, functions, url, await r.text())
            return result
    except:
        return None

async def gather(session, functions, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(render(session, functions, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
async def render_all(functions, urls):
    async with aiohttp.ClientSession(headers=headers) as session:
        data = await gather(session, functions, urls)
        return data

# def load_cookies(path,useon="requests"):
#     raw = json.load(open(path))
#     if useon == "requests":
#         cookies = {}
#         for cookie in raw:
#             cookies.update({cookie['name']:cookie['value']})
#         return cookies
#     elif useon == "selenium":
#         cookies = []
#         for cookie in raw:
#             name = cookie['name']
#             value = cookie['value']
#             cookies.append({'name':name,'value':value})
#         return cookies

# def get_auchan_title(page):
#     url = page.find("link",{"rel":"canonical"})['href']
#     try:
#         return page.find("h1").text.strip()
#     except:
#         return None

# def get_auchan_barcode(page):
#     container = page.find_all("div",{"class":"product-description__content-wrapper"})[-1]
#     barcode_raw = container.find_all("div",{"class":"product-description__feature-wrapper"})[-1].text
#     if "EAN" in barcode_raw:
#         barcode = barcode_raw.split(": ")[-1]
#         barcode = barcode.split("/")[-1].strip()
#         return barcode
#     else:
#         return None

# def get_data(html):
#     try:
#         page = BeautifulSoup(html,"html.parser")
#         result = {
#             "title": get_auchan_title(page),
#             "barcode": get_auchan_barcode(page)
#         } 
#         return result
#     except:
#         return None

# def search_barcode(data):
#     name = data['name']
#     brand = data['brand']
#     url = data['url']
#     ori = {
#         "name": name,
#         "brand": brand,
#         "url": url,
#     }
#     if name != None:
#         try:
#             title = sb.search_term(name,brand)
#             result = sb.find_barcode(title)
#             ori.update(result)
#             return ori
#         except:
#             return None
#     else:
#         return None

# search file execution functions
# async def search_from(data):
#     loop = asyncio.get_event_loop()
#     result = await loop.run_in_executor(None, search_barcode, data)
#     return result

# async def search_all(all_data):
#     tasks = []
#     for data in all_data:
#         task = asyncio.create_task(search_from(data))
#         tasks.append(task)
#     results = await asyncio.gather(*tasks)
#     return results