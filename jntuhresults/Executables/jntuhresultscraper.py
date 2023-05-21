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
        self.roll_number = roll_number
        self.results = {"Details": {}, "Results": {}}
        
        # Exam codes for different semesters
        self.exam_codes = {
            "1-1": ["1323", "1358", "1404", "1430", "1467", "1504", "1572", "1615", "1658"],
            "1-2": ["1356", "1363", "1381", "1435", "1448", "1481", "1503", "1570", "1620", "1622", "1656"],
            "2-1": ["1391", "1425", "1449", "1496", "1560", "1610", "1628"],
            "2-2": ["1437", "1447", "1476", "1501", "1565", "1605", "1627"],
            "3-1": ["1454", "1491", "1550", "1590", "1626", "1639", "1645", "1655"],
            "3-2": ["1502", "1555", "1595", "1625", "1638", "1649", "1654"],
            "4-1": ["1545", "1585", "1624", "1640", "1644", "1653"],
            "4-2": ["1580", "1600", "1623"]
        }


        #To be implemented after implementing redis server
        # self.examcodes=jntuhresultscraper.exam_codes()

        # GPA conversion table
        self.grades_to_gpa = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0, 'Ab': 0, '-': 0}
        
        # Payloads for different types of result requests
        self.payloads = ["&etype=r17&result=null&grad=null&type=intgrade&htno=", "&etype=r17&result=gradercrv&grad=null&type=rcrvintgrade&htno="]

    async def fetch_result(self, session, exam_code, payload):
        
        # Prepare the payload for the HTTP POST request
        payloaddata="?degree=btech&examCode="+exam_code+payload+self.roll_number

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
        self.results["Details"]["Htno"]=Htno
        self.results["Details"]["Name"]=Name
        self.results["Details"]["Father_Name"]=Father_Name
        self.results["Details"]["College_Code"]=College_Code
        
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
            if(subject_code in self.results["Results"][semester_code] and 
                    self.results["Results"][semester_code][subject_code]["subject_grade"]!='F' and
                    self.results["Results"][semester_code][subject_code]["subject_grade"]!='Ab' and
                    self.results["Results"][semester_code][subject_code]["subject_grade"]!='-' and
                    self.results["Results"][semester_code][subject_code]["subject_grade"]<subject_grade):
                continue
            
            self.results["Results"][semester_code][subject_code] = {}
            self.results["Results"][semester_code][subject_code]["subject_code"] = subject_code
            self.results["Results"][semester_code][subject_code]["subject_name"] = subject_name
            self.results["Results"][semester_code][subject_code]["subject_grade"] = subject_grade
            self.results["Results"][semester_code][subject_code][
                "subject_credits"
            ] = subject_credits

    def total_grade_calculator(self, code, value):
        total = 0
        credits = 0

        for data in value:
            if 'DETAILS' in data:
                continue

            if value[data]['subject_grade'] in ('F', 'Ab','-'):
                return ""

            total += int(self.grades_to_gpa[value[data]['subject_grade']]) * float(value[data]['subject_credits'])
            credits += float(value[data]['subject_credits'])

        self.results["Results"][code]["total"] = total
        self.results["Results"][code]["credits"] = credits
        self.results["Results"][code]["CGPA"] = "{0:.2f}".format(round(total / credits, 2))


    async def scrape_all_results(self, exam_codes="all"):
        async with aiohttp.ClientSession() as session:
            tasks = {}

            if exam_codes == "all":
                exam_codes = self.exam_codes
                if self.roll_number[4] == "5":
                    del exam_codes["1-1"], exam_codes["1-2"]
            else:
                exam_codes = self.exam_codes

            for exam_code in exam_codes.keys():
                # Create a task for each exam code
                tasks[exam_code] = []

                for code in exam_codes[exam_code]:
                    for payload in self.payloads:
                        task = asyncio.ensure_future(self.fetch_result(session, code, payload))
                        tasks[exam_code].append(task)

            # Wait for all the tasks to complete
            for exam_code, exam_tasks in tasks.items():
                self.results["Results"][exam_code] = {}

                for result in await asyncio.gather(*exam_tasks):
                    if "Enter HallTicket Number" not in result:
                        self.scrape_results(exam_code, result)

                if bool(self.results["Results"][exam_code]):
                    self.total_grade_calculator(exam_code, self.results["Results"][exam_code])

        return self.results


    def run(self):
        return asyncio.run(self.scrape_all_results())