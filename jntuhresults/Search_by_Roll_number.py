from bs4 import BeautifulSoup
import time
import asyncio
import aiohttp

#default parameters-----------------------
headers = {
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
url = "http://results.jntuh.ac.in/resultAction"
grades_to_gpa={'O':10,'A+':9,'A':8,'B+':7,'B':6,'C':5,'F':0,'Ab':0}
arr11=[1323,1358,1404,1430,1467,1504]
arr12=[1356,1381,1435,1448,1481,1503]
arr21=[1391,1425,1449,1496,1560]
arr22=[1437,1447,1476,1501,1565]
arr31=[1454,1491,1550]
arr32=[1502,1555]
arr41=[1545]
arr42=[1580]
#-----------------------------------------------------------------------

def exam_codes(code):
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
    else:
        return []



class Results:
    def __init__(self):
        self.deta={}
        self.deta.clear()
        self.tasks=[]

    def get_tasks(self,session,arr,roll):
        for i in arr:
            payload="degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=null&type=null&htno="+roll
            self.tasks.append(session.post(url, data=payload,headers=headers,ssl=False))
        return self.tasks  

    def total_grade_Calculator(self,value):
        total,credits=0,0
        for data in value:
            if('DETAILS' in data):
                pass
            else:
                if(value[data]['subject_grade']=='F' or value[data]['subject_grade']=='Ab'):
                    return ""
                total=total+int(grades_to_gpa[value[data]['subject_grade']])*float(value[data]['subject_credits'])
                credits=credits+float(value[data]['subject_credits'])
        return "{0:.2f}".format(round(total/credits,2)) 
     
    async def getting_the_grades(self,code,roll):
        arr=exam_codes(code)
        async with aiohttp.ClientSession() as session:
            tasks=self.get_tasks(session,arr,roll)
            responses =await asyncio.gather(*tasks)
            self.deta[code]={}
            for response in responses:
                r=await response.text()
                soup = BeautifulSoup(r, "html.parser")
                try:
                    table = soup.find_all("table")
                    table1 = table[0].find_all("tr")
                    Roll_NO = table1[0].find_all("td")[1].find_all("b")[0].contents[0]
                    NAME = table1[0].find_all("td")[3].find_all("b")[0].contents[0]
                    FATHER_NAME = table1[1].find_all("td")[1].find_all("b")[0].contents[0]
                    COLLEGE_CODE = table1[1].find_all("td")[3].find_all("b")[0].contents[0]
                    table2 = table[1].find_all("tr")
                    table2_column_names = [content.text for content in table2[0].findAll('b')]
                    
                    grade_index = table2_column_names.index("GRADE")
                    subject_name_index = table2_column_names.index("SUBJECT NAME")
                    subject_code_index = table2_column_names.index("SUBJECT CODE")
                    subject_credits_index = table2_column_names.index("CREDITS(C)")
                    table2 = table2[1:]
                    self.deta[code]["DETAILS"] = {"NAME": NAME, "Roll_No": Roll_NO, "COLLEGE_CODE": COLLEGE_CODE}
            
            
                    for row in table2:
                        subject_name = row.find_all("td")[subject_name_index].find("b").contents[0]
                        subject_code = row.find_all("td")[subject_code_index].find("b").contents[0]
                        subject_grade = row.find_all("td")[grade_index].find("b").contents[0]
                        subject_credits = row.find_all("td")[subject_credits_index].find("b").contents[0]
                        
                        self.deta[code][subject_code]={}
                        self.deta[code][subject_code]["subject_name"]=subject_name
                        self.deta[code][subject_code]["subject_code"]=subject_code
                        self.deta[code][subject_code]["subject_grade"]=subject_grade
                        self.deta[code][subject_code]["subject_credits"]=subject_credits
                except:
                    pass
        try:
            self.deta[code]["TOTAL"]=self.total_grade_Calculator(self.deta[code])
        except:
            pass
        return self.deta

def get_grade_start(roll,code):
    start =time.time()
    grade=Results()
    url = "http://results.jntuh.ac.in/resultAction"
    result=asyncio.run(grade.getting_the_grades(code,roll))
    stop=time.time()
    print(roll)
    print(stop-start)
    return result

        
                



