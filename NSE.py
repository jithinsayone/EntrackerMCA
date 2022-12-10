import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException



import requests
headers = {
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
'cookie': 'ga=GA1.1.1349942696.1670346998; ak_bmsc=21459057CF378479A4DBD48C667BFE82~000000000000000000000000000000~YAAQXydzaGBl/KGEAQAAsQtc+xJjwBsiBf5tDYEZHNuCt1LZ+j0iVTIzp+B0N3OLzJN7ABlqp49IYWTCLT7s1dShO0PGJIGZ3Bi1HNV2fs3Z5ypYrNtLnJeBMkicEoGEw7xdOJfSiJVrtmatY4k1GNoKqtQQ3FWP6IEu0rixkoHGLv9oF4z9+Q+dl3xTPgsc68ydBrmjjlSGwPfmhFs/LSh392X8Rb2U19FJC4o2rzFi3Gc9icifgGEGi2D7QbSqRR6PFIRy4iqbkTdYbYXT7VGnuWeb1IFT9JzJE9pO7R31MF0HR6kpOxQ02DWLLYilLPQCN3107HUx98fqK/LKKSCB+qloVphh8ZW01uFjBBT+NfHaA52K7MZ3kbVPEzQ6aTJ3/Fj/d11tHUXFZ/y0rh6VsL/YGPPnwkJfTQZFHHi8eaZJt+mECfFxzcvbq+aI/f9xauDz+cn/MDILiUo3h/QFsuZuJKuH5TWpRr5d2uDyknjmnAvQ2H3MbloF; nseQuoteSymbols=[{"symbol":"NAUKRI","identifier":null,"type":"equity"}]; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTY3MDY2OTg2NiwiZXhwIjoxNjcwNjczNDY2fQ.wLAKUUBKSpCddLoWupqTcVEfzG85aw7-rvAC7ySF4W8; nsit=tJ3H7oV5disSZ5b1ceOMD5xx; AKA_A2=A; _ga_PJSKY6CFJH=GS1.1.1670669866.4.1.1670669872.54.0.0; bm_sv=1A357DFD76313C9D0CFBBECA403E73C6~YAAQaTLUFyiWeYKEAQAAHWqv+xKrDEwXt/oEdP1HLI0lv65Fx7OAbyfXMHeThet0JayJfWBJebCOESsHI3zVLdxnnMoC062KV/iWSo/tv3o1HAbRUA/77+QCbaZnr4ep1MXWRPMKt/5O44DYcghOTEXuuW48/Vv4F8Wf/k4IWKH3mOoMn+b60kE3wL1z3ZJ1OZOt9J0UojAZHtwj19x42WHdWLdV3ZqYTELzGtf6w+YUtTbT8Azb0CKHyDRFa3F6gNdX~1; RT="sl=0&ss=lbhtp9gb&tt=0&z=1&dm=nseindia.com&si=7f0fb097-6433-4fea-8eb0-1e1dabe798f7&nu=4as7epbn&cl=1e40',
#'referer': 'https://www.nseindia.com/companies-listing/corporate-filings-announcements?symbol=NAUKRI&tabIndex=equity',
'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Linux"',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
}



company_list=["NAUKRI","ZOMATO","DELHIVERY","NYKAA","POLICYBZR","PAYTM","CARTRADE","EASEMYTRIP"]
for i in company_list:
   print("Searching :",i)
   r = requests.get("https://www.nseindia.com/api/corporate-announcements?index=equities&symbol="+i,headers=headers)

   print(r)
   if r.status_code == 200:
       import json
       data = json.loads(r.text)
       #print(data)       
       #print("Document Count:",len(data))
       for i in data:
        print("Subject :",i['desc'],"\n","ANNOUNCEMENT :",i['attchmntText'])
   else:
       print("blocekd")
   time.sleep(10)