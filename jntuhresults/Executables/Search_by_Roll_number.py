from bs4 import BeautifulSoup
import asyncio
import aiohttp
from jntuhresults.Executables.constants import *
import time


class Results:
    def __init__(self):
        self.deta={}
        self.deta.clear()
        self.deta["Results"]={}
        self.tasks=[]

    #Running all the links asynchronously
    def get_tasks(self,session,arr,roll):
        for payload in payloads:
            for i in arr:
                payloaddata="degree=btech&examCode="+str(i)+payload+roll
                self.tasks.append(session.post(url[1], data=payloaddata,headers=headers,ssl=False))
        return self.tasks  

    #SGPA Calculator
    def total_grade_Calculator(self,code,value):
        try:
            total,credits=0,0
            for data in value:
                if('DETAILS' in data):
                    pass
                else:
                    if(value[data]['subject_grade']=='F' or value[data]['subject_grade']=='Ab'): 
                        return ""
                    total=total+int(grades_to_gpa[value[data]['subject_grade']])*float(value[data]['subject_credits'])
                    credits=credits+float(value[data]['subject_credits'])
            self.deta["Results"][code]["CGPA"]="{0:.2f}".format(round(total/credits,2)) 
        except:
            pass


    #Scraping the grades from the html page
    def scraping_the_grades(self,code,soup):
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
            self.deta["DETAILS"] = {"NAME": NAME, "Roll_No": Roll_NO, "COLLEGE_CODE": COLLEGE_CODE}
            
            for row in table2:
                try:
                    subject_name = row.find_all("td")[subject_name_index].find("b").contents[0]
                except:
                    subject_name=""
                subject_code = row.find_all("td")[subject_code_index].find("b").contents[0]
                subject_grade = row.find_all("td")[grade_index].find("b").contents[0]
                subject_credits = row.find_all("td")[subject_credits_index].find("b").contents[0]
                try:
                    if(self.deta["Results"][code][subject_code]["subject_grade"]!="F"):
                        continue    
                except:
                    pass
                self.deta["Results"][code][subject_code]={}
                self.deta["Results"][code][subject_code]["subject_name"]=subject_name
                self.deta["Results"][code][subject_code]["subject_code"]=subject_code
                self.deta["Results"][code][subject_code]["subject_grade"]=subject_grade
                self.deta["Results"][code][subject_code]["subject_credits"]=subject_credits
        except:
            pass
    
    
    async def getting_the_grades(self,code,roll):
        exam_Codes=exam_codes(code)
        async with aiohttp.ClientSession() as session:
            tasks=self.get_tasks(session,exam_Codes,roll)
            
            ###########################################################
            responses =await asyncio.gather(*tasks)
            ###########################################################

            self.deta["Results"][code]={}
            for response in responses:
                r=await response.text()
                soup = BeautifulSoup(r, "html.parser")
                
                self.scraping_the_grades(code,soup)
        await session.close()
        self.total_grade_Calculator(code,self.deta["Results"][code])
        return self.deta

    #Function called from views
    def get_grade_start(self,roll,code):
        return asyncio.run(self.getting_the_grades(code,roll))
    
    #Function to call from all-R18  
    async def getting_faster_Grades(self,roll,code):
        return asyncio.run(self.getting_the_grades(code,roll))

def get_cgpa(result):
    total,credits=0
    for ind in result:
        semesters=result[ind]
        for semester in semesters:
            print(semesters)
            subjects=semesters[semester]
            
            try:
                
                total=total+int(grades_to_gpa[subjects['subject_grade']])*float(subjects['subject_credits'])
                credits=credits+float(subjects['subject_credits'])
                print(total, credits)
            except:
                pass
    # if(value[data]['subject_grade']=='F' or value[data]['subject_grade']=='Ab'): 
    #                     return ""
    #                 total=total+int(grades_to_gpa[value[data]['subject_grade']])*float(value[data]['subject_credits'])
    #                 credits=credits+float(value[data]['subject_credits'])
    return 0   

        
                



