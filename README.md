<p align="center">
  <img src="https://raw.githubusercontent.com/ThilakReddyy/JNTUHRESULTS-WEB/main/public/favicon-black.png#gh-dark-mode-only" alt="JNTUH B.TECH RESULTS" width="100">
  <img src="https://raw.githubusercontent.com/ThilakReddyy/JNTUHRESULTS-WEB/main/public/favicon-light.png#gh-light-mode-only" alt="JNTUH B.TECH RESULTS" width="100">
  <br>
  django | python | BeautifulSoup 
</p>

The Backbone of JNTUHRESULTS-WEB where all the semester results of a student and the results of all the classmates are fetched

## HOW IT WORKS

* The JNTUH website does not have an API, and it does not authenticate requests. Instead, it sends back the response of each request made
* I made a request and received a response. Using Beautiful Soup, I parsed the HTML and obtained the results.

## API
* https://jntuhresults.up.railway.app/api/single?htno={Roll_NO}
* https://jntuhresults.up.railway.app/api/multi?from={from_roll_no}&to={To_roll_no}&code={code}


## Running locally in development mode

To get started, just clone the repository and run `pip install and python manage.py runserver`:

    git clone https://github.com/ThilakReddyy/JNTUHRESULTS-SERVICE.git
    cd JNTUHRESULTS-SERVICE
    pip install -r requirements.txt
    python manage.py runserver

Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.

## Questions? Need Help? Found a bug?

If you've got questions about setup, deploying, special feature implementation, or just want to chat with the developer, please feel free to contact me on <a href="mailto:thilakreddypothuganti@gmail.com">mail</a>

Found a bug ? Go ahead and [submit an issue](https://github.com/ThilakReddyy/JNTUHRESULTS-SERVICE/issues). And, of course, feel free to submit pull requests with bug fixes or changes to the `dev` branch.

Also feel free to message me if you have any ideas for small website tools that you can't yet find online. Thanks!

## Thanks

- [django](https://www.djangoproject.com/) is a high-level Python web framework that encourages rapid development and clean, pragmatic design
- [python](https://www.python.org/) is a programming language that lets you work quickly
and integrate systems more effectively.

 
