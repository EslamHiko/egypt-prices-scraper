"""
Importing Libraries
"""
from bs4 import BeautifulSoup as bs
import json
import requests as rq
import pathlib
import csv
url = "http://www.egprices.com/en/category/computers/laptops"
s = rq.get(url).content ### Get The Page Content

soup = bs(s,"html.parser") ### Analyzing Page Tags And Classes
pages = []

### Finding The Last Page Num
for x in soup.find('ul',{'class':'pagination'}):
    try :
        pages.append(int(x.text))
    except:
        pass ## To Ignore Undefined '...' Pages ex: 1 - 2 - ... - 61
w = 1
"""
Creating Lists To Collect Information
"""
images = []
item_name = []
prices = []
stores = []
items = 0
### Scraping The Site Page By Page
while w <= max(pages):
    url = "http://www.egprices.com/en/category/computers/laptops" + "/?&page=" + str(w)
    s = rq.get(url).content
    soup = bs(s,"html.parser")
    for tag in soup.find_all('div',{'class':'row hide-for-small-only'}):
    ### Getting Images
        for x in tag.find_all('a',{'class':'divItem'}):
            for a in x.find_all('img',src=True):
                images.append("http://www.egprices.com" + a['src'])
    ### Getting Item's Name
        for x in tag.find_all('div',{'class':'medium-6 columns'}):
            for a in x.find('a'):
                item_name.append(a)
                items = items + 1
    ### Getting Item's Price
        for x in tag.find_all('div',{'class':'medium-2 text-center columns'}):
            for a in x.find_all('div',{'class':'child'}):
                for b in a.find('div'):
                    prices.append(b)
    ### Getting Store's Name
        for x in tag.find_all('div',{'class':'medium-2 text-center columns'}):
            for a in x.find_all('img',src=True,alt=True):
                if('store' in a['src']):
                    stores.append(a['alt'])
    print('scraping page: '+str(w)) ### Print The Page Num It's Working On To Tell Me That It's Working
    w = w + 1
"""
Exporting To CSV File
"""
pathlib.Path('./results').mkdir(parents=True, exist_ok=True) 


f = csv.writer(open("./results/Laptops.csv",'w',newline=''))
f.writerow(['item','price','store','image'])
result = zip(item_name,prices,stores,images)

for x in result:
    f.writerow(x)
"""
Exporting To JSON File
"""

json_result = [{'name':n,'price': p,'store':s,'image':i} for n, p, s, i in zip(item_name,prices,stores,images)]

f = open("./results/Laptops.json",'w',newline='')
f.write(json.dumps(json_result, indent=4, separators=(',', ': ')))

print(json.dumps(json_result, indent=4, separators=(',', ': ')))
