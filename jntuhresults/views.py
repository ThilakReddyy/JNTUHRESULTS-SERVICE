import asyncio
import time
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from jntuhresults.Executables.jntuhresultscraper import ResultScraper
from jntuhresults.Executables.jntuhallresultsscraper import ResultScraperr
from django.views.generic import View
from jntuhresults.Executables.notificationsretriever import get_notifications
import redis
import json
from datetime import timedelta
import os
from dotenv import load_dotenv


load_dotenv()
REDIS_URL = os.environ.get("REDIS_URL")
REDIS_CLIENT = redis.from_url(str(REDIS_URL))


# Class Result ----------------------------------------------------------------------
class ClassResult(View):
    async def scrape_results_async(self, htno, semester):
        HTTP_REFERER = requests.META.get("HTTP_REFERER")
        if HTTP_REFERER is None:
            return HttpResponse(" meta data error")
        print(HTTP_REFERER)

        # Create an instance of ResultScraper
        jntuhresult = ResultScraper(htno.upper())

        # Scrape all the results asynchronously
        result = await jntuhresult.scrape_all_results(semester)

        return result

    async def get(self, request):
        # Retrieve htnos and semester from the GET parameters
        htnos = request.GET.get("htnos").split(",")
        semester = request.GET.get("semester")

        # Print htnos for debugging

        print(htnos)

        # Create a list to hold the tasks
        tasks = []

        # Add the tasks to the list
        for htno in htnos:
            # Create a task for scraping results asynchronously for each htno
            task = asyncio.create_task(self.scrape_results_async(htno, semester))
            tasks.append(task)

        # Await all the tasks to complete
        gathered_results = await asyncio.gather(*tasks)

        # Filter out the empty results
        filtered_results = [result for result in gathered_results if result["Details"]]

        # Return the results as a JSON response
        return JsonResponse(filtered_results, safe=False)


# ----------------------------------------------------------------------------------------------------------------

# check which url is working ------------------------------------------------


def check_url(index, roll_number):
    try:
        urls = [
            "http://202.63.105.184/results/resultAction?degree=btech&examCode=1323&etype=r16&result=null&grad=null&type=intgrade&htno=18E51A0479",
            "https://results.jntuh.ac.in/results/resultAction?degree=btech&examCode=1323&etype=r16&result=null&grad=null&type=intgrade&htno=18E51A0479",
        ]
        response = requests.get(urls[index], timeout=2)
        print(response.status_code, roll_number)
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print(f"Requests to {index} timeout ")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Requests to {index} failed: {e}")
        return False


# -----------------------------------------------------------------------------------------------------------------
# academicresult------------------------------------------------------------------------------------------------------------


