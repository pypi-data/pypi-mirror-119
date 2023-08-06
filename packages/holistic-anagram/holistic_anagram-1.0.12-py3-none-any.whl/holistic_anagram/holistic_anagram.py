import os
from .english_heroku import heroku_words

class Anagram(object):
    
    __author__ = 'Michael S. Russell'
    __email__ = 'michael.r2014@yahoo.co.uk'
    __version__ = '1.0.12'
    
    def __init__(self):
        
        self.words = None
        self.real_words = []
        self.res = {}
        self.sentence = ""
        self.json = {"anagram": [], "non-anagram": []}
        self.path = os.getcwd()
    
    def init_app(self, heroku=False):
        
        if heroku:
            
            self.words = heroku_words.split(" ")
            
        else:
            
            with open(self.path + "\\english.txt", "r") as r:
                words = r.read().replace("\n", ",").split(",")

            self.words = words
        
    
    def enter_words_print(self):
            
        self.sentence = input("Enter words for anagram algo: ")

        mylist = self.sentence.split(" ")
    
        mylist = list(set(mylist))

        for word in mylist:

            if word in self.words:

                self.real_words.append(word)

        for word in self.real_words:

            self.res[tuple(sorted(word))] = []

        for key in self.res:

            for word in self.real_words:

                if tuple(sorted(word)) == key:

                    self.res[key].append(word)
            
        for w in list(self.res.values()):

            if len(w) >= 2:
                print("Anagram :", w)

            else:

                print("Not an anagram :", w)
            print()
            
        self.real_words = []
        self.res = {}
        self.sentence = ""

    
    def enter_words_json(self, sentence):
            
        self.sentence = sentence

        mylist = self.sentence.split(" ")
    
        mylist = list(set(mylist))

        for word in mylist:

            if word in self.words:

                self.real_words.append(word)

        for word in self.real_words:

            self.res[tuple(sorted(word))] = []

        for key in self.res:

            for word in self.real_words:

                if tuple(sorted(word)) == key:

                    self.res[key].append(word)
                    
            
        for w in list(self.res.values()):

            if len(w) >= 2:
                
                self.json["anagram"].append(w)

            else:

                self.json["non-anagram"].append(w)
                
        data = self.json
        self.real_words = []
        self.res = {}
        self.sentence = ""
        self.json = {"anagram": [], "non-anagram": []}
        
        return data
    
