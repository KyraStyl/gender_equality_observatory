from neo4j import GraphDatabase
from .models import Professor,driver

# Return the K professors that have the most coauthors
def getTopKProfessorsWithMostCoauthors(numberOfProfessorsToReturn:int)-> list:

    """
    ######## Returns for number=2 ##########################
    [['Nandana Rajatheva', 'M', 24], ['Jukka Riekki', 'M', 23]]
    """

    with driver.session() as session:
        coauthors = session.run("MATCH (p:Professor)-[r:cooperateWith]-(p2) \
                                RETURN p.name, p.gender, count(p2.name)\
                                ORDER BY count(p2.name) DESC, p.gender\
                                LIMIT $number" \
                                ,number=numberOfProfessorsToReturn)
        return coauthors.values()


# Returns the K professor with highest page rank score in the network in descending order
def topKProfessorsWithHighestPageRankScore(topK:int)-> list:

    """
    ########### Return for topk=3 ###############
    [['Nicolas PERRY', 'M', 6.9452032727334245], ['Georg Schmitz', 'M', 6.273291582755126], ['Peter Mark', 'M', 6.123292444521661]]
    """

    with driver.session() as session:
        topKProfessors = session.run("CALL gds.pageRank.stream('my-graph') \
                                    YIELD nodeId, score \
                                    WHERE labels(gds.util.asNode(nodeId)) = ['Professor'] \
                                    RETURN gds.util.asNode(nodeId).name AS name, gds.util.asNode(nodeId).gender AS gender, score \
                                    ORDER BY score DESC, gender \
                                    LIMIT $topK" \
                                    ,topK=topK)
        return topKProfessors.values()


# Returns the K professor with highest betweenes score in the network in descending order
def topKProfessorsWithHighestBetweenes(topK:int)-> list:

    """
    ########### Return for topk=3 ###############
    [['Jürgen Oehm', 'M', 276683.5748508272], ['Christos Katsanos', 'M', 203253.62510595468], ['João Canas Ferreira', 'M', 173018.887142207]]
    """

    with driver.session() as session:
        topKProfessors = session.run("CALL gds.betweenness.stream('my-graph') \
                                    YIELD nodeId, score \
                                    WHERE labels(gds.util.asNode(nodeId)) = ['Professor'] \
                                    RETURN gds.util.asNode(nodeId).name AS name, gds.util.asNode(nodeId).gender AS gender, score \
                                    ORDER BY score DESC, gender \
                                    LIMIT $topK" \
                                    ,topK=topK)
        return topKProfessors.values()


# Returns the K professor with highest degree centrality score in the network in descending order
def topKProfessorsWithHighestDegreeCentrality(topK:int)-> list:

    """
    ########### Return for topk=3 ###############
    [['Nandana Rajatheva', 'M', 48.0], ['Jari Iinatti', 'M', 46.0], ['Jukka Riekki', 'M', 46.0]]
    """

    with driver.session() as session:
        topKProfessors = session.run("CALL gds.degree.stream('my-graph',{ orientation: 'UNDIRECTED' }) \
                                    YIELD nodeId, score \
                                    WHERE labels(gds.util.asNode(nodeId)) = ['Professor'] \
                                    RETURN gds.util.asNode(nodeId).name AS name, gds.util.asNode(nodeId).gender AS gender, score \
                                    ORDER BY score DESC, gender \
                                    LIMIT $topK" \
                                    ,topK=topK)
        return topKProfessors.values()


