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
    return redirect('/')

#Home Page request
async def index(request):
    # return redirect("https://www.djangoproject.com")
    return render(request,'index.html',{'a_dic':a_dic})


#Multi Results of One semester
async def MultiRollNumber(request):
    Params=request.GET.dict() if(request.method=='GET') else request.POST.dict()
    first,last,roll,code=Params["First_Roll_Last_Digits"],Params["Last_Roll_Last_Digits"],Params["First_Roll"],Params["code"]
    First_Index,Last_Index=Index_Keys.index(first),Index_Keys.index(last)
    Index_List=Index_Keys[First_Index:Last_Index+1]
    return render(request,'MultiRollNumber.html',{'roll':roll.upper(),'dict':Index_List,'code':code}) if(last>=first) else HttpResponse("Enter the valid details") 


#Results of All semester of One Roll Number
async def SingleRollNumber(request):
    Roll=request.GET.get('Roll') if(request.method=='GET') else request.POST.get('Roll')
    regular=True
    if(Roll[4]=='5'):
        regular=False
    return render(request,'SingleRollNumber.html',{'roll':Roll,'regular':regular})
    
    

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










#Temp code..........................................................................................................................
async def TempMultiRollNumber(request):
    deta={}
    deta.clear()
    CollegeCode=request.GET.get('CollegeCode')
    print(CollegeCode)
    BranchCode=request.GET.get('Branch')
    print(BranchCode)
    Regulation=request.GET.get('Regulation')
    print(Regulation)
    roll=Regulation+CollegeCode+'1A'+BranchCode
    lateral_roll=str(int(Regulation)+1)+CollegeCode+'5A'+BranchCode
    print(lateral_roll)
    code='2-1'
    firsti=Index_Keys.index("01")
    lasti=Index_Keys.index("Z0")
    dict=Index_Keys[firsti:lasti+1]
    # roll_first=roll+first
    # roll_last=roll+last
    # print("Results from",roll_first," to",roll_last)
    return render(request,'tempMultiRollNumber.html',{'roll':roll,'dict':dict,'code':code,'lateral_roll':lateral_roll})


def temp(request):
    print("yes")
    with open('jntuhresults/Json/college_codes.json') as fp:
        College_codes = json.load(fp)
    with open('jntuhresults/Json/Branch_codes.json') as fp:
        Branch_codes = json.load(fp)
    return render(request,'temp.html',{'College_codes':College_codes,'Branch_Codes':Branch_codes})
#..........................................................................................................................