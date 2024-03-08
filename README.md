# [JNTUH RESULTS](http://results.jntuh.ac.in/)  - SERVICE </h1>

[![Website](https://img.shields.io/badge/Website-Jntuh%20Results-blue?style=flat&logo=world&logoColor=white)](https://jntuhresults.up.railway.app/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/048b7d94dd064d56a4e6f3f64d65c7b8)](https://app.codacy.com/gh/ThilakReddyy/JNTUHRESULTS-SERVICE/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![License](https://img.shields.io/github/license/thilakreddyy/jntuhresults-service.svg)](https://github.com/ThilakReddyy/JNTUHRESULTS-SERVICE/blob/main/LICENSE)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/thilakreddyy/jntuhresults-service.svg)

This repository serves as the backbone for the [JNTUH RESULTS](https://github.com/ThilakReddyy/JNTUHRESULTS-WEB)  project. It fetches the semester results of a student and their classmates from the JNTUH website.

## HOW IT WORKS


The JNTUH website does not provide an API and does not require authentication for requests. Instead, it sends back the response for each request made. This service makes requests to the JNTUH website and parses the HTML response using Beautiful Soup to obtain the results.

## API'S

There are two API endpoints available for fetching results:

* `https://jntuhresults.up.railway.app/api/academicresult?htno={Roll_NO}` - Fetches results for a single student using their roll number.
* `https://jntuhresults.up.railway.app/api/classresult?htnos={multiple_htnos_separate_by_commas}&semester={code}` - Fetches results for multiple students within a given range of roll numbers and code.
## Running Locally

To run the code locally in development mode, follow these steps:

* Clone the repository: `git clone https://github.com/ThilakReddyy/JNTUHRESULTS-SERVICE.git`
* Navigate to the repository: `cd JNTUHRESULTS-SERVICE`
* Install the requirements: `pip install -r requirements.txt`
* Run the server: `python manage.py runserver`
* Open [http://localhost:8000](http://localhost:8000) in your browser to view the results.

## Need Help or Found a bug?

If you've got questions about setup, deploying, special feature implementation, or just want to chat with the developer, please feel free to contact me on <a href="mailto:thilakreddypothuganti@gmail.com">mail</a>

Found a bug ? Go ahead and [submit an issue](https://github.com/ThilakReddyy/JNTUHRESULTS-SERVICE/issues). And, of course, feel free to submit pull requests with bug fixes or changes to the `dev` branch.

Also feel free to message me if you have any ideas for small website tools that you can't yet find online. Thanks!

# Acknowledgements
This project relies on the following technologies:

- [django](https://www.djangoproject.com/) a high-level Python web framework that encourages rapid development and clean, pragmatic design.
- [python](https://www.python.org/)  a powerful and versatile programming language that is widely used in many fields.

 