# Returns the K professor with highest closeness centrality score in the network in descending order
def topKProfessorsWithHighestClosenessCentrality(topK:int)-> list:

    """
    ########### Return for topk=3 ###############
    [['Joanna Sekulska-Nalewajko', 'F', 1.0], ['Teresa Leão', 'F', 1.0], ['Mariusz Postół', 'M', 1.0]]
    """

    with driver.session() as session:
        topKProfessors = session.run("CALL gds.alpha.closeness.stream('my-graph') \
                                    YIELD nodeId, centrality \
                                    WHERE labels(gds.util.asNode(nodeId)) = ['Professor'] \
                                    RETURN gds.util.asNode(nodeId).name AS name, gds.util.asNode(nodeId).gender AS gender, centrality \
                                    ORDER BY centrality DESC, gender \
                                    LIMIT $topK" \
                                    ,topK=topK)
        return topKProfessors.values()

# Returns the K professor with highest closeness harmonic centrality score in the network in descending order
def topKProfessorsWithHighestClosenessHarmonicCentrality(topK:int)-> list:

    """
    ########### Return for topk=3 ###############
    [['Jukka Riekki', 'M', 0.18965481577492124], ['Timo Ojala', 'M', 0.18651939802165704], ['Erkki Harjula', 'M', 0.18560336187406978]]
    """

    with driver.session() as session:
        topKProfessors = session.run("CALL gds.alpha.closeness.harmonic.stream('my-graph') \
                                    YIELD nodeId, centrality \
                                    WHERE labels(gds.util.asNode(nodeId)) = ['Professor'] \
                                    RETURN gds.util.asNode(nodeId).name AS name, gds.util.asNode(nodeId).gender AS gender, centrality \
                                    ORDER BY centrality DESC, gender \
                                    LIMIT $topK" \
                                    ,topK=topK)
        return topKProfessors.values()


# Returns the K professor with highest spread information influenc score in the network in descending order
def topKProfessorsWithHighestSpreadInformationInfluence(topK:int)-> list:

    """
    ########### Return for topk=3 ###############
    [['Antti Tölli', 'M', 12.615], ['Erkki Harjula', 'M', 8.588], ['Andrew R. Gibson', 'M', 4.444]]
    """

    with driver.session() as session:
        topKProfessors = session.run("CALL gds.alpha.influenceMaximization.greedy.stream('my-graph',{seedSetSize:$topK}) \
                                    YIELD nodeId, spread \
                                    WHERE labels(gds.util.asNode(nodeId)) = ['Professor'] \
                                    RETURN gds.util.asNode(nodeId).name AS name, gds.util.asNode(nodeId).gender AS gender, spread \
                                    ORDER BY spread DESC, gender" \
                                    ,topK=topK)
        return topKProfessors.values()

# Returns the average triangles that a male/female professor participates
def getAvgOfTrianglesForMaleAndFemaleProfessors()-> list:

    """
    ########### Returns ###############
    [['M', 11.89160839160838], ['F', 6.784313725490197]]
    """

    with driver.session() as session:
        genderAverages = session.run("CALL gds.triangleCount.stream('my-graph') \
                                    YIELD nodeId, triangleCount \
                                    WHERE labels(gds.util.asNode(nodeId)) = ['Professor'] \
                                    RETURN gds.util.asNode(nodeId).gender AS gender, avg(triangleCount)" \
                                    )
        return genderAverages.values()

# Returns the average local clustering coefficient for male/female professor
def getAvgLocalClusteringCoefficientForMaleAndFemaleProfessor()-> list:

    """
    ########### Returns ###############
    [['M', 0.13881527930639231], ['F', 0.13646585140848477]]
    """

    with driver.session() as session:
        genderAverages = session.run("CALL gds.localClusteringCoefficient.stream('my-graph') \
                                    YIELD nodeId, localClusteringCoefficient \
                                    WHERE labels(gds.util.asNode(nodeId)) = ['Professor'] \
                                    RETURN gds.util.asNode(nodeId).gender AS gender, avg(localClusteringCoefficient)" \
                                    )
        return genderAverages.values()



