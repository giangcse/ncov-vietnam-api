import requests
import re
import json
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)


@app.route('/ncov', methods=['GET'])
def index():
    url = "https://ncov.moh.gov.vn/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}
    try:
        # Turn off verify for SSL
        _r = requests.get(url, headers=header, verify=False)
        soup = BeautifulSoup(_r.content, "html.parser")
        all = soup.find("div", {"class": "pt-2"}).get_text()
        str_list = re.split('|\r|\t|', all)  # Delete all escape character
        my_str = ""
        for i in str_list:
            my_str += i
        my_str = my_str.strip()  # Delete any space character in string
        my_str = my_str.split("\n")  # Delete all newline character in string

        # Two loops for remove null character
        for c in my_str:
            if c == "":
                my_str.remove(c)

        for c in my_str:
            if c == "":
                my_str.remove(c)
        # Result: ['Việt Nam', 'Số ca nhiễm 11.635', 'Đang điều trị 6.980', 'Khỏi 4.590', 'Tử vong 61', 'Thế giới', 'Tổng ca nhiễm 177.786.258', 'Đang nhiễm 11.654.173', '', 'Khỏi 162.283.936', '', '', 'Tử vong 3.848.149']

        my_dict = {"Việt Nam": [{"Ca nhiễm": my_str[1][my_str[1].rindex(" "):], "Đang điều trị": my_str[2][my_str[2].rindex(" "):], "Khỏi": my_str[3][my_str[3].rindex(" "):], "Tử vong": my_str[4][my_str[4].rindex(
            " "):]}], "Thế giới": [{"Ca nhiễm": my_str[6][my_str[6].rindex(" "):], "Đang nhiễm": my_str[7][my_str[7].rindex(" "):], "Khỏi": my_str[9][my_str[9].rindex(" "):], "Tử vong": my_str[12][my_str[12].rindex(" "):]}]}
        return json.dumps(my_dict)
    except ConnectionError:
        print("Loi ket noi den may chu")
