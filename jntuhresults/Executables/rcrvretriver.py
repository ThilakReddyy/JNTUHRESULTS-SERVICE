from bs4 import BeautifulSoup
import requests


response = requests.get("http://results.jntuh.ac.in/jsp/RCRVInfo.jsp")
soup = BeautifulSoup(response.content, "html.parser")
rcrvs = soup.find_all("h3")
results = []
for rcrv in rcrvs:
    try:
        splitedrcrv = rcrv.get_text().split(" ")[1:]

        splitedone = ""
        for splitted in splitedrcrv:
            if "-20" in splitted:
                splitedone = splitted[0:10]
        result = {
            "release data": rcrv.get_text().split(" ")[0].split("(")[1].split(")")[0],
            "rcrv valuation": splitedone,
        }

        results.append(result)
    except Exception as e:
        print(e)
        print(rcrv.get_text().split(" ")[1].split("(")[1].split(")")[0])
print(results)
