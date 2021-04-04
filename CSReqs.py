import sys

import requests

from bs4 import BeautifulSoup

import nltk

from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

from nltk.sentiment.vader import SentimentIntensityAnalyzer

import pandas as pd

import matplotlib.pyplot as plt

 

def parseInput(fileName):

    classesTaken = set()

    f = open(fileName)

    for line in f:

        classesTaken.add(line[:-1])

    f.close()

    return classesTaken

 

def main():

    fileName = sys.argv[1]

    classesTaken = parseInput(fileName)

 

    session = requests.Session()

    link = session.get(http://collegecatalog.uchicago.edu/thecollege/computerscience/)

    soup = BeautifulSoup(link.text.strip(), "html.parser")

    results = soup.find_all("td", "codecol")

    allClasses = list()

    for r in results:

        result = str(r.find("a", "bubblelink code"))[114:124]

        result = result.replace(u'\xa0', u' ')

        allClasses.append(result)

 

    allClasses = allClasses[1:-8]

    numCat = [0, 3, 2, 1, 18, 2, 2, 10]

    numEach = [1, 1, 1, 3, 1, 1, 1]

 

    beg = numCat[0]

    end = numCat[1]

    index = 0

 

    print("CLASSES LEFT TO TAKE:")

 

    for i in numCat[2:]:

        count = 0

        found = False

        for c in allClasses[beg:end]:

            if c in classesTaken:

                classesTaken.remove(c)

                found = True

                count = count + 1

        if not found or count < numEach[index]:

            print("You have "+ str(numEach[index]-count)+ " class(es) left from this list:")

            print(allClasses[beg:end])

        beg = end

        end = end + i

        index = index + 1

 

if __name__ == "__main__":

    main()
