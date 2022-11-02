import string
# from jntuhresults.Executables.examcodes import *  
#default parameters-----------------------
headers = {
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
# url = "http://results.jntuh.ac.in/resultAction"
url=["http://202.63.105.184/results/resultAction","http://results.jntuh.ac.in/resultAction"]

grades_to_gpa={'O':10,'A+':9,'A':8,'B+':7,'B':6,'C':5,'F':0,'Ab':0}

#R18 Semester codes
arr11=[1323,1358,1404,1430,1467,1504,1572]
arr12=[1356,1363,1381,1435,1448,1481,1503,1570]
arr21=[1391,1425,1449,1496,1560]
arr22=[1437,1447,1476,1501,1565,1605]
arr31=[1454,1491,1550,1590]
arr32=[1502,1555,1595]
arr41=[1545,1585]
arr42=[1580,1600]

# payloads=["&etype=r17&result=null&grad=null&type=null&htno=","&etype=r17&result=gradercrv&grad=null&type=rcrvintgrade&htno="]
payloads=["&etype=r17&result=null&grad=null&type=intgrade&htno=","&etype=r17&result=gradercrv&grad=null&type=rcrvintgrade&htno="]


#Exam Codes-----------------------------------------------------------
def exam_codes(code,htno):
    if (code =="1-1"):
        return arr11
    elif(code =="1-2"):
        return arr12
    elif(code =="2-1"):
        return arr21
    elif(code =="2-2"):
        return arr22
    elif(code =="3-1"):
        return arr31
    elif(code =="3-2"):
        return arr32
    elif(code =="4-1"):
        return arr41
    elif(code =="4-2"):
        return arr42


a_dic={'0'+str(i):'0'+str(i) for i in range(1,10)}
for i in range(10,100):
    a_dic[str(i)]=str(i) 
 
for letter in string.ascii_uppercase:
    for i in range(0,10):
        a_dic[letter+str(i)]=letter+str(i)
Index_Keys=list(a_dic.keys())
#-----------------------------------------------------------------------
