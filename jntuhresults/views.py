from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from jntuhresults.Executables.jntuhresultscraper import ResultScraper
from jntuhresults.Executables import Search_by_Roll_number
from jntuhresults.Executables.constants import Index_Keys
import asyncio
import time
from django.views.generic import View

listi=['1-1','1-2','2-1','2-2','3-1','3-2','4-1','4-2']
JNTUH_Results={}
#Page Not Found Redirect

def page_not_found_view(request, exception):
    return redirect('/api/single?htno=18E51A0479')
    
#Multi-----------------------------------------------------------------------------------------------------
class multi(View):
    async def gettingurl(self,htno,fro,to,code):
        tasksi=[]
        First_Index,Last_Index=Index_Keys.index(fro),Index_Keys.index(to)
        Index_List=Index_Keys[First_Index:Last_Index+1]
        for i in Index_List:
            Result=Search_by_Roll_number.Results()
            tasksi.append(asyncio.create_task(Result.getting_faster_Grades(htno+i,code)))
        responses = asyncio.gather(*tasksi)
        return await responses

    def get(self,request):
        global listi
        try:
            htno1=request.GET.get('from').upper()
            htno2=request.GET.get('to').upper()
            code=request.GET.get('code').upper()
            return HttpResponse("currently this feature is not available")
        except:
            return HttpResponse("Pass from and to roll number as query")
        if(code not in listi):
            return HttpResponse("Please put down the correct code")
        if(htno1[:8]!=htno2[:8]):
            return HttpResponse("Please Maintain from roll number first and last numbers as same")
        elif(htno1[8:]>htno2[8:]):
            return HttpResponse("First Hall ticket should be greater")
        elif(len(htno1)!=10 or len(htno2)!=10):
            return HttpResponse("Please Enter the Roll Numbers correctly")
        res=asyncio.run(self.gettingurl(htno1[:8],htno1[8:],htno2[8:],code))
        response=list()
        for i in res:
            if(len(i['Results'][code])==0):
                del i   
            else:
                response.append(i)
        return JsonResponse(response,safe=False)
#----------------------------------------------------------------------------------------------------------------



#academicresult------------------------------------------------------------------------------------------------------------

class academicResult(View):
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
                print(htno,result['Details']['NAME']," ",stopping-starting)

                del jntuhresult
                # Return the result
                return JsonResponse(result,safe=False)
        
        except Exception as e:
            print(htno,e)
            # Catch any exceptions raised during scraping
            return HttpResponse(htno+" - 500 Internal Server Error")
           
#------------------------------------------------------------------------------------------------------------------
