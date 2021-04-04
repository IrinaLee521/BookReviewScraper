import sys
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

# Scrapes book reviews off of the Goodreads website
def getGoodreads(title):
    session = requests.Session()

    session.post("https://www.goodreads.com/user/sign_in", data=dict(
    email="irina.lee101@gmail.com",
    password="sdaerdoog"
    ))

    # Processes the book title and generates the book searchbar link
    arr = title.split(" ")
    book_title = ""
    for word in arr:
        book_title += word + "+"
    book_title = book_title[:-1]
    search_link = "https://www.goodreads.com/search?q=" + book_title + "&qid="

    # Generates the link to the book's review page
    search = session.get(search_link)
    soup = BeautifulSoup(search.text.strip(), "html.parser")
    link = "https://www.goodreads.com" + soup.find("a", "bookTitle")["href"]
    r = session.get(link)
    soup = BeautifulSoup(r.text.strip(), "html.parser")

    # Gets the reviews in bs4 format - find_all(tag, class)
    reviews = []
    for bs4 in soup.find_all("div", "reviewText stacked"):
        reviews += bs4.find_all("span", "readable")

    # Extracts the text from the bs4s
    texts = []
    for elem in reviews:
        texts.append(elem.text.strip())
    return texts


def clean_text_data(reviews):
    # Breaks reviews into word tokens
    tokenized_reviews = []
    for review in reviews:
        tokenized_reviews.append(word_tokenize(review))

    # Filters out non-essential words and punctuation
    filtered_reviews = []
    stop_words = set(stopwords.words("english"))
    punctuation = {'.', ',', '?', '!', '"', '|', '[', ']', '{', '}', '/', '-', '...'}
    for review in tokenized_reviews:
        filtered_review = []
        for word in review:
            if word not in stop_words and word not in punctuation:
                filtered_review.append(word)
        filtered_reviews.append(filtered_review)

    return filtered_reviews

def evaluateSentiments(reviews):
    sia = SentimentIntensityAnalyzer()
    pos_review_count = 0
    neg_review_count = 0
    neutral_review_count = 0

    for review in reviews:
        pos_count = 0
        neg_count = 0
        polarity_total = 0
        for word in review:
            score = sia.polarity_scores(word)['compound']
            polarity_total += score
            if score >= 0.5:
                pos_count += 1
            elif score <= -0.5:
                neg_count += 1
        print("Polarity Total: " + str(polarity_total) + "\t" + "Pos Words: " + str(pos_count) + "\t" + "Neg Words: " + str(neg_count))
        if (pos_count > neg_count):
            pos_review_count += 1
        elif (pos_count < neg_count):
            neg_review_count += 1
        else:
            neutral_review_count += 1
    print("Positive Reviews: " + str(pos_review_count))
    print("Negative Reviews: " + str(neg_review_count))
    print("Neutral Reviews: " +  str(neutral_review_count))


def main():
    reviews = getGoodreads(sys.argv[1])
    filtered_reviews = clean_text_data(reviews)
    print("Total Reviews: " + str(len(reviews)))
    evaluateSentiments(filtered_reviews)

if __name__ == "__main__":
    main()
