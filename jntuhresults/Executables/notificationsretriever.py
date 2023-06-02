import requests
from bs4 import BeautifulSoup


def get_notifications():
    url = "http://results.jntuh.ac.in/jsp/home.jsp"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    btech_results = soup.find_all("table")[0].find_all("tr")
    results=[]
    for result in btech_results:
        result_link = result.find_all("td")[0].find_all("a")[0]["href"]
        result_text = result.get_text()
        result_text_index=result_text.find("Results")+7
        json_appendded={
            "Result_title":result_text[:result_text_index],
            "Link":"http://results.jntuh.ac.in"+result_link,
            "Date":result_text[result_text_index:]
        }
        results.append(json_appendded)  
    return results
