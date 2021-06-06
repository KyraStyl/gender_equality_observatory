from datetime import datetime

import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_babel import Babel
from flask_babel import gettext
from flask_restful import Api

from .models import *
from .networkCharacteristicsQueries import *
from .genderCharacteristicsQueries import *


def flatmap(di):
    l = []
    for i in di.items():
        value = i[1]
        if type(value) is dict:
            value = flatmap(value)
        l.append(value)
    return l

def dictToList(diction):
    dictlist = []
    for item in diction.items():
        value = item[1]
        if type(value) is dict:
            value = flatmap(value)
        dictlist.append([item[0], value])
    return dictlist

def loadStaticDataForGender():
    cardHeaders = ['Average Number of Publications', 'Average Number Of Coauthors', 'Average Number Of Citations',
                   'Average Number Of HIndex', 'Average Number Of I10Index', 'Average Degree Centrality',
                   'Average Betweenness', 'Average PageRank Score', 'Average Closeness Centrality', 'Average Number of Triangles']
    cardData = []
    cardData.append(getAverageNumberOfPublicationsOfMaleAndFemaleProfessor())
    cardData.append(dictToList(getAverageNumberOfCoauthorsOfMaleAndFemaleProfessor()))
    cardData.append(getAverageNumberOfCitationsOfMaleAndFemaleProfessor())
    cardData.append(getAverageNumberOfHIndexOfMaleAndFemaleProfessor())
    cardData.append(getAverageNumberOfI10IndexOfMaleAndFemaleProfessor())
    cardData.append(avgDegreeCentralityScoreOfFemaleAndMaleProfessor())
    cardData.append(avgBetweenesScoreOfFemaleAndMaleProfessor())
    cardData.append(avgPageRankScoreOfFemaleAndMaleProfessor())
    cardData.append(avgClosenessCentralityOfFemaleAndMaleProfessor())
    cardData.append(getAvgOfTrianglesForMaleAndFemaleProfessors())

    return cardHeaders, cardData


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.app_context().push()
    app.secret_key = "fgdk456#rteg"

    api = Api(app, "/api/v1")
    #api.add_resource()

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        if "lang" in request.cookies and request.cookies["lang"] in translations:
            return request.cookies["lang"]
        return request.accept_languages.best_match(translations, default="en")

    app.jinja_env.globals["get_locale"] = get_locale
    app.jinja_env.globals["req_datetime"] = datetime.now()


    @app.route("/")
    @app.route("/home")
    def home():
        return render_template('home.html')

    @app.route("/gender", methods=['GET','POST'])
    def gender():
        if request.method in ['GET','POST']:
            titles, headers, data = [], [], []
            if request.method == 'GET':
                num = 5
            if request.method == 'POST':
                num = int(request.form["topk"])
                if request.form.get('coauthors'):
                    titles.append('with the Most Co-authors')
                    headers.append(['Name','Gender','Co-authors'])
                    data.append(getTopKProfessorsWithMostCoauthors(num))
                if request.form.get('pagerank'):
                    titles.append('with Highest PageRank Score')
                    headers.append(['Name','Gender','PageRank Score'])
                    data.append(topKProfessorsWithHighestPageRankScore(num))
                if request.form.get('betweenness'):
                    titles.append('with the Highest Betweenness')
                    headers.append(['Name', 'Gender', 'Betweeness'])
                    data.append(topKProfessorsWithHighestBetweenes(num))
                if request.form.get('degreecentr'):
                    titles.append('with the Highest Degree Centrality')
                    headers.append(['Name', 'Gender', 'Degree Centrality'])
                    data.append(topKProfessorsWithHighestDegreeCentrality(num))
                if request.form.get('closenesscentr'):
                    titles.append('with the Highest Closeness Centrality')
                    headers.append(['Name', 'Gender', 'Closeness Centrality'])
                    data.append(topKProfessorsWithHighestClosenessCentrality(num))
                if request.form.get('closharmcentr'):
                    titles.append('with the Highest Closeness Harmonic Centrality')
                    headers.append(['Name', 'Gender', 'Closeness Harmonic Centrality'])
                    data.append(topKProfessorsWithHighestClosenessHarmonicCentrality(num))
            numFunc = len(titles)
            cardHeaders, cardData = loadStaticDataForGender()
            return render_template("gender.html", size=len(cardHeaders), cardHeaders=cardHeaders, cardData=cardData, num=num, numFunc=numFunc, titles=titles, headers=headers, data=data)
        else:
            return render_template('error.html')

    @app.route("/graphmtr", methods=['GET'])
    def graphmtr():
        if request.method == 'GET':
            info = getAllInfo()
            louvain = int(getNumberOfCommunitiesLouvain())
            scc = int(getNumberOfCommunitiesSCC())
            wcc = int(getNumberOfCommunitiesWCC())
            modularity = int(getNumberOfCommunitiesModularityOptimization())
            triangles = int(getNumberOfTriangles())
            return render_template("graphmtr.html", info=info, louvain=louvain, scc=scc, wcc=wcc, triangles=triangles, modularity=modularity)
        return render_template('error.html')
    # you can add more pages using @app.route("/page")

    @app.route("/universities", methods=['GET'])
    def universities():
        if request.method == 'GET':
            unis = dictToList(getAllUniversities())
            gender_distr = dictToList(getGenderDistributionOfUniversities())
            return render_template("universities.html", unis=unis, gender_distr=gender_distr)
        return render_template("error.html")


    @app.route("/profforuni/<uni>", methods=["GET"])
    def profforuni(uni):
        if request.method == "GET":
            profs = dictToList(getAllProfessorsOfSpecificUniversity(uni))
            return render_template("profforuni.html", uni=uni, profs=profs)
        return render_template("error.html")

    @app.route("/profinfo/<prof>", methods=["GET"])
    def profinfo(prof):
        if request.method == "GET":
            professor = getSpecificProfessor(prof)
            info = dictToList(professor.serialize)
            return render_template("profinfo.html", name=prof, info=info)
        return render_template("error.html")


    #@app.errorhandler(Exception)
    #def page_not_found(e):
    #    return render_template('error.html'), 400

    #app.register_error_handler(400, page_not_found)
    return app


app = create_app()