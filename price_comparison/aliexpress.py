import pandas as pd
from bs4 import BeautifulSoup
import requests, time

def find_computers_aliexpress():
    n = 1
    data = []
    while n <= 50:
        html_text = requests.get(f"https://fr.aliexpress.com/w/wholesale-pc.html?page={n}&g=y&SearchText=pc").text
        soup = BeautifulSoup(html_text, "lxml")
        computers = soup.find_all("div", class_="list--gallery--C2f2tvm search-item-card-wrapper-gallery")

        for computer in computers:
            price_str = computer.find("div", class_="multi--price-sale--U-S0jtj").text.strip()
            price = float(price_str.replace(',', '').split("D")[-1])

            transport_fee_str = computer.find("span", class_="tag--text--1BSEXVh tag--textStyle--3dc7wLU multi--serviceStyle--1Z6RxQ4")
            if transport_fee_str!=None and "Livraison gratuite" not in transport_fee_str.text:
              transport_fee = float(transport_fee_str.text.strip().replace(',', '').split("D")[-1]) if transport_fee_str else None

            promo = (computer.find("span", class_="tag--text--1BSEXVh tag--textStyle--3dc7wLU multi--superStyle--1jUmObG").text.strip()).split()[1] if computer.find("span", class_="tag--text--1BSEXVh tag--textStyle--3dc7wLU multi--superStyle--1jUmObG") else None
            if transport_fee_str!=None and"Livraison gratuite" not in transport_fee_str.text :
              total_price = price + transport_fee if transport_fee else price

            data.append({
                'name': computer.find("div", class_="multi--title--G7dOCj3").text.strip(),
                'price_without_transportion_fee': str(price)+" Dhs",
                'transport_fee': str(transport_fee)+" Dhs" if transport_fee_str!=None and "Livraison gratuite" not in transport_fee_str.text else None ,
                'promo': promo,
                'total_price': total_price if transport_fee_str!=None and "Livraison gratuite" not in transport_fee_str.text else price,
                'website':"AliExpress"
            })
        n += 1
        print(n)

    return data

if __name__ == "__main__":
    data = find_computers_aliexpress()
    with pd.ExcelWriter("output.xlsx") as writer:
        pd.DataFrame(data).to_excel(writer, sheet_name="sheet1")