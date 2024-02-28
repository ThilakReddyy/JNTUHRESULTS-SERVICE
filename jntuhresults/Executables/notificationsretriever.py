import requests
import redis
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


load_dotenv()
redis_url = os.environ.get("REDIS_URL")
redis_client = redis.from_url(str(redis_url))


def get_notifications():
    # Load environment variables from .env file

    #    redis_response = redis_client.get("notifications")
    # if redis_response is not None:
    #    data = json.loads(redis_response)
    #    return data["data"]
    try:
        url = "http://results.jntuh.ac.in/jsp/home.jsp"
        # url = "http://202.63.105.184/results/jsp/home.jsp"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        results = []
        for i in range(0, 8):
            jntuh_notifications = soup.find_all("table")[i].find_all("tr")

            for result in jntuh_notifications:
                result_link = result.find_all("td")[0].find_all("a")[0]["href"]
                result_text = result.get_text()
                result_text_index = result_text.find("Results") + 7
                json_appendded = {
                    "Result_title": result_text[:result_text_index],
                    "Link": "http://results.jntuh.ac.in" + result_link,
                    "Date": result_text[result_text_index:],
                }
                results.append(json_appendded)
        month_map = {
            "JAN": 0,
            "FEB": 1,
            "MAR": 2,
            "APR": 3,
            "MAY": 4,
            "JUN": 5,
            "JUL": 6,
            "AUG": 7,
            "SEP": 8,
            "OCT": 9,
            "NOV": 10,
            "DEC": 11,
        }
        new_results = []
        for result in results:
            try:
                day, month, year = result["Date"].split("-")
                month_abbreviation = str(month)[:3].upper()
                month_index = month_map[month_abbreviation]
                formatted_date = datetime(int(year), month_index + 1, int(day))
                result["formatted_date"] = formatted_date.strftime("%Y-%m-%d")
                new_results.append(result)
            except Exception as e:
                print(result, e)
        results = new_results
        results.sort(key=lambda x: x["formatted_date"], reverse=True)
        redis_client.set("notifications", json.dumps({"data": results}))
        redis_client.expire("notifications", timedelta(minutes=120))
        return results
    except Exception as e:
        print(e)
