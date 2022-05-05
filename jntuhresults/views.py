from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse
from requests.sessions import Request
import string
from . import Search_by_Roll_number


def page_not_found_view(request, exception):
    return redirect('/')

a_dic={'0'+str(i):'0'+str(i) for i in range(1,10)}
for i in range(10,100):
    a_dic[str(i)]=str(i) 
 
for letter in string.ascii_uppercase:
    for i in range(0,10):
        a_dic[letter+str(i)]=letter+str(i)
lolli=list(a_dic.keys())

#index request
def index(request):
    return render(request,'index.html',{'a_dic':a_dic})


def results(request):
    
    if(request.method == 'GET'):
        return redirect('/')
    deta={}
    deta.clear()
    air=request.POST.dict()
    first=air["first"]
    last=air["last"]
    roll=air["firsti"]
    code=air["code"]
    print(code)
    firsti=lolli.index(first)
    lasti=lolli.index(last)
    dict=lolli[firsti:lasti]
    print(dict)
    if(last<=first):
            return HttpResponse("Enter the valid details")
    return render(request,'manyroll.html',{'roll':roll,'dict':dict,'code':code})

# getting the one roll details
def oneroll(request):
    
    if(request.method == 'GET'):
        return redirect('/')
    air=request.POST.dict()
    roll=air["roll"]
    return render(request,'oneroll.html',{'roll':roll})

#snippet of code
def gettingurl(request,htno,code):
    deta={}
    deta=Search_by_Roll_number.the_loaderi(htno,code)
    b=bool(deta[code])
    if(b==False):
        return HttpResponse("")
    return render(request,'snippet.html',{'deta':deta})
