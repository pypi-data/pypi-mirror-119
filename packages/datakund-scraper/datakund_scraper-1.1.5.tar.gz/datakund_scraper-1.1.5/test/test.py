from datakund_scraper import *
import json
link='https://stackoverflow.com/questions/4345830/calculate-area-of-html-element-on-website'
#response=scraper.train(url=link)
#print(response["id"])
#response=scraper.run(url=link,id=response["id"])
response=scraper.run(url=link,id="TG67K0DK04R8XTJ")
print(response)
with open ("data.json","w",encoding="utf-8") as d:
    d.write(json.dumps(response,sort_keys=False))
'''
import json
import datetime
def read_file(file):
    with open(file+".txt",encoding="utf-8") as d:
        html=d.read()
    return html
print(datetime.datetime.now())
html1=read_file("html1")
html2=read_file("html2")
res=scraper.train(html1,html2)
#res=scraper.run(html=html1,id="NUT7D6M49OTWUBT")
print("res",res)
print(datetime.datetime.now())
'''