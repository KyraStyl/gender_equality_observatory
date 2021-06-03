from neo4j import GraphDatabase
from datetime import datetime
from neo4j.graph import Node
import os

driver = None

username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')
if username is None:
    username = "neo4j"
if password is None:
    password = "a"

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=(username, password))

class Professor:

    def __init__(self, professor: Node):
        print(type(professor["interests"]))

        self.name = professor["name"]
        self.scholar_Id = professor["scholar_id"]
        self.gender = professor["gender"]
        self.role = professor["role"]
        self.picture = professor["url_picture"]  # The url of the image from google scholar
        self.citedby = professor["citedby"]
        self.citedby5y = professor["citedby5y"]
        self.hindex = professor["hindex"]
        self.hindex5y = professor["hindex5y"]
        self.i10index = professor["i10index"]
        self.i10index5y = professor["i10index5y"]
        self.num_publications = professor["num_publications"]
        self.cites_per_year = dict(
            [tuple(citesInAYear.split("-")) for citesInAYear in professor["cites_per_year"].split(" ")])
        try:  # professor has at least one interest
            self.interests = [interest for interest in
                             [interest.replace("_", " ") for interest in professor["interests"].split(" ")]]
        except AttributeError:
            self.interests = []

    @property
    def serialize(self):
        return {
            'name': self.name,
            'scholar_id': self.scholar_Id,
            'gender': self.gender,
            'role': self.role,
            'picture': self.picture,
            'citedby': self.citedby,
            'citedby5y': self.citedby5y,
            'hindex': self.hindex,
            'hindex5y': self.hindex5y,
            'i10index': self.i10index,
            'i10index5y': self.i10index5y,
            'num_publications': self.num_publications,
            'cites_per_year': self.cites_per_year,
            'interests': self.interests
        }

def date():
    return datetime.now().strftime('%Y-%m-%d')