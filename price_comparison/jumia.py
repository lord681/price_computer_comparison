import pandas as pd
from bs4 import BeautifulSoup
import requests, time

def find_computers_jumia():
    n=1
    data = []
    while n<=50:
        html_text=requests.get(f"https://www.jumia.ma/catalog/?q=pc&page={n}#catalog-listing").text
        soup=BeautifulSoup(html_text,"lxml")
        computers=soup.find_all("a",class_="core")

        for computer in computers:

            data.append({
                'name':computer.find("h3",class_="name").text.strip(),
                'price_without_transportion_fee':computer.find("div",class_="prc").text.strip(),
                'transport_fee':None,
                'promo':computer.find("div", class_="bdg _dsct _sm").text.strip() if computer.find("div", class_="bdg _dsct _sm") else None,
                'total_price':computer.find("div",class_="prc").text.strip(),
                'website':"jumia"
            })
        n+=1
        print(n)


    return data

if __name__=="__main__":

    data = find_computers_jumia()
    with pd.ExcelWriter("output2.xlsx") as writer:
        pd.DataFrame(data).to_excel(writer,sheet_name="sheet1")

