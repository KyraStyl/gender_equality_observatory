# Web scraping procedure for building the graph database

Built using the [Scholarly Python API, version 1.2.0](https://pypi.org/project/scholarly/)

---

__*Author csv structure*__:
- name: string (full name)
- id: int (Scholar id)
- gender: M/F
- role: string (role in affiliation)
- affiliation: string
- citedby: int
- citedby5y: int
- hindex: int
- hindex5y: int
- i10index: int
- i10index5y: int
- num_publications: int
- citations: string, e.g. ... 2018-954 2019-1048 ...
- interests: string, e.g. Wireless_Networks IoT

__*Coauthor csv structure*__:
- name: string (full name)
- id: int (Scholar id)
+ affiliation: string
+ citedby: int
+ citebyd5y: int
+ hindex: int
+ hindex5y: int
+ i10index: int
+ i10index5y: int
+ num_publications: int

__*Edges csv structure*__:
- node1: string (author full name)
- node2: string (coauthor full name)

------

Stages:
 - Stage 1: Retrieving the initial data
 - Stage 2: Improving Google Scholar search with alternative keywords
 - Stage 3: Retrieving AUTH staff
 - Stage 4: Retrieving h-index, i10-index and citedby information for authors
 - Stage 5: Requerying failed AUTH authors
 - Stage 6: Merging other university authors with AUTH authors
 - Stage 7: Retrieving coauthor data
 - Stage 8: Handling failed coauthors
 - Stage 9: Removing authors from coauthors
 - Stage 10: Requerying all authors to retrieve citations and interests
 - Stage 11: Making the initial graph data

*Each stage produces some data. Data from previous stages are passed on to the next ones.