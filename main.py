from bs4 import BeautifulSoup
import requests as req
import os
import lxml
from smtplib import SMTP

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
TARGET_PRICE = 68
PRODUCT_URL = "https://www.amazon.com.br/dp/8575224158/?coliid=I2FMUAJHABN7IZ&colid=2OS1FKTLRUG66&psc=1"
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

response = req.get(url=PRODUCT_URL, headers=HEADER)
product_webpage = response.text
soup = BeautifulSoup(product_webpage, 'lxml')
price = soup.find('span',
                  class_="a-size-base a-color-price a-color-price"
                  ).getText()

product_title = soup.find('span', id='productTitle').getText().strip()
print(f"{product_title}\n{price}")

if TARGET_PRICE > float(price.replace("R$", "").replace(",", ".")):
    with SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls()
        smtp.login(user=SENDER_EMAIL, password=SENDER_PASSWORD)
        smtp.sendmail(from_addr=SENDER_EMAIL,
                      to_addrs=RECIPIENT_EMAIL,
                      msg=f'Subject:Amazon Price Alert!\n\n"{product_title}" is now {price}'.encode('utf8'))
