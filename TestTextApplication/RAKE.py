from __future__ import division
import operator
import nltk
import string
from SemanticSimilarity import *

#Based on http://sujitpal.blogspot.com/2013/03/implementing-rake-algorithm-with-nltk.html

#Functions
#punct will be 1 char and listed
def isPunct(word):
  return len(word) == 1 and word in string.punctuation

#Number will be able to be a float or an int.
def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

class RAKE(object):

    def __init__(self):
        self.stopwords = set(nltk.corpus.stopwords.words())
        self.top_fraction = 3 # consider top third candidate keywords by score
        self.sentences = []
        self.items = []

    def extract(self, text, incl_scores=False):
        self.sentences = nltk.sent_tokenize(text) #tokenize by sentence
        self.items = nltk.word_tokenize(text) 
        phrase_list = self._generate_candidate_keywords(self.sentences) #grab candidates by phrase
        word_scores = self._calculate_word_scores(phrase_list) #score words
        phrase_scores = self._calculate_phrase_scores(phrase_list, word_scores) #score phrases
        sorted_phrase_scores = sorted(phrase_scores.items(), key=operator.itemgetter(1), reverse=True) #sort scored phrases in decending order
        n_phrases = len(sorted_phrase_scores) #length of the sorted list
        if incl_scores:
          return sorted_phrase_scores[0:int(n_phrases/self.top_fraction)] #return top third scored candidates
        else:
          return map(lambda x: x[0], sorted_phrase_scores[0:int(n_phrases/self.top_fraction)]) #lambda loops through list, returning first element of each?

    def _generate_candidate_keywords(self, sentences): 
        phrase_list = []
        for sentence in sentences:
          words = map(lambda x: "|" if x in self.stopwords else x, nltk.word_tokenize(sentence.lower())) #tokenize sentence by word, taking out stopwords
          phrase = []
          for word in words:
            if word == "|" or isPunct(word): #checks for stopword symbol or puncuation
              if len(phrase) > 0:
                phrase_list.append(phrase) #keeps track of words between stopwords and puncuation, 
                phrase = []
            else:
              phrase.append(word)
        return phrase_list

    def _calculate_word_scores(self, phrase_list):
        word_freq = nltk.FreqDist()
        word_degree = nltk.FreqDist()
        for phrase in phrase_list:
          degree = len(list(filter(lambda x: not isNumeric(x), phrase))) - 1
          for word in phrase:
            word_freq[word] += 1
            word_degree[word] += degree # other words
        for word in word_freq.keys():
          word_degree[word] = word_degree[word] + word_freq[word] # itself
        # word score = deg(w) / freq(w)
        word_scores = {}
        for word in word_freq.keys():
          word_scores[word] = word_degree[word] / word_freq[word]
        return word_scores

    def _calculate_phrase_scores(self, phrase_list, word_scores):
        phrase_scores = {}
        for phrase in phrase_list:
          phrase_score = 0
          for word in phrase:
            phrase_score += word_scores[word]
          phrase_scores[" ".join(phrase)] = phrase_score
        return phrase_scores

    def search_text(self, query): #look through text, and return the sentence in which it is found.
        query_words = nltk.word_tokenize(query)
        for sentence in self.sentences: #check each sentence for the phrase
            neededWords = len(query_words)
            sentence_words = nltk.word_tokenize(sentence.lower())
            for word in query_words:
                if word in sentence_words:
                    neededWords -= 1
                else:
                    break
                if neededWords == 0:
                    return sentence  
           
        else:
            print("Could not find " + query + " in text")
            return None     

    def get_key_sentences(self, keyphrases, sentences):
        length = int(len(keyphrases) / 3)
        top_phrases = []
        for index, phrase in enumerate(keyphrases):
            top_phrases.append(phrase[0])
            if index == length + 1:
                break

        key_Sentences = []
        for phrase in top_phrases:
            sent = self.search_text(phrase)
            if sent != None and sent not in key_Sentences :
                key_Sentences.append(sent)

        return key_Sentences

    def clean_Text(self, sentences):
        cleanedText = []
        for sentence in sentences:
           cleanedText.append(sentence.replace('\n',''))
        return cleanedText
                
    def tally_Words(self, sentences):
        tally = 0
        for sentence in sentences:
            sent = nltk.word_tokenize(sentence)
            tally += len(sent)

        return tally

    def test(text):
        rakeObj = RAKE()
        keywords = rakeObj.extract(text, incl_scores=True)
        clean_text = rakeObj.clean_Text(rakeObj.get_key_sentences(keywords, rakeObj.sentences))
        clean_tally = rakeObj.tally_Words(clean_text)
        print (keywords)
        print ("")
        print (clean_text)
        print ("")
        print ("Cut " + str(len(rakeObj.items) - clean_tally) + " words.")
        print ("Summary " + str((clean_tally / len(rakeObj.items)) * 100) + "% of the length of the source.")


    
      
      
      