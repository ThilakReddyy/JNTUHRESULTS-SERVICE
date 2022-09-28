<p align="center">
  <img src="https://raw.githubusercontent.com/ThilakReddyy/JNTUHRESULTS-WEB/main/public/favicon-black.png#gh-dark-mode-only" alt="JNTUH B.TECH RESULTS" width="100">
  <img src="https://raw.githubusercontent.com/ThilakReddyy/JNTUHRESULTS-WEB/main/public/favicon-light.png#gh-light-mode-only" alt="JNTUH B.TECH RESULTS" width="100">
  <br>
  django | python | BeautifulSoup 
</p>

The Backbone of JNTUHRESULTS-WEB where all the semester results of a student and the results of all the classmates are fetched

## HOW IT WORKS

* Jntuh website doesn't have any api and it does not authenticate when a request is made it just sends back the response of that request
* I made a request and i got a response and using beautiful soup i have parse the html and i got my results

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

Found a bug with upstream Slate? Go ahead and [submit an issue](https://github.com/ThilakReddyy/JNTUHRESULTS-SERVICE/issues). And, of course, feel free to submit pull requests with bug fixes or changes to the `dev` branch.

Also feel free to message me if you have any ideas for small website tools that you can't yet find online. Thanks!

## Thanks

- [▲ Vercel](https://vercel.com/) for fast deployments served from the edge, hosting our website, downloads, and updates.
- [Next.js](https://nextjs.org/) for development framework created by Vercel enabling React-based web applications with server-side rendering and generating static websites

 
