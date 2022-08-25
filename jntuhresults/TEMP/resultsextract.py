import requests
from bs4 import BeautifulSoup
url = "http://results.jntuh.ac.in/jsp/home.jsp"


response = requests.request("GET", url)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find_all("table")
table=table[0]
tr = table.find_all("tr",text="")
for i in tr:
    if("R18" in i.get_text()):
        print(i.get_text())
        el = i.find(href=True)
        print(el["href"])


