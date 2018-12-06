#!/usr/bin/env python

import sys
import nltk
import re
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter

class Stats:

    def __init__(self, entry):
        self.entry = entry

        #save text to file
        f = open('entry.txt', 'w')
        f.write(self.entry + '\n')
        f.close()

    def __del__(self):
        os.remove('entry.txt')

    def getTotalWords(self):
        total_words = 0

        #open file
        with open('entry.txt') as entry:

            #iterate through each word in file
            for line in entry.readlines():
                for word in line.split():
                    #increment count
                    total_words += 1

        return total_words

    def getTenseDist(self):

        #get input body of text
        e = open('entry.txt').read()

        #tokenize the file by word
        word_list = nltk.word_tokenize(e)

        #tag each part of speech and store in list
        word_tag_list = nltk.pos_tag(word_list)

        #iterate through words and count occurrences of words and tags
        #word_count = Counter(word for word,tag in word_tag_list)
        #tag_count = Counter(tag for word,tag in word_tag_list)

        #split into past/present/future
        past_tags = filter(lambda x: x[1] == 'VBD' or x[1] == 'VBN', word_tag_list)
        present_tags = filter(lambda x: x[1] == 'VBG' or x[1] == 'VBP' or x[1] == 'VBZ', word_tag_list)
        future_tags = filter(lambda x: x[1] == 'MD', word_tag_list)

        #convert filter objects to lists
        past_list = list(past_tags)
        present_list = list(present_tags)
        future_list = list(future_tags)

        #count occurences
        past_count = len(past_list)
        present_count = len(present_list)
        future_count = len(future_list)
        total_count = past_count + present_count + future_count

        if (total_count == 0) {
            total_count = 1;
        }

        tense_tuple = (round((past_count/total_count) * 100), round((present_count/total_count) * 100), round((future_count/total_count) * 100))
        return tense_tuple

    def getPolarizedScores(self):
        #get input body of text
        e = open('entry.txt').read()

        #tokenize the file by sentence
        sentence_list = nltk.sent_tokenize(e)

        #declare vars
        total_neg = 0
        total_neu = 0
        total_pos = 0
        total_com = 0
        total = 0
        num_sent = 0;

        #load object
        sid = SentimentIntensityAnalyzer()

        #determine score for each sentence
        for sentence in sentence_list:

            scores = sid.polarity_scores(sentence)
            for score in scores:
                if score == "neg":
                    total_neg += scores[score]
                elif score == "neu":
                    total_neu += scores[score]
                elif score == "pos":
                    total_pos += scores[score]
                else:
                    total_com += scores[score]

                #print(score)
                #print(scores[score])

            #print("========================================")

            #print("{:-<40}\n{}\n".format(sentence, str(ss)))

        #print(total_neg)
        #print(total_neu)
        #print(total_pos)
        #print(total_com)

        total = total_neg + total_neu + total_pos           #also equals to number of sentences

        #make tuple of scores
        total_scores = (round((total_neg/total) * 100), round((total_neu/total) * 100), round((total_pos/total) * 100), round((total_com/total) * 100), round(total))

        return total_scores

    def getPolarizedWords(self):
        #get input body of text
        e = open('entry.txt').read()

        #tokenize the file by sentence
        sentence_list = nltk.sent_tokenize(e)

        #declare lists
        pos_word_list=[]
        neu_word_list=[]
        neg_word_list=[]

        #iterate through list
        for sentence in sentence_list:
            #tokenize by word
            tokenized_sentence = nltk.word_tokenize(sentence)

            #load object
            sid = SentimentIntensityAnalyzer()

            #split words by polarity
            for word in tokenized_sentence:
                if (sid.polarity_scores(word)['compound']) >= 0.1:
                    pos_word_list.append(word)
                elif (sid.polarity_scores(word)['compound']) <= -0.1:
                    neg_word_list.append(word)
                else:
                    neu_word_list.append(word)

            #score = sid.polarity_scores(sentence)
            #print('\nScores:', score)
            #print("========================================")

        #make tuple of lists
        word_polarity = (neg_word_list, neu_word_list, pos_word_list)

        return word_polarity
