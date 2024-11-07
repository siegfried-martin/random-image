import random

words = []
default_word_types = [
    "adjectives",
    "nouns",
    "verbs",
    "adjectives",
    "nouns"
]

#word type must have associated file of the form [word type].txt
#this file must contain a newline separated list of words
def load_words(word_types=default_word_types):
    for word_type in word_types:
        #print(f'{word_type}.txt')
        with open(f'{word_type}.txt', 'r') as file:
            lines = file.readlines()
            #print(len(lines))
            words.append({"type": word_type, "word_list": lines})

def getRandomPhrase():
    phrase = ""
    if not len(words):
        load_words()
    for word_group in words:
        if len(word_group["word_list"]):
            if phrase:
                phrase += " "
            phrase += random.choice(word_group["word_list"])
    return phrase.replace("\n", "")

#uncomment to test
#print(getRandomPhrase())
        