import nltk
import sys
import datetime
from nltk.sentiment import vader
import sqlite3
from PIL import ImageTk, Image


def index_calc(choice_value, review1):
    choice = int(choice_value)
    print (choice)

    #print'=============================================================='
    #print '1: Sentiment Analysis on Movie Reviews'
    #print '2: Sentiment Analysis from tweets'
    #print '3: Exit'
    #print'=============================================================='"""
    # C:\\Users\\Admin\\PycharmProjects\\Sentiment\\rt-polaritydata\\rt-polaritydata\\rt-polaritypos.txt

    # C:\\Users\\Admin\\PycharmProjects\\Sentiment\\rt-polaritydata\\rt-polaritydata\\rt-polarityneg.txt"
    db = sqlite3.connect('Database')
    c = db.cursor()
    #c.execute('''CREATE TABLE pic(name text, picture BLOB)''')


    #sql = '''INSERT INTO pic VALUES(?, ?);'''
    #c.execute(sql, ['neg', buffer(sqlite3.Binary(p1))])
    #c.execute(sql, ['pos', buffer(sqlite3.Binary(p2))])

    # aq = c.execute('SELECT * FROM temp WHERE name=pos')
    # print aq
    #choice = input('Enter Your Choice :')
    if choice == 1:
        positiveReviewsFileName = "./lib\\rt-polaritypos.txt"
        negativeReviewsFileName = "./lib\\rt-polarityneg.txt"
        msg = review1

        print ("\nAnalyzing the Review..."  "\t\tExec. starts at: " + datetime.datetime.now().strftime('%H:%M:%S'))

        with open(positiveReviewsFileName, 'r') as f:
            positiveReviews = f.readlines()
        with open(negativeReviewsFileName, 'r') as f:
            negativeReviews = f.readlines()


        testTrainingSplitIndex = 2500

        testNegativeReviews = negativeReviews[testTrainingSplitIndex + 1:]
        testPositiveReviews = positiveReviews[testTrainingSplitIndex + 1:]
        trainingNegativeReviews = negativeReviews[:testTrainingSplitIndex]
        trainingPositiveReviews = positiveReviews[:testTrainingSplitIndex]

        def getTestReviewSentiments(naive_bayes_sentiment_calculator):
            testNegResults = [naive_bayes_sentiment_calculator(review) for review in testNegativeReviews]
            testPosResults = [naive_bayes_sentiment_calculator(review) for review in testPositiveReviews]
            labelToNum = {'positive': 1, 'negative': -1}
            numericNegresults = [labelToNum[x] for x in testNegResults]
            numericPosResults = [labelToNum[x] for x in testPosResults]
            return {'results-on-positive': numericPosResults, 'results-on-negative': numericNegresults}


        def getVocabulary():
            positiveWordList = [word for line in trainingPositiveReviews for word in line.split()]
            negativeWordList = [word for line in trainingNegativeReviews for word in line.split()]
            allWordList = [item for sublist in [positiveWordList, negativeWordList] for item in sublist]
            allWordSet = list(set(allWordList))
            vocabulary = allWordSet
            word_features = list(nltk.FreqDist(vocabulary).keys())[:3000]
            return word_features


        def getTrainingData():
            negTaggedTrainingReviewList = [{'review': oneReview.split(), 'label': 'negative'} for oneReview in trainingNegativeReviews]
            posTaggedTrainingReviewList = [{'review': oneReview.split(), 'label': 'positive'} for oneReview in trainingPositiveReviews]
            fullTaggedTrainingData = [item for sublist in [negTaggedTrainingReviewList, posTaggedTrainingReviewList] for item in sublist]
            trainingData = [(review['review'], review['label']) for review in fullTaggedTrainingData]

            return trainingData

        def find_features(review):
            words = set(review)
            features = {}
            for w in vocabulary:
                features[w] = (w in words)

            return features


        def extract_features(review):
            #i = 1
            review_words = set(review)
            features = {}
            for word in vocabulary:
                features[word] = (word in review_words)
            return features


        def getTrainedNaiveBayesClassifier(find_features, trainingData):
            trainingFeatures = nltk.classify.apply_features(find_features, trainingData)
            trainedNBClassifier = nltk.NaiveBayesClassifier.train(trainingFeatures)

            return trainedNBClassifier

        vocabulary = getVocabulary()
        trainingData = getTrainingData()
        trainedNBClassifier1 = getTrainedNaiveBayesClassifier(find_features, trainingData)

        def naive_bayes_sentiment_calculator(review):

            problemInstance = review.split()
            problemFeatures = find_features(problemInstance)
            return trainedNBClassifier1.classify(problemFeatures)

        re = naive_bayes_sentiment_calculator(msg)

        inten = vader.SentimentIntensityAnalyzer()
        q = inten.polarity_scores(msg)['compound']
        q1 = inten.polarity_scores(msg)['neg']
        q2 = inten.polarity_scores(msg)['neu']
        if q1 == 0.0:
            re = "positive"

        print ("\nThe Review Was \"" + msg + "\"\n")

        print ("The Sentiment Behind the Review --> " + re + "\n")

        print (re + " Score is " + str(q) + "\t\tgot output at: " + datetime.datetime.now().strftime('%H:%M:%S') + "\n\n")

            # print(datetime.datetime.now().strftime('%H:%M:%S'))
            # rr = naive_bayes_sentiment_calculator("What a terrible movie")
            # print rr

    elif choice == 2:
        print 'no'
    else:
        sys.exit()
    return re, q






