from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from asgiref.sync import sync_to_async
from jntuhresults.Executables import Search_by_Roll_number
from jntuhresults.Executables.constants import a_dic,Index_Keys
import json
import asyncio
import time
listi=['1-1','1-2','2-1','2-2','3-1','3-2','4-1','4-2']

#Page Not Found Redirect
def page_not_found_view(request, exception):
    return redirect('/allResults?htno=18E51A0479')
    

#Multi-----------------------------------------------------------------------------------------------------
async def gettingurl(htno,fro,to,code):
    tasksi=[]
    First_Index,Last_Index=Index_Keys.index(fro),Index_Keys.index(to)
    Index_List=Index_Keys[First_Index:Last_Index+1]
    for i in Index_List:
        Results=Search_by_Roll_number.Results()
        tasksi.append(asyncio.create_task(Results.getting_faster_Grades(htno+i,code)))
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
    return JsonResponse(res,safe=False)
#----------------------------------------------------------------------------------------------------------------



#single------------------------------------------------------------------------------------------------------------
async def allResults_extend(htno):
    global listi
    if(htno[4]=='5'):
        listi=listi[2:]
    tasksi=[]
    for i in listi:
        Results=Search_by_Roll_number.Results()
        tasksi.append(asyncio.create_task(Results.getting_faster_Grades(htno,i)))
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
    json_object = asyncio.run(allResults_extend(htno))
    Results={}
    Results['Details']={}
    Results['Results']={}
    for i in json_object:   
        try:
            for ind in i['Results']:
                Results['Results'][ind]=i['Results'][ind]
                Results['Details']=i['DETAILS']
        
        except:
            del Results['Results'][ind]
    stopping=time.time()
    print(stopping-starting)
    return JsonResponse(Results,safe=False)
#------------------------------------------------------------------------------------------------------------------