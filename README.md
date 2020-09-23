<p align="center">
  <a href="" rel="noopener">
 
</p>

<h3 align="center">Flaskgram, a Flask-based Instagram Clone</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Few lines describing your project.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

An attempt to clone the instagram Web Application

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.

```python
Python(>v3.6.x), Pip Package manager and a virtualenvironment manager(Pipenv, Poetry etc)
```
### Installing

A step by step series of examples that tell you how to get a development env running.

Clone the repo from github. 
Create and Activate Virtual Environment(recommended) to avoid dependency resolution issues.
If you intend to contribute, create a branch and checkout(switch) to it as your main working branch.
Set up a database(SQLITE3 is fine.) and automatically load up the necessary .env variables
Run the appropriate db migrations to load the db schema and keep track the versions of the db and flask translate {lang} ti run the i8n translations.
Run the tests.
Finally, launch flask run to run a dev server(or flask run--cert=adhoc to get an adhoc ssl certificate)o
```bash
#Clone the repo
git clone https://github.com/Bnjorogedev/Flaskgram-instaclone.git
```
Create and activate a virtualenvironment
```python
#if you use virtualenvwrapper, run virtualenv{name of venv dir} or pipenv {name of dir} otherwise
python3 -m venv {name of venv} && source /path/to/venv/bin/activate/
```
Install required dependencies and switch to your dev branch
```python
pip install -r requirements.txt
cd {path/to/venvdir}
git checkout -b {branch name}
```
Create a .env file and copy the env templates
```bash
touch .env && cp .env.template .env
```
### Run db migrations and i8n translations
```python
flask db migrate && flask db upgrade
flask translate fr
```
```python
nose2 tests/ && flask run
```

### And coding style tests

I use [Black](https://pypi.org/project/black/#:~:text=Black%20is%20the%20uncompromising%20Python,energy%20for%20more%20important%20matters) code to format my code.

```
black {name of dir}
```

## 🎈 Features <a name="features"></a>
1. Standard and Secure Registration/Login(with email verification and password resetting)
2. Google/Facebook/Twitter/Github Oauthentication Flows
3. CRUD posts with image and captioning functionality.
4. Like/Unlike Posts
5. Follow/Unfollow Users/Hashtags
6. Bookmark Posts/Get post notifications via email and from your profile.
7. Basic Feed personalization that allows you to view posts from users you follow.
8. Recommend follow suggestions based on hashtags.
9. Simple non-websocket private chat messaging feature.
10. Basic Video Call 
11. Multi-feature search functionality. Search by Users, Posts, Captions etc

## 🚀 Deployment <a name = "deployment"></a>
Will update soon.

## ⛏️ Built Using <a name = "built_using"></a>

- [Flask](https://www.mongodb.com/) - Web Framework
- [MySQL](https://expressjs.com/) - Database
- [Bootstrap4](https://vuejs.org/) - Frontend Framework
- [ElasticSearch](https://nodejs.org/en/) - Search Engine
## Contributing
Pull requests are certainly welcome.
I've used [Travis-CI](https://travis-ci.com) for my CI/CD workflows, so before your PR is merged into master I'll review it and Travis will run a test build.

## TODO/Bugs
- [ ] Switch to pytest for testing and add more test coverage  
- [ ] Add a whole lot more dynamism using Javascript
- [ ] There's a bug with the search functionality. 
- [ ] Add collaborative filter recommendation system for Posts/Users
- [ ] Constantly refactor the codebase
- [ ] Add Instagram-like filters.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Miguel Grinberg's Flask Mega Tutorial
- Inspiration
- References

## License
[MIT](https://choosealicense.com/licenses/mit/)
