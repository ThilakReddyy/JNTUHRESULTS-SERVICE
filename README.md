<p align="center">
  <img src="https://raw.githubusercontent.com/ThilakReddyy/JNTUHRESULTS-WEB/main/public/favicon-black.png#gh-dark-mode-only" alt="JNTUH B.TECH RESULTS" width="100">
  <img src="https://raw.githubusercontent.com/ThilakReddyy/JNTUHRESULTS-WEB/main/public/favicon-light.png#gh-light-mode-only" alt="JNTUH B.TECH RESULTS" width="100">
  <br>
  django | python | BeautifulSoup 
</p>

The Backbone of <a href="https://github.com/ThilakReddyy/JNTUHRESULTS-WEB">JNTUHRESULTS-WEB</a> where all the semester results of a student and the results of all the classmates are fetched

## HOW IT WORKS

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aadfdfa66e2347d3974bce4230b81e1a)](https://app.codacy.com/gh/ThilakReddyy/JNTUHRESULTS-SERVICE?utm_source=github.com&utm_medium=referral&utm_content=ThilakReddyy/JNTUHRESULTS-SERVICE&utm_campaign=Badge_Grade)

* The JNTUH website does not have an API, and it does not authenticate requests. Instead, it sends back the response of each request made
* I made a request and received a response. Using Beautiful Soup, I parsed the HTML and obtained the results.

## API
Two API endpoints are available for fetching results:

* https://jntuhresults.up.railway.app/api/academicresult?htno={Roll_NO} - Fetches results for a single student using their roll number.
* https://jntuhresults.up.railway.app/api/classresult?htnos={multiple_htnos_seperate_by_commas}&semester={code} - Fetches results for multiple students within a given range of roll numbers and code.


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

## Thanks

- [django](https://www.djangoproject.com/) a high-level Python web framework that encourages rapid development and clean, pragmatic design.
- [python](https://www.python.org/)  a powerful and versatile programming language that is widely used in many fields.

 
