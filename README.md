# GENDER EQUALITY

![alt text](GenderEquality-HERO.jpg?raw=true)

## Motivation

The term "gender balance" refers to an equitable distribution of life's opportunities and resources between women and men, and/or the equal representation of women and men. In science and academia inequalities exist in different career stages from postgraduate level to top-tier academia.

## Description

This work aims to create a gender balance observatory on scientific research, by exploring curated data extracted from Google Scholar. More specifically, we created a web application that visualizes the analysis made on data collected for some faculty members, in order to be presented and emphasized the inequality of the two genders, in academia.

## Universities Participating
[1. Univeristy of Porto](https://www.up.pt/) <br>
[2. University of Bordeaux](https://www.u-bordeaux.fr/) <br>
[3. University of Oulu](https://www.oulu.fi/fi) <br>
[4. University of Lodz](https://p.lodz.pl/) <br>
[5. University of Bochum](https://www.ruhr-uni-bochum.de/en) <br>
[6. Aristotle University of Thessaloniki](https://www.auth.gr/) <br>

## How To Run Flask App

###1. Run docker image of Neo4j with gds plugin
```
sudo docker run -it --rm --publish=7474:7474 --publish=7687:7687 --user="$(id -u):$(id -g)" -e NEO4J_AUTH=none --env NEO4JLABS_PLUGINS='["graph-data-science"]' neo4j:4.2
```

###2. Install all the necessary libraries in python
```
pip install -r webapp/requirements.txt
```

###3. Load the Neo4j Database
```
python 3 dataset/databaseLoading.py
```

###4. Run the Flask App
```
./start-flask-app.sh
```

###5. Visit Web Application at http://127.0.0.1:5000/
