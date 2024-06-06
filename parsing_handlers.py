import requests
from bs4 import BeautifulSoup
import json
import os


user_agent = "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
headers = {
    "User-Agent": user_agent
}
main_domain = ""

root = os.path.dirname(__file__) + "/"


# tool for saving web page to html file

def save_html(link, headers, save_to="output.html"):
    """Preservation of a web file in a local document. Save_to allows you to select a file for saving,
    by default it is 'output.html' """
    response = requests.get(link, headers=headers)
    file = open(save_to, mode="w", encoding="utf-8")
    file.write(response.text)
    file.close()


# reading the html file and writing it to a variable for processing

def read_html(file_name="output.html"):
    """Return BeautifulSoup object gat from file_name (output.html by default)"""
    file = open(file_name, mode="rt", encoding="utf-8")
    file_text = file.read()
    file.close()
    html = BeautifulSoup(file_text, "html.parser")
    return html


# getting a list of links from a web page. Example tag: tag = "a"; tag = "a", {"class": "list-item__title"}

def get_products_links(page, tag_find):
    """Getting a list of links from a web page"""
    response = requests.get(page, headers=headers)
    page = BeautifulSoup(response.text, "html.parser")
    tags = page.find_all(tag_find)
    data_links = [tag["href"] for tag in tags]
    return data_links


# read a json file and write it to a variable

def read_json(name_file):
    """Read a json file and write it to a variable"""
    file = open(root + name_file, mode="rt", encoding="utf-8")
    result = json.load(file)
    file.close()
    return result


# data entry into JSON file

def write_json(what, where):
    """Data entry into JSON file"""
    file = open(root + where, mode="wt", encoding="utf-8")
    json.dump(what, file, indent=2, ensure_ascii=False)
    print("success")