# Returns the avg shortest path of a men/female professor to a female professor or coauthor in the network
def getAvgShortestpathFromProfessorToFemale()-> dict:

    """
    ####### Returns ##############
    {'Female': 5.918486133192016, 'Male': 5.980548730548734}
    """

    with driver.session() as session:

        Professors = session.run("MATCH (p:Professor) \
                                Return p.gender, collect(p.name) AS Professors")
        professors = Professors.data()
        professorsMen, professorsFemale = professors
        #print(professorsMen["Professors"])
        #print(professorsFemale["Professors"])

        femaleAvgShortestPath = 0
        maleAvgShortestPath = 0
        for index, allProfessorsOfAGender in enumerate([professorsMen["Professors"],professorsFemale["Professors"] ]):
            avgPathLengthOfEachProfessor = list()

            for professor in allProfessorsOfAGender:
                shortestPaths = session.run("MATCH (p:Professor {name:$professor}) \
                                        CALL gds.allShortestPaths.dijkstra.stream('my-graph', {sourceNode: p}) \
                                        YIELD index, sourceNode, targetNode, nodeIds, path \
                                        WHERE gds.util.asNode(targetNode).gender = $gender \
                                        RETURN path " \
                                        ,professor=professor,gender="F")
                pathLength = list()
                for path in shortestPaths.values():
                    pathLength.append(len(path[0]))
                if pathLength:
                    avgPathLength = sum(pathLength) / len(pathLength)
                    avgPathLengthOfEachProfessor.append(avgPathLength)
                else:
                    avgPathLengthOfEachProfessor.append(0)

            if index == 0:
               maleAvgShortestPath = sum(avgPathLengthOfEachProfessor) / len(avgPathLengthOfEachProfessor)
               print(maleAvgShortestPath)
            else:
               femaleAvgShortestPath = sum(avgPathLengthOfEachProfessor) / len(avgPathLengthOfEachProfessor)
               print(femaleAvgShortestPath)


        return {"Female":femaleAvgShortestPath, "Male":maleAvgShortestPath}


# Returns the avg shortest path of a men/female professor to a male professor or coauthor in the network
def getAvgShortestpathFromProfessorToMale()-> dict:

    """
    ####### Returns ##############
    {'Female': 6.103181626037764, 'Male': 6.01130447802985}
    """

    with driver.session() as session:

        Professors = session.run("MATCH (p:Professor) \
                                Return p.gender, collect(p.name) AS Professors")
        professors = Professors.data()
        professorsMen, professorsFemale = professors
        #print(professorsMen["Professors"])
        #print(professorsFemale["Professors"])

        femaleAvgShortestPath = 0
        maleAvgShortestPath = 0
        for index, allProfessorsOfAGender in enumerate([professorsMen["Professors"],professorsFemale["Professors"] ]):
            avgPathLengthOfEachProfessor = list()

            for professor in allProfessorsOfAGender:
                shortestPaths = session.run("MATCH (p:Professor {name:$professor}) \
                                        CALL gds.allShortestPaths.dijkstra.stream('my-graph', {sourceNode: p}) \
                                        YIELD index, sourceNode, targetNode, nodeIds, path \
                                        WHERE gds.util.asNode(targetNode).gender = $gender \
                                        RETURN path " \
                                        ,professor=professor,gender="M")
                pathLength = list()
                for path in shortestPaths.values():
                    pathLength.append(len(path[0]))
                if pathLength:
                    avgPathLength = sum(pathLength) / len(pathLength)
                    avgPathLengthOfEachProfessor.append(avgPathLength)
                else:
                    avgPathLengthOfEachProfessor.append(0)

            if index == 0:
               maleAvgShortestPath = sum(avgPathLengthOfEachProfessor) / len(avgPathLengthOfEachProfessor)
               print(maleAvgShortestPath)
            else:
               femaleAvgShortestPath = sum(avgPathLengthOfEachProfessor) / len(avgPathLengthOfEachProfessor)
               print(femaleAvgShortestPath)


        return {"Female":femaleAvgShortestPath, "Male":maleAvgShortestPath}
