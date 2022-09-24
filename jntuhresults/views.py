from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from asgiref.sync import sync_to_async
from jntuhresults.Executables import Search_by_Roll_number
from jntuhresults.Executables.constants import a_dic,Index_Keys
import json
import asyncio
import time

#Page Not Found Redirect
def page_not_found_view(request, exception):
    return redirect('/allResults?htno=18E51A0479')

#Home Page request
    

#Actual Snippet Which Returns Results

async def gettingurl(request,htno,code):
    Results=Search_by_Roll_number.Results()
    deta=Results.get_grade_start(htno.upper(),code)
    del Results
    return render(request,'snippet.html',{'deta':deta}) if(bool(deta['Results'][code])) else HttpResponse("")


async def allResults_extend(htno):
    listi=['1-1','1-2','2-1','2-2','3-1','3-2','4-1','4-2']
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
    htno=request.GET.get('htno').upper()
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
    # calculate_cgpa=Search_by_Roll_number.get_cgpa(Results['Results'])
    stopping=time.time()
    print(stopping-starting)
    return JsonResponse(Results,safe=False)
