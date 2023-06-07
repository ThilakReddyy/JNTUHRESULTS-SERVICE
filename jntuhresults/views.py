import asyncio
import time
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from jntuhresults.Executables.jntuhresultscraper import ResultScraper
from django.views.generic import View
from jntuhresults.Executables.notificationsretriever import get_notifications


# Class Result ----------------------------------------------------------------------
class ClassResult(View):
    async def scrape_results_async(self, htno, semester):
        # Create an instance of ResultScraper
        jntuhresult = ResultScraper(htno.upper())
        
        # Scrape all the results asynchronously
        result = await jntuhresult.scrape_all_results(semester)
        
        return result

    async def get(self, request):
        # Retrieve htnos and semester from the GET parameters
        htnos = request.GET.get('htnos').split(",")
        semester = request.GET.get('semester')
        
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

#----------------------------------------------------------------------------------------------------------------



#academicresult------------------------------------------------------------------------------------------------------------

class AcademicResult(View):
    def get(self,request):
        starting =time.time()    

        htno=request.GET.get('htno').upper()
        # Check if the hall ticket number is valid
        if len(htno) != 10:
            return HttpResponse(htno+" Invalid hall ticket number")
        try:
                # Create an instance of ResultScraper
                jntuhresult = ResultScraper(htno.upper())

                # Run the scraper and return the result
                result = jntuhresult.run()
                
                # Calculate the total marks and credits
                total_credits = 0  # Variable to store the total credits
                total = 0  # Variable to store the total marks
                failed = False  # Flag to indicate if any value is missing 'total' key

                # Iterate over the values in result["Results"] dictionary
                for value in result["Results"].values():
                    if 'total' in value.keys():  # Check if the current value has 'total' key
                        total += value['total']  # Add the 'total' value to the total marks
                        total_credits += value['credits']  # Add the 'credits' value to the total credits
                    else:
                        failed = True  # Set the flag to indicate missing 'total' key

                # Calculate the CGPA if there are non-zero credits
                if not failed:
                    result["Results"]["Total"] = "{0:.2f}".format(round(total/total_credits,2))

                stopping=time.time()
                print(htno,result['Details']['NAME'],stopping-starting)

                del jntuhresult
                # Return the result
                return JsonResponse(result,safe=False)
        
        except Exception as e:
            print(htno,e)
            # Catch any exceptions raised during scraping
            return HttpResponse(htno+" - 500 Internal Server Error")
           
#------------------------------------------------------------------------------------------------------------------


#- Notifications -------------------------------------------------------------------------------------------------
class Notification(View):
    def get(self,request):
        try:
            return JsonResponse(get_notifications(),safe=False)
        except Exception as e:
            return HttpResponse(e)
    
#---------------------------------------------------------------------------------------------------------------

def homepage(request):
    return render(request,'index.html')