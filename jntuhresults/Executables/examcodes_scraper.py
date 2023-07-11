import requests
from bs4 import BeautifulSoup

def extract_exam_code(result_link):
    # Find the index of "examCode" in the result link
    exam_code_index = result_link.find("examCode")
    # Extract the exam code from the result link
    exam_code = result_link[exam_code_index + 9:exam_code_index + 13]
    try:
        if (exam_code[3]=='&'):
            return exam_code[:3]
    except Exception as e:
        print(e)
        return exam_code
    return exam_code


def categorize_exam_code(result_text, exam_code):
    # Categorize the exam code based on the result text
    if " I Year I " in result_text:
        return "1-1"
    elif " I Year II " in result_text:
        return "1-2"
    elif " II Year I " in result_text:
        return "2-1"
    elif " II Year II " in result_text:
        return "2-2"
    elif " III Year I " in result_text:
        return "3-1"
    elif " III Year II " in result_text:
        return "3-2"
    elif " IV Year I " in result_text:
        return "4-1"
    elif " IV Year II " in result_text:
        return "4-2"
    else:
        return None


def categorize_masters_exam_code(result_text,exam_code):
    # Categorize the masters exam code based on the result text
    if " I Semester" in result_text:
        return "1-1"
    elif " II Semester" in result_text:
        return "1-2"
    elif " III Semester" in result_text:
        return "2-1"
    elif " IV Semester" in result_text:
        return "2-2"
    else:
        return None
    
def get_exam_codes():
    url = "http://results.jntuh.ac.in/jsp/home.jsp"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    exam_codes = {
        "btech": {
            "R18": {},
            "R22": {}
        },
        "bpharmacy": {
            "R17": {},
            "R22":{}
        },
        "Mpharmacy":{
            "R19":{},
            "R22":{}
        },
        "MTech":{
                "R19":{},
                "R22":{}
        },
        "MBA":{
            "R19":{},
            "R22":{}
        }
    }
    degree=list(exam_codes.keys())
    for table in range(0,5):
        results = soup.find_all("table")[table].find_all("tr")
        regulations=exam_codes[degree[table]].keys()

        # Iterate through each result in the B.Tech results table
        for result in results:
            result_link =result.find_all("td")[0].find_all("a")[0]["href"]
            result_text=result.get_text()

            # Check if the result text contains any of the regulations
            for regulation in regulations:
                if regulation in result_text:
                    exam_code = extract_exam_code(result_link)
                    if (table<2):
                        category = categorize_exam_code(result_text, exam_code)
                    else:
                        category = categorize_masters_exam_code(result_text,exam_code)

                    if category is not None:
                        exam_codes[degree[table]][regulation].setdefault(category, [])
                        if exam_code not in exam_codes[degree[table]][regulation][category]:
                            exam_codes[degree[table]][regulation][category].append(exam_code)

        # Sort the exam codes within each category and sort the categories
        for regulation in regulations:
            for category, codes in exam_codes[degree[table]][regulation].items():
                exam_codes[degree[table]][regulation][category] = sorted(codes)
            exam_codes[degree[table]][regulation] = dict(sorted(exam_codes[degree[table]][regulation].items(), key=lambda x: x[0]))
    return exam_codes

exam_codes=get_exam_codes()


print(exam_codes)
