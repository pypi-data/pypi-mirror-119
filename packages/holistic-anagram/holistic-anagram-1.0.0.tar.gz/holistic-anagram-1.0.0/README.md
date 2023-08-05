# ANAGRAM READ ME 

There are several methods that can be used in the holistic_anagram.py file. These include:

- init_app
- enter_words_print
- enter_words_json


### Install

**Note: python-anagram requires python3**

```shell
pip install holistic-anagram
```

### Website using python-anagram
- (anagram website example)[https://holistic-anagram.herokuapp.com/]


### Steps on how to use python-anagram package
1. Create an instance of your anagram. Example: anagram = Anagram()
2. Initialize your instance. anagram.init_app(). This allows the app to check if a word is real or not.
3. You can then enter words using `enter_words_print` method or
`enter_words_json`. The former is as an interactive script using the input function.
The later requires the sentence argument, and generates json data to be used in a web application e.g. in FastAPI, Flask, Django, etc.

### Example of use
- Type in `bats tabs tekken attack on titan no rats tsar star tops tops spot stop psto psto pots`
- This will remove the non-English words, remove duplicates and leave you with:
`bats tabs attack on titan no rats tsar star tops spot stop`
- It then checks if any of the words are anagrams of each other.
- Output is either a print statement or returns json formatted data.


### Dependencies
- No dependencies

### Python versions
 - 3.7.x
 - 3.8.x
 - 3.9.x