class AcademicResult(View):
    def get(self, request):
        # Record the current time as the starting time
        starting = time.time()

        # Get the 'htno' parameter from the request and convert it to uppercase
        htno = request.GET.get("htno").upper()

        # Retrieve data from Redis cache using the 'htno' as the key
        redis_response = REDIS_CLIENT.get(htno)

        # Check if data exists in the Redis cache
        if redis_response is not None:
            # If data exists, parse the JSON response
            data = json.loads(redis_response)
            # redis_client.expire(htno, timedelta(seconds=1))
            # Record the current time as the stopping time
            stopping = time.time()

            # Print relevant details (e.g., 'htno', student name, and execution time)
            print(htno, data["data"]["Details"]["NAME"], stopping - starting)

            # Return the data as a JSON response to the client
            return JsonResponse(data["data"], safe=False)

        url_index = 1
        if check_url(url_index, htno) is not True:
            if check_url(0, htno) is not True:
                return HttpResponse(b"JNTUH Servers are down!!!", status=422)
            else:
                url_index = 1
        # Check if the hall ticket number is valid
        if len(htno) != 10:
            return HttpResponse(htno + " Invalid hall ticket number")
        try:
            # Create an instance of ResultScraper
            jntuhresult = ResultScraper(htno.upper(), url_index)

            # Run the scraper and return the result
            result = jntuhresult.run()

            # Calculate the total marks and credits
            total_credits = 0  # Variable to store the total credits
            total = 0  # Variable to store the total marks
            failed = False  # Flag to indicate if any value is missing 'total' key

            # Iterate over the values in result["Results"] dictionary
            if result is not None:
                for value in result["Results"].values():
                    if (
                        "total" in value.keys()
                    ):  # Check if the current value has 'total' key
                        total += value[
                            "total"
                        ]  # Add the 'total' value to the total marks
                        total_credits += value[
                            "credits"
                        ]  # Add the 'credits' value to the total credits
                    else:
                        failed = True  # Set the flag to indicate missing 'total' key

                # Calculate the CGPA if there are non-zero credits
                if not failed:
                    result["Results"]["Total"] = "{0:.2f}".format(
                        round(total / total_credits, 2)
                    )

            # Record the current time as the stopping time
            stopping = time.time()

            if result is not None:
                # Print relevant details (e.g., 'htno', student name, and execution time)
                print(htno, result["Details"]["NAME"], stopping - starting)

            # Delete the variable 'jntuhresult' from memory
            del jntuhresult

            # Store the 'result' data in the Redis cache with the 'htno' as the key.
            REDIS_CLIENT.set(htno, json.dumps({"data": result}))

            # Set an expiration time of 4 hours for the cached data associated with 'htno'.
            REDIS_CLIENT.expire(htno, timedelta(hours=1))

            # Return the result
            return JsonResponse(result, safe=False)

        except Exception as e:
            print(htno, e)
            # Catch any exceptions raised during scraping
            return HttpResponse(htno + " - 500 Internal Server Error")


# ------------------------------------------------------------------------------------------------------------------


# - Notifications -------------------------------------------------------------------------------------------------
class Notification(View):
    def get(self, request):
        notifications = get_notifications()
        REDIS_CLIENT.set("notifications", json.dumps({"data": notifications}))
        REDIS_CLIENT.expire("notifications", timedelta(hours=1))

        return JsonResponse({"data": notifications}, safe=False)
        # return JsonResponse({"data": "Notifications have been fetched"}, safe=False)


# ---------------------------------------------------------------------------------------------------------------


class AcademicAllResults(View):
    def get(self, request):
        starting = time.time()
        htno = request.GET.get("htno").upper()
        index = 1

        return HttpResponse(htno + " - 500 Internal Server Error")
        # if check_url(0, htno):
        #     index = 0
        # if not check_url(index, htno):
        #     return HttpResponse(htno + " - Server Busy")
        jntuhresult = ResultScraperr(htno.upper(), index)
        redis_response = REDIS_CLIENT.get(htno + "ALL")
        redis_response = None

        # Check if data exists in the Redis cache
        if redis_response is not None:
            # If data exists, parse the JSON response
            data = json.loads(redis_response)
            # redis_client.expire(htno, timedelta(seconds=1))
            # Record the current time as the stopping time
            stopping = time.time()

            # Print relevant details (e.g., 'htno', student name, and execution time)
            print(htno, data["data"]["Details"]["NAME"], stopping - starting)

            # Return the data as a JSON response to the client
            return JsonResponse(data["data"], safe=False)

        # Run the scraper and return the result
        result = jntuhresult.run()
        if result is not None:
            if result["Details"]:
                results = result["Results"]
                sorted_results = {
                    outer_key: dict(sorted(inner_dict.items()))
                    for outer_key, inner_dict in sorted(results.items())
                }

                result["Results"] = sorted_results
                REDIS_CLIENT.set(htno + "ALL", json.dumps({"data": result}))
                REDIS_CLIENT.expire(htno + "ALL", timedelta(hours=6))

                stopping = time.time()
                print(htno, result["Details"]["NAME"], stopping - starting)

                return JsonResponse({"data": result}, safe=False)

        stopping = time.time()
        print(htno, stopping - starting, "Failed")
        return HttpResponse(htno + " - 500 Internal Server Error")


def homepage(request):
    return render(request, "index.html")


def test(request):
    return render(request, "test.html")
