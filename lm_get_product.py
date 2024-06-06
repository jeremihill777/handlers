from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from data_base_handlers import Database

db = Database("Leroy_Merlin")

user_agent = "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"

headers = {
    "User-Agent": user_agent
}
main_domain = "https://www.leroymerlin.pl/"

db.create_table("products", {"id_lm": "INTEGER", "product_name": "TEXT", "product_price": "FLOAT"})

url = "https://www.leroymerlin.pl/produkty/lazienka/baterie-lazienkowe/baterie-bidetowe/?p=1"
browser = webdriver.Chrome()
browser.get(url)
time.sleep(3)
with open('lm_web_page.html', mode='wt', encoding="utf-8") as file:
    file.write(browser.page_source)
file = browser.page_source


def get_products_link(page, tag):
    # response = requests.get(page, headers=headers)
    page_1 = BeautifulSoup(page, "html.parser")
    tags = page_1.find_all("a", {"class": "kl-tile-link kl-tile--h-to-v"})
    data_links = [tag["href"] for tag in tags]
    return data_links


data_links = get_products_link(file)
full_data_links = [main_domain + data_link for data_link in data_links]

for link in full_data_links:
    browser.get(link)
    time.sleep(3)
    with open('lm_product.html', mode='wt', encoding='utf-8') as file_product:
        file_product.write(browser.page_source)
    file_product = browser.page_source
    page = BeautifulSoup(file_product, "html.parser")
    product_ref = page.find("span", {"class": "js-product-ref"}).text.strip()
    product_name = page.find("h1",
                             {"class": "mt-heading mt-heading--s l-product-detail-presentation__title"}).text.strip()
    product_price = page.find("span", {"class": "js-main-price"}).text.strip()
    db.add_record("products", (product_ref, product_name, product_price))
    db.save()
