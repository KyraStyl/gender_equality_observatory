from py2neo import Graph, Node, Relationship
from datetime import datetime
import os

graph = Graph()
# OR
# url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
# username = os.environ.get('NEO4J_USERNAME')
# password = os.environ.get('NEO4J_PASSWORD')

username = "NEO4J_USERNAME"

class Person:
    def __init__(self, name):
        self.name = name

    def find(self):
        # create a method to check if person exists

    def createPerson(self, name):
        if not self.find():
            # person = Node( arguments ) -- create a new Node
            # graph.create(person) -- add node to graph
            return True
        else:
            return False

    def submit_a_query(self):
            query = '''
            MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
            WHERE user.username = {username}
            RETURN post, COLLECT(tag.name) AS tags
            ORDER BY post.timestamp DESC LIMIT 5
            '''
            response = graph.cypher.execute(query)
            # or graph.run(query) ?
            return response

def date():
    return datetime.now().strftime('%Y-%m-%d')