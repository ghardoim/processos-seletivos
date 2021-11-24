from bs4 import BeautifulSoup
from flask import jsonify
import requests as rq
import flask

def get_lenovo_list():
    resp = rq.get("https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")
    soup = BeautifulSoup(resp.text, 'html.parser')

    lenovo_list = []
    for notebook in soup.find_all("div", class_ = "col-sm-4 col-lg-4 col-md-4"):
        if "lenovo" in notebook.text.lower():
            lenovo = {}
            lenovo["id_product"] = notebook.find("a", class_ = "title")["href"].split("/")[-1]

            lenovo["title"] = notebook.find("a", class_ = "title")["title"]
            lenovo["price"] = float(notebook.find("h4", class_ = "pull-right price").text[1:])

            lenovo["image"] = notebook.find("img", class_ = "img-responsive")["src"]
            lenovo["reviews"] = int(notebook.find("p", class_ = "pull-right").text.split("reviews")[0])
            lenovo["stars"] = len(notebook.find_all("span", class_ = "glyphicon glyphicon-star"))

            lenovo["full_description"] = notebook.find("p", class_ = "description").text
            components = lenovo["full_description"].split(",")
            lenovo["name"] = components[0]
            if " Black" in lenovo["full_description"]:
                lenovo["resolution"] = components[2].strip()
                lenovo["processor"] = components[3].strip()
                lenovo["ram"] = components[4].strip()
                lenovo["memory"] = components[5].strip()
            else:
                lenovo["resolution"] = components[1].strip()
                lenovo["processor"] = components[2].strip()
                lenovo["ram"] = components[3].strip()
                lenovo["memory"] = components[4].strip()
            lenovo["graphic_card"] = components[5].strip() if 6 < len(components) else ""

            if "keyboard" in lenovo["full_description"] or "kbd" in lenovo["full_description"]:
                lenovo["o_system"] = components[-2].strip()
                lenovo["keyboard"] = components[-1].strip()
            else:
                lenovo["o_system"] = components[-1].strip()
                lenovo["keyboard"] = ""

            lenovo_list.append(lenovo)

    return lenovo_list

app = flask.Flask(__name__)

@app.route('/lenovo', methods = ['GET'])
def home():
    return jsonify(get_lenovo_list())

app.run()