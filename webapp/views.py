from datetime import datetime

import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_babel import Babel
from flask_babel import gettext
from flask_restful import Api

from .models import *
from .networkCharacteristicsQueries import *


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

    @app.route("/topk", methods=['GET'])
    def topk():
        if request.method == 'GET':
            unis = dictToList(getAllUniversities())
            gender_distr = dictToList(getGenderDistributionOfUniversities())
            return render_template("topk.html", unis=unis, gender_distr=gender_distr)
        return render_template('topk.html')

    @app.route("/graphmtr")
    def graphmtr():
        return render_template('graphmtr.html')
    # you can add more pages using @app.route("/page")

    #@app.errorhandler(Exception)
    #def page_not_found(e):
    #    return render_template('error.html'), 400
    #app.register_error_handler(400, page_not_found)

    return app


app = create_app()