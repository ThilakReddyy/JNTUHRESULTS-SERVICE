import requests
from bs4 import BeautifulSoup
url = "http://202.63.105.184/results/resultAction"

payload='degree=btech&etype=r17&examCode=1580&grad=null&htno=18E51A0462&result=null&type=intgrade'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

response = requests.request("POST", url, headers=headers, data=payload)

soup = BeautifulSoup(response.content, "html.parser")
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
            for row in table2:
                subject_name = row.find_all("td")[subject_name_index].find("b").contents[0]
                subject_code = row.find_all("td")[subject_code_index].find("b").contents[0]
                subject_grade = row.find_all("td")[grade_index].find("b").contents[0]
                subject_credits = row.find_all("td")[subject_credits_index].find("b").contents[0]
                
except:
    pass
print(NAME,FATHER_NAME,COLLEGE_CODE)