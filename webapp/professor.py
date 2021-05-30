from neo4j.graph import Node

class Professor:

    def __init__(self,professor:Node):
        print(type(professor["interests"]))

        self.scholarId = name=professor["name"]
        self.scholar_Id=professor["scholar_id"]
        self.gender=professor["gender"]
        self.role=professor["role"]
        self.picture=professor["url_picture"] # The url of the image from google scholar
        self.citedby=professor["citedby"]
        self.citedby5y=professor["citedby5y"]
        self.hindex=professor["hindex"]
        self.hindex5y=professor["hindex5y"]
        self.i10index=professor["i10index"]
        self.i10index5y=professor["i10index5y"]
        self.num_publications=professor["num_publications"]
        self.cites_per_year=  dict([tuple(citesInAYear.split("-")) for citesInAYear in professor["cites_per_year"].split(" ")])
        try: # professor has at least one interest
            self.interest = [ interest for interest in [interest.replace("_"," ") for interest in professor["interests"].split(" ")] ]
        except AttributeError:
            self.interests = []

