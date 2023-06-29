# Import necessary libraries
import asyncio
import aiohttp
import time
import json
from bs4 import BeautifulSoup
# from jntuh.Executables import jntuhresultscraper

# Define a class for scraping JNTUH results
class ResultScraper:
    def __init__(self, roll_number):
        
        # Initialize instance variables
        self.url = "http://results.jntuh.ac.in/resultAction"
        # self.url="http://202.63.105.184/results/resultAction"
        
        self.roll_number = roll_number
        
        self.results = {"Details": {}, "Results": {}}
        
        # Exam codes for different regulations and semesters
        self.exam_codes={
                'btech': {
                    'R18': {
                    '1-1': ['1323', '1358', '1404', '1430', '1467', '1504', '1572', '1615', '1658'],
                    '1-2': ['1356', '1363', '1381', '1435', '1448', '1481', '1503', '1570', '1620', '1622', '1656'],
                    '2-1': ['1391', '1425', '1449', '1496', '1560', '1610', '1628', '1667','1671'],
                    '2-2': ['1437', '1447', '1476', '1501', '1565', '1605', '1627', '1663'],
                    '3-1': ['1454', '1491', '1550', '1590', '1626', '1639', '1645', '1655'],
                    '3-2': ['1502', '1555', '1595', '1625', '1638', '1649', '1654'],
                    '4-1': ['1545', '1585', '1624', '1640', '1644', '1653'],
                    '4-2': ['1580', '1600', '1623']
                    },
                    'R22': {
                    '1-1': ['1662']
                    }
                },
                'bpharmacy': {
                    'R17': {
                    '1-1': ['519', '537', '577', '616', '643', '683', '722', '781', '824', '832','855'],
                    '1-2': ['517', '549', '575', '591', '648', '662', '698', '727', '779', '829', '831','853','860'],
                    '2-1': ['532', '570', '638', '673', '717', '769', '819', '849'],
                    '2-2': ['558', '611', '650', '661', '693', '711', '774', '814', '845'],
                    '3-1': ['597', '633', '668', '712', '759', '799', '837'],
                    '3-2': ['655', '660', '688', '710', '764', '804', '841'],
                    '4-1': ['663', '705', '754', '794', '832', '836'],
                    '4-2': ['678', '700', '789', '809']
                    },
                    'R22': {
                        '1-1': ['859']
                    }
                },
                'mpharmacy': {
                    'R19': 
                    {
                        '1-1': ['319', '332', '347', '356', '371', '382', '388'], 
                        '1-2': ['328', '336', '344', '353', '368', '379', '387'],
                        '2-1': ['337', '350', '365', '376', '386'], 
                        '2-2': ['340', '374', '385']
                    }, 
                    'R22': 
                    {
                        '1-1': ['389']
                    }
                }, 
                'mTech': {
                    'R19': 
                    {
                        '1-1': ['161', '177', '185', '198', '209', '215'], 
                        '1-2': ['157', '165', '174', '182', '195', '206', '214'], 
                        '2-1': ['166', '180', '194', '204', '213'], 
                        '2-2': ['169', '203', '212']
                    }, 
                    'R22': 
                    {
                        '1-1': ['216']
                    }
                }, 
                'mba': {
                    'R19': 
                    {
                        '1-1': ['297', '316', '323', '350', '362', '368'], 
                        '1-2': ['122', '293', '302', '313', '320', '347', '359', '367'], 
                        '2-1': ['303', '310', '344', '356', '366'], 
                        '2-2': ['120', '307', '341', '353', '365']
                    }, 
                    'R22': 
                    {
                        '1-1': ['369']
                    }
                }
            }


        #To be implemented after implementing redis server
        # self.examcodes=jntuhresultscraper.exam_codes()

        # GPA conversion table
        self.grades_to_gpa = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0, 'Ab': 0, '-': 0}
        
        # Payloads for different types of result requests
        self.payloads={
                "btech":["&degree=btech&etype=r17&result=null&grad=null&type=intgrade&htno=","&degree=btech&etype=r17&result=gradercrv&grad=null&type=rcrvintgrade&htno="],
                "bpharmacy":["&degree=bpharmacy&etype=r17&grad=null&result=null&type=regular&htno=","&degree=bpharmacy&etype=r17&grad=null&result=gradercrv&type=rcrvintgrade&htno="],
                "mba":["&degree=mba&grad=pg&etype=null&result=grade17&type=intgrade&htno=","&degree=mba&grad=pg&etype=r16&result=gradercrv&type=rcrvintgrade&htno="]
                }

    async def fetch_result(self, session, exam_code, payload):
        
        # Prepare the payload for the HTTP POST request
        payloaddata="?&examCode="+exam_code+payload+self.roll_number
        
        # Make the HTTP POST request and print the response text
        async with session.get(self.url+payloaddata) as response:
            return await response.text()

    def scrape_results(self, semester_code, response):
        
        # Parse the response HTML using BeautifulSoup
        soup = BeautifulSoup(response, "lxml")

        # Get student details
        Details = soup.find_all("table")[0].find_all("tr")
        Htno = Details[0].find_all("td")[1].get_text()
        Name = Details[0].find_all("td")[3].get_text()
        Father_Name = Details[1].find_all("td")[1].get_text()
        College_Code = Details[1].find_all("td")[3].get_text()
        
        # Store student details in the results dictionary
        self.results["Details"]["NAME"]=Name
        self.results["Details"]["Roll_No"]=Htno
        self.results["Details"]["COLLEGE_CODE"]=College_Code
        self.results["Details"]["FATHER_NAME"]=Father_Name
        
        Results = soup.find_all("table")[1].find_all("tr")

        Results_column_names = [content.text for content in Results[0].findAll("b")]
        grade_index = Results_column_names.index("GRADE")
        subject_name_index = Results_column_names.index("SUBJECT NAME")
        subject_code_index = Results_column_names.index("SUBJECT CODE")
        subject_credits_index = Results_column_names.index("CREDITS(C)")

        Results = Results[1:]
        for result_subject in Results:
            subject_name = result_subject.find_all("td")[subject_name_index].get_text()
            subject_code = result_subject.find_all("td")[subject_code_index].get_text()
            subject_grade = result_subject.find_all("td")[grade_index].get_text()
            subject_credits = result_subject.find_all("td")[
                subject_credits_index
            ].get_text()

            # Skip subjects with lower grades if already stored
            if(subject_code in self.results["Results"][semester_code] and 
                    self.results["Results"][semester_code][subject_code]["subject_grade"]!='F' and
                    self.results["Results"][semester_code][subject_code]["subject_grade"]!='Ab' and
                    self.results["Results"][semester_code][subject_code]["subject_grade"]!='-' and
                    self.grades_to_gpa[self.results["Results"][semester_code][subject_code]["subject_grade"]]>self.grades_to_gpa[subject_grade]):
                continue
           
            # Store Subject details in results dictionary
            self.results["Results"][semester_code][subject_code] = {}
            self.results["Results"][semester_code][subject_code]["subject_code"] = subject_code
            self.results["Results"][semester_code][subject_code]["subject_name"] = subject_name
            self.results["Results"][semester_code][subject_code]["subject_grade"] = subject_grade
            self.results["Results"][semester_code][subject_code][
                "subject_credits"
            ] = subject_credits
    
    # Calculate the total cgpa of each semester
    def total_grade_calculator(self, code, value):
        total = 0
        credits = 0

        for data in value:
            if 'DETAILS' in data:
                continue

            if value[data]['subject_grade'] in ('F', 'Ab','-'):
                return ""

            #important formulae
            total += int(self.grades_to_gpa[value[data]['subject_grade']]) * float(value[data]['subject_credits'])
            credits += float(value[data]['subject_credits'])

        self.results["Results"][code]["total"] = total
        self.results["Results"][code]["credits"] = credits
        self.results["Results"][code]["CGPA"] = "{0:.2f}".format(round(total / credits, 2))


    async def scrape_all_results(self, exam_code="all"):
        async with aiohttp.ClientSession() as session:
            tasks = {}

            # Check the roll number's fifth character to identify the degree
            if self.roll_number[5] == "A":
                # Set payloads to btech
                payloads = self.payloads["btech"]
                # Determine the exam codes based on the roll number prefix
                exam_codes = self.exam_codes["btech"]["R22" if self.roll_number[:2] == "22" else "R18"]

            elif self.roll_number[5] == "R":
                # Set payloads to bpharmacy
                payloads = self.payloads["bpharmacy"]
                # Set the exam codes for bpharmacy
                exam_codes = self.exam_codes["bpharmacy"]["R22" if self.roll_number[:2] == "22" else "R17"]
            
            elif self.roll_number[5]=="E":
                 # Set payloads to MBA
                payloads = self.payloads["mba"]
                
                # Determine the exam codes based on the roll number prefix
                exam_codes = self.exam_codes["mba"]["R22" if self.roll_number[:2] == "22" else "R19"]
                
            else:
                return self.results

            # Check if the fourth character of the roll number is '5'
            if self.roll_number[4] == "5":
                # Remove specific exam codes from the exam_codes dictionary
                exam_codes.pop("1-1", None)
                exam_codes.pop("1-2", None)

            # Check if exam_codes should include all codes
            if exam_code != "all":
                exam_codes={exam_code : exam_codes[exam_code]}

            for exam_code in exam_codes.keys():
                # Create a task for each exam code
                tasks[exam_code] = []

                for code in exam_codes[exam_code]:
                    for payload in payloads:
                        try:
                            task = asyncio.ensure_future(self.fetch_result(session, code, payload))
                            tasks[exam_code].append(task)
                        except Exception as e:
                            pass
                            print(self.roll_number,e)

            # Wait for all the tasks to complete
            for exam_code, exam_tasks in tasks.items():
                self.results["Results"][exam_code] = {}
                try:
                    for result in await asyncio.gather(*exam_tasks):
                        if "Enter HallTicket Number" not in result:
                            self.scrape_results(exam_code, result)

                    if bool(self.results["Results"][exam_code]):
                        self.total_grade_calculator(exam_code, self.results["Results"][exam_code])
                    else:
                        del self.results["Results"][exam_code]
                except Exception as e:
                    print(self.roll_number,e)
        return self.results


    def run(self):
        timeout = 3.5  # Timeout value in seconds
        try:
            return asyncio.run(asyncio.wait_for(self.scrape_all_results(), timeout))
        except asyncio.TimeoutError:
            return None
