from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from asgiref.sync import sync_to_async
from jntuhresults.Executables import Search_by_Roll_number
from jntuhresults.Executables.jntuhresultscraper import ResultScraper
from jntuhresults.Executables.constants import a_dic,Index_Keys
import json
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



#single------------------------------------------------------------------------------------------------------------
class allResults(View):
    async def allResults_extend(self,htno):
            global listi
            listE=listi
            if(htno[4]=='5'):
                listE=listi[2:]
            tasksi=[]
            for i in listE:
                Result=Search_by_Roll_number.Results()
                tasksi.append(asyncio.create_task(Result.getting_faster_Grades(htno,i)))
            responses = asyncio.gather(*tasksi)
            return await responses

    #API for getting all Results
    def get(self,request):
        print(request.META.get("HTTP_USER_AGENT"))
        starting =time.time()
        try:
            htno=request.GET.get('htno').upper()
            print(htno)
        except:
            return HttpResponse('Enter hallticket number correctly')
        try:
            Result=JNTUH_Results[htno]
            stopping=time.time()
            print(stopping-starting)
            print("Loaded from cache")
            return JsonResponse(Result,safe=False)
        except:
            print("Not loaded from cache")
        try:
            json_object = asyncio.run(self.allResults_extend(htno))
        except:
            print("Failed")
            return HttpResponse("Not working correctly",status=400)
        Results={}
        Results['Details']={}
        Results['Results']={}
        total=0
        credits=0
        all_pass=True
        for i in json_object:   
            try:
                for ind in i['Results']:
                    Results['Results'][ind]=i['Results'][ind]
                    Results['Details']=i['DETAILS']
                    try:
                        total=total+i['Results'][ind]['total']
                        credits=credits+i['Results'][ind]['credits']
                    except:
                        all_pass=False
            except:
                del Results['Results'][ind]
        try:
            print(Results['Details']['NAME'])
        except:
            pass
        if(all_pass):
            Results['Results']['Total']="{0:.2f}".format(round(total/credits,2))
        stopping=time.time()
        print(stopping-starting)
        #JNTUH_Results[htno]=Results
        return JsonResponse(Results,safe=False)
    
class academicResult(View):
    def get(self,request):
        # Check if the university code is 'jntuh'
        htno=request.GET.get('htno').upper()
        # Check if the hall ticket number is valid
        if len(htno) != 10:
            return HttpResponse("Invalid hall ticket number")

            # Create an instance of ResultScraper
        jntuhresult = ResultScraper(htno.upper())

        try:
                # Run the scraper and return the result
                result = jntuhresult.run()

                # Calculate the total marks and credits
                total = sum(
                    i.get("total", 0)
                    for i in result["Results"].values()
                    if i.get("credits", 0) != 0
                )
                total_credits = sum(
                    i["credits"]
                    for i in result["Results"].values()
                    if i.get("credits", 0) != 0
                )

                # Calculate the CGPA if there are non-zero credits
                if total_credits != 0:
                    result["CGPA"] = total / total_credits

                # Return the result
                return JsonResponse(result,safe=False)
        except Exception as e:
            # Catch any exceptions raised during scraping
            return HttpResponse("500 Internal Server Error")
           
#------------------------------------------------------------------------------------------------------------------
