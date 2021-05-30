from neo4j import GraphDatabase
from professor import Professor






class databaseConnector:

    def __init__(self):
        uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", "a"))



    # returns all the universities and their departments  
    def getAllUniversities(self)-> dict:  

        """
        ################ Returns ####################
        {
        'University of Oulu': ['CSEE'] 
        ,'University of Bochum': ['Department of Civil and Enviromental Engineering', 'Faculty of Electrical Engineering and Information Technology'] 
        ,'University of Porto': ['CS', 'ECE'] 
        ,'University of Bordeaux': ['CS', 'IME'] 
        ,'University of Lodz': ['MIS', 'IT', 'ApCS'] 
        ,'University of Thessaloniki': ['CS', 'ECE']
        }
        """

        #'University of Oulu': ['MIC', 'ACM', 'INTERACT', 'CAS', 'M3S', 'Ubiquitous Computing', 'OASIS', 'ECE', 'BISG', 'CWC-Radio Technologies', 'MRU', 'CMVS', 'OMT', 'CWC', 'CWC-NS'] \

        with self.driver.session() as session:
            universities = session.run("MATCH (d:Department)-[]->(u:University) RETURN u.name, collect(d.name)")
            return dict(universities.values())


    # Returns for each university the number of Males and Females
    def getGenderDistributionOfUniversities(self)-> dict(): 

        """
        ########### Returns #########################
        {
        'University of Oulu': {'Male': 68, 'Female': 17} 
        ,'University of Bochum': {'Male': 28, 'Female': 7} 
        ,'University of Porto': {'Male': 25, 'Female': 4}
        ,'University of Bordeaux': {'Male': 30, 'Female': 6}
        ,'University of Lodz': {'Male': 42, 'Female': 9}
        ,'University of Thessaloniki': {'Male': 24, 'Female': 2}
        }

        """
        with self.driver.session() as session:
            genderDistributionOfUniversities = dict()
            for university in self.getAllUniversities():
                e = session.run("MATCH (pm:Professor {gender:$male})-[r1:worksAt]->(d:Department)-[r2:belongsTo]->(u:University {name:$name}) \
                            RETURN 'Male' AS Gender,  count(pm) AS number \
                            UNION \
                            MATCH (pf:Professor {gender:$female})-[r1:worksAt]->(d:Department)-[r2:belongsTo]->(u:University {name:$name}) \
                            RETURN 'Female' AS Gender, count(pf) AS number" \
                            ,male="M", female="F",name=university)
                genderDistributionOfUniversities[university] = dict(e.values())

            return genderDistributionOfUniversities 



    # Returns all the professors of a specific university 
    def getAllProfessorsOfSpecificUniversity(self,university:str)-> dict:  

        """
        ############ Returns for university of thessaloniki ##############
        {
        'CS': ['Athena Vakali', 'IOANNIS STAMELOS', 'I. Pitas', 'Petros Nicopolitidis', 'Nikos Laskaris', 'Dimitris Vrakas', 'Ioannis Vlahavas', 'Grigorios Tsoumakas', 'Nikolaos L. Tsitsas', 'Thrasyvoulos Tsiatsos', 'Anastasios Tefas', 'Nikos Pleros', 'Apostolos N. Papadopoulos', 'Georgios Papadimitriou', 'Christos Ouzounis', 'Nikos Nikolaidis', 'Amalia Miliou', 'Constantine Kotropoulos', 'Nikos Konofaos', 'Georgios Keramidas', 'Panagiotis Katsaros', 'Christos Katsanos', 'Anastasios Gounaris', 'Stavros Demetriadis', 'Nick Bassiliades', 'Lefteris (Eleftherios) Angelis']
        ,'ECE': ['Vasilis Chatziathanasiou', 'Charis Demoulias', 'Dimitrios Chrissoulidis', 'George Sergiadis', 'Athanasios Kehagias', 'Thomas E. Tsovilis', 'George Andreou', 'Minas Alexiadis', 'Pandelis Biskas', 'Grigoris  K. Papagiannis', 'Pantelis N. Mikropoulos', 'Christos Mademlis', 'George Litsardakis', 'Dimitrios P. Lampridis (Dimitris P. Labridis)', 'CLOUVAS', 'Anastasios Bakirtzis', 'Nestor Chatzidiamantis', 'Nikolaos Atreas', 'Traianos Yioultsis', 'Leontios J. Hadjileontiadis', 'Ioannis T. Rekanos', 'Thomas Xenos', 'Emmanouil Kriezis', 'George K. Karagiannidis', 'Leonidas Georgiadis', 'Christos Antonopoulos', 'Konstantinos Papalamprou', 'Dimitris Geneiatakis', 'Andreas L. Symeonidis', 'Leonidas Pitsoulis', 'Nikos P. Pitsianis', 'Ioannis Papaefstathiou', 'Anastasios Delopoulos', 'John B. Theocharis', 'George A. Rovithakis', 'Pericles A. Mitkas', 'D Kugiumtzis', 'Zoe Doulgeri']
        }
        """

        with self.driver.session() as session:
            professors = session.run("MATCH (p:Professor)-[r1:worksAt]->(d:Department)-[r2:belongsTo]->(u:University {name:$name}) \
                                     RETURN d.name, collect(p.name)"  \
                                     ,name=university)
            return dict(professors.values())



    # returns the details of a specific professor 
    def getSpecificProfessor(self,professor:str)-> Professor:
        with self.driver.session() as session:
            professor = session.run("MATCH (p:Professor) WHERE p.name=$name RETURN p",name=professor)
            return Professor(professor.value()[0])




    # returns all the coauthors of a professor
    def getCoauthorsOfSpecificProfessor(self,professor:str)-> list: 

        """
        ############### Returns for I. Pitas ###############
        [['Anastasios Tefas', 'M'], ['Nikos Nikolaidis', 'M'], ['Constantine Kotropoulos', 'M']]
        """

        with self.driver.session() as session:
            coauthors = session.run("MATCH (p:Professor {name:$professor})-[r:cooperateWith]-(p2) \
                                    RETURN p2.name, p2.gender" \
                                    ,professor=professor)
            return coauthors.values()



    # return the N professors that have the most coauthors
    def getProfessorsWithMostCoauthors(self,numberOfProfessorsToReturn:int)-> list: 

        """
        ######## Returns for nunber=2 ##########################
        [['Alexander Bykov', 'M', 21], ['Guoying Zhao', 'F', 21]]
        """

        with self.driver.session() as session:
            coauthors = session.run("MATCH (p:Professor)-[r:cooperateWith]-(p2) \
                                    RETURN p.name, p.gender, count(p2.name)\
                                    ORDER BY count(p2.name) DESC, p.gender\
                                    LIMIT $number" \
                                    ,number=numberOfProfessorsToReturn)
            return coauthors.values()




    # Returns the least number of hops from a professor to a female 
    def getShortestpathFromProfessorToFemale(self,professorName:str)->  

        """
        ####### Returns for I. Pitas ##############
        ('3', 'Amalia Miliou')
        """

        with self.driver.session() as session:
            path = session.run("MATCH (p1:Professor {name:$professorName}), (p2 {gender:$gender}), \
                            path = shortestPath((p1)-[:cooperateWith*]-(p2)) \
                            RETURN path", \
                            professorName=professorName,gender="F")
            try:
                #return str(len(path.value())) 
                return str(len(path.peek().values()[0])), path.value()[0].end_node["name"]
            except IndexError: # if professor doesn't has path for female
                return None 


