import requests
from bs4 import BeautifulSoup
urll = "http://results.jntuh.ac.in/jsp/home.jsp"


arr11,arr12,arr21,arr22,arr31,arr32,arr41,arr42=set(),set(),set(),set(),set(),set(),set(),set()

response = requests.request("GET", urll)
soup = BeautifulSoup(response.content, "html.parser")
tr= soup.find_all("table")[0].find_all("tr")
for i in tr:
    td=i.find_all("td")[0]
    href=td.find_all("a")[0]['href']
    text=td.get_text()
    code='R18'
    if code in text:
        examCode_Index=href.find("examCode")
        examCode=href[examCode_Index+9:examCode_Index+13]
        if(' I Year I ' in text):
            arr11.add(examCode)
        elif(' I Year II ' in text):
            arr12.add(examCode)
        elif(' II Year I ' in text):
            arr21.add(examCode)
        elif(' II Year II ' in text):
            arr22.add(examCode)
        elif(' III Year I ' in text):
            arr31.add(examCode)
        elif(' III Year II ' in text):
            arr32.add(examCode)
        elif(' IV Year I ' in text):
            arr41.add(examCode)
        elif(' IV Year II ' in text):
            arr42.add(examCode)
        
arr11=sorted(arr11)
arr12=sorted(arr12)
arr21=sorted(arr21)
arr22=sorted(arr22)
arr31=sorted(arr31)
arr32=sorted(arr32)
arr41=sorted(arr41)
arr42=sorted(arr42)
print(type(arr11))


