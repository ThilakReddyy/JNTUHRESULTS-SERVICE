import requests
from bs4 import BeautifulSoup

#default parameters-----------------------
headers = {
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
url = "http://results.jntuh.ac.in/resultAction"
dicti={'O':10,'A+':9,'A':8,'B+':7,'B':6,'C':5,'F':0,'Ab':0}
arr11=[1323,1358,1404,1430,1467,1504]
arr12=[1356,1381,1435,1448,1481,1503]
arr21=[1391,1425,1449,1496,1560]
arr22=[1437,1447,1476,1501,1565]
arr31=[1454,1491,1550]
arr32=[1502,1555]
arr41=[1545]
arr42=[]
#-----------------------------------------------------------------------

class Results_Extracter:
    def __init__(self):
        self.deta={}
        self.deta.clear()
    #Getting the data from jntuh website--------------------------------
    def getting_the_grades(self,payload,roll):
        try:
            r = requests.request("POST", url, headers=headers, data=payload)
            soup = BeautifulSoup(r.content, "html.parser")
            table = soup.find_all("table")
            table1 = table[0].find_all("tr")
            Roll_NO = table1[0].find_all("td")[1].find_all("b")[0].contents[0]
            NAME = table1[0].find_all("td")[3].find_all("b")[0].contents[0]
            print(Roll_NO,end=" - ")
            print(NAME)
            FATHER_NAME = table1[1].find_all("td")[1].find_all("b")[0].contents[0]
            COLLEGE_CODE = table1[1].find_all("td")[3].find_all("b")[0].contents[0]
            table2 = table[1].find_all("tr")
            table2_column_names = [content.text for content in table2[0].findAll('b')]
            
            grade_index = table2_column_names.index("GRADE")
            subject_name_index = table2_column_names.index("SUBJECT NAME")
            subject_code_index = table2_column_names.index("SUBJECT CODE")
            subject_credits_index = table2_column_names.index("CREDITS(C)")
            
            table2 = table2[1:]
            
            self.deta[roll]["DETAILS"] = {"NAME": NAME, "Roll_No": Roll_NO, "COLLEGE_CODE": COLLEGE_CODE}
            
            
            for row in table2:
                subject_name = row.find_all("td")[subject_name_index].find("b").contents[0]
                subject_code = row.find_all("td")[subject_code_index].find("b").contents[0]
                subject_grade = row.find_all("td")[grade_index].find("b").contents[0]
                subject_credits = row.find_all("td")[subject_credits_index].find("b").contents[0]
                
                self.deta[roll][subject_code]={}
                self.deta[roll][subject_code]["subject_name"]=subject_name
                self.deta[roll][subject_code]["subject_code"]=subject_code
                self.deta[roll][subject_code]["subject_grade"]=subject_grade
                self.deta[roll][subject_code]["subject_credits"]=subject_credits
            return self.deta   
        except:
            pass
    #-----------------------------------------------------------------------
    def gradeCalculator(self,value):
        total,credits=0,0
        for data in value:
            if('DETAILS' in data):
                pass
            else:
                if(value[data]['subject_grade']=='F' or value[data]['subject_grade']=='Ab'):
                    return ""
                total=total+int(dicti[value[data]['subject_grade']])*float(value[data]['subject_credits'])
                credits=credits+float(value[data]['subject_credits'])
        return "{0:.2f}".format(round(total/credits,2))

def the_loaderi(roll,code):
    roll=roll.upper()
    extract=Results_Extracter()
    extract.deta[code]={}
    if(code=='1-1'):
        for i in arr11:
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=null&type=null&htno="+roll,code)
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=gradercrv&type=rcrvintgrade&htno="+roll,code)
    if(code=='1-2'):
        for i in arr12:
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=null&type=null&htno="+roll,code)
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=gradercrv&type=rcrvintgrade&htno="+roll,code)
    if(code=='2-1'):
        for i in arr21:
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=null&type=null&htno="+roll,code)
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=gradercrv&type=rcrvintgrade&htno="+roll,code)
    if(code=='2-2'):
        for i in arr22:
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=null&type=null&htno="+roll,code)
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=gradercrv&type=rcrvintgrade&htno="+roll,code)
    if(code=='3-1'):
        for i in arr31:
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=null&type=null&htno="+roll,code)
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=gradercrv&type=rcrvintgrade&htno="+roll,code)
    if(code=='3-2'):
        for i in arr32:
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=null&type=null&htno="+roll,code)
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=gradercrv&type=rcrvintgrade&htno="+roll,code)
    if(code=='4-1'):
        for i in arr41:
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=null&type=null&htno="+roll,code)
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=gradercrv&type=rcrvintgrade&htno="+roll,code)
    if(code=='4-2'):
        for i in arr42:
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=null&type=null&htno="+roll,code)
            extract.getting_the_grades("degree=btech&examCode="+str(i)+"&etype=r17&result=null&grad=gradercrv&type=rcrvintgrade&htno="+roll,code)
    value=extract.deta[code]
    try:
        extract.deta[code]['TOTAL']=extract.gradeCalculator(value)
    except:
        pass
    return extract.deta


