from neo4j import GraphDatabase
import pandas as pd


# The universities and their departments
universities_departments = {
               "University of Oulu" : ["CSEE"], \
               "University of Bochum": ["Faculty of Electrical Engineering and Information Technology", \
                                        "Department of Civil and Enviromental Engineering"],
               "University of Porto" : ["ECE", \
                                        "CS"],
               "University of Bordeaux" : ["CS", \
                                           "IME"],
               "University of Lodz" : ["IT", \
                                       "ApCS", \
                                       "MIS"],
               "University of Thessaloniki" : ["CS", \
                                               "ECE"]
                }



professors = pd.read_csv("professors.csv", header=0)
#professors = pd.read_csv("professors2.csv", header=0)


coauthors = pd.read_csv("coauthors.csv", header=0)
#coauthors = pd.read_csv("co.csv", header=0)


relations = pd.read_csv("relations.csv", header=0)
#relations = pd.read_csv("relations2.csv", header=0)



# Stores the universities and their departments in Neo4j
# Create the edges between the departments and the universities the belong
def storeUniversitiesAndDepartmentsInNeo4j(tx, universities:dict):
    for university, departments in universities.items():
        tx.run("CREATE (:University {name:$name})", name=university)
        for department in departments:
            tx.run("MATCH (u:University {name:$universityName}) \
                    CREATE (d:Department {name:$departmentName})-[:belongsTo]->(u)", \
                    departmentName=department, \
                    universityName=university)


# Stores the Professor of the universities in Neo4j
# create the edges between the professors and the department they work at
def storeProfessorInNeo4j(tx, professor):
        
    tx.run("CREATE (:Professor {name:$name, \
                               scholar_Id:$scholar_Id, \
                               gender:$gender, \
                               role:$role, \
                               url_picture:$picture, \
                               citedby:$citedby, \
                               citedby5y:$citedby5y, \
                               hindex:$hindex, \
                               hindex5y:$hindex5y, \
                               i10index:$i10index, \
                               i10index5y:$i10index5y, \
                               num_publications:$num_publications, \
                               cites_per_year:$cites_per_year, \
                               interests:$interests})", \
                               name=professor["name"], \
                               scholar_Id=professor["scholar_id"], \
                               gender=professor["gender"], \
                               role=professor["role"], \
                               picture=professor["url_picture"], \
                               citedby=professor["citedby"], \
                               citedby5y=professor["citedby5y"], \
                               hindex=professor["hindex"], \
                               hindex5y=professor["hindex5y"], \
                               i10index=professor["i10index"], \
                               i10index5y=professor["i10index5y"], \
                               num_publications=professor["num_publications"], \
                               cites_per_year=professor["cites_per_year"], \
                               interests=professor["interests"])

    tx.run("MATCH (p:Professor {name:$professorName}), (d:Department {name:$departmentName})-[:belongsTo]->(:University {name:$universityName})\
            CREATE (p)-[:worksAt]->(d)" \
            ,professorName=professor["name"] \
            ,departmentName=professor["department"] \
            ,universityName=professor["affiliation"])

# Stores the coauthors of the professors in Neo4j
def storeCoauthorInNeo4j(tx, coauthor):
        
    tx.run("CREATE (:Coauthor {name:$name, \
                               scholar_Id:$scholar_Id, \
                               affiliation:$affiliation, \
                               url_picture:$picture, \
                               citedby:$citedby, \
                               citedby5y:$citedby5y, \
                               hindex:$hindex, \
                               hindex5y:$hindex5y, \
                               i10index:$i10index, \
                               i10index5y:$i10index5y, \
                               num_publications:$num_publications})", \
                               name=coauthor["name"], \
                               scholar_Id=coauthor["scholar_id"], \
                               affiliation=coauthor["affiliation"], \
                               picture=coauthor["url_picture"], \
                               citedby=coauthor["citedby"], \
                               citedby5y=coauthor["citedby5y"], \
                               hindex=coauthor["hindex"], \
                               hindex5y=coauthor["hindex5y"], \
                               i10index=coauthor["i10index"], \
                               i10index5y=coauthor["i10index5y"], \
                               num_publications=coauthor["num_publications"]) 

                               #gender:$gender, \
                               #gender=coauthor["gender"], \

# Create the edges between the Professors and their coauthors
def connectoCoauthorToProfessor(tx,relation):
    tx.run("MATCH (p1:Professor {name:$professor}),(p2 {name:$coauthor}) \
            CREATE (p1)-[r:cooperateWith]->(p2)" \
            ,professor=relation["src"] \
            ,coauthor=relation["dst"])

# deletes all the data from Neo4j
def cleanNeo4j(session):
    session.run("MATCH ()-[r]->() DELETE r")
    session.run("MATCH (n) DELETE n")


def main():


    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "a"))

    with driver.session() as session:

        cleanNeo4j(session)

        session.write_transaction(storeUniversitiesAndDepartmentsInNeo4j,universities_departments)

        for index, professor in professors.iterrows():
            session.write_transaction(storeProfessorInNeo4j, professor)

        for index, coauthor in coauthors.iterrows():
            session.write_transaction(storeCoauthorInNeo4j, coauthor)

        for index, relation in relations.iterrows():
            session.write_transaction(connectoCoauthorToProfessor, relation)

    driver.close()


if __name__ == "__main__":
    main()

