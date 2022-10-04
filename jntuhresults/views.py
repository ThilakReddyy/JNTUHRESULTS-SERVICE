from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from asgiref.sync import sync_to_async
from jntuhresults.Executables import Search_by_Roll_number
from jntuhresults.Executables.constants import a_dic,Index_Keys
import json
import asyncio
import time
from datetime import datetime
listi=['1-1','1-2','2-1','2-2','3-1','3-2','4-1','4-2']
JNTUH_Results={}
#Page Not Found Redirect
def page_not_found_view(request, exception):
    return redirect('/api/single?htno=18E51A0479')
    
def cors(request):
    return HttpResponse("hello")
#Multi-----------------------------------------------------------------------------------------------------
async def gettingurl(htno,fro,to,code):
    tasksi=[]
    First_Index,Last_Index=Index_Keys.index(fro),Index_Keys.index(to)
    Index_List=Index_Keys[First_Index:Last_Index+1]
    for i in Index_List:
        tasksi.append(asyncio.create_task(Search_by_Roll_number.getting_faster_Grades(htno+i,code)))
    responses = asyncio.gather(*tasksi)
    return await responses

async def multi(request):
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
    res=asyncio.run(gettingurl(htno1[:8],htno1[8:],htno2[8:],code))
    response=list()
    for i in res:
        if(len(i['Results'][code])==0):
            del i   
        else:
            response.append(i)
    return JsonResponse(response,safe=False)
#----------------------------------------------------------------------------------------------------------------



#single------------------------------------------------------------------------------------------------------------
async def allResults_extend(htno):
    global listi
    listE=listi
    if(htno[4]=='5'):
        listE=listi[2:]
    tasksi=[]
    for i in listE:
        tasksi.append(asyncio.create_task(Search_by_Roll_number.getting_faster_Grades(htno,i)))
    responses = asyncio.gather(*tasksi)
    return await responses


#API for getting all Results
async def allResults(request):
    starting =time.time()
    try:
        htno=request.GET.get('htno').upper()
        print(htno)
    except:
        return HttpResponse('Enter hallticket number correctly')
    try:
        return JsonResponse(JNTUH_Results[htno],safe=False)
    except:
        print("Not loaded from cache")
    try:
        json_object = asyncio.run(allResults_extend(htno))
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
    JNTUH_Results[htno]=Results
    return JsonResponse(Results,safe=False)
#------------------------------------------------------------------------------------------------------------------