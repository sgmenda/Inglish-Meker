import json
import re
import eng_to_ipa as ipa
import random
from multiprocessing import Pool

ourMapping = dict()

mapEnglishToAnglish = dict()

with open("English-to-Anglish-Dictionary/dictionary.json") as toAnglishDictJSON:
    toAnglishDict = json.load(toAnglishDictJSON)

with open("english-words/words_dictionary.json") as englishWordsJSON:
    englishWords = json.load(englishWordsJSON)

for d in toAnglishDict:
    if toAnglishDict[d]["attested"] in ["", "-"]:
        continue
    attested_translations = toAnglishDict[d]["attested"].replace(';', ',')
    attested_translations = toAnglishDict[d]["attested"].replace('\n', ',')
    attested_translations = attested_translations.split(',')
    first_attested_translation = attested_translations[0]

    # Some special cases
    if first_attested_translation[:2] == "1.":
        first_attested_translation = first_attested_translation[2:].split("2.")[0]
    if first_attested_translation[:5] == "(cf. ":
        continue
    if first_attested_translation[-1:] == "-":
        continue

    while '(' in first_attested_translation:
        first_attested_translation = first_attested_translation.split('(')[0] + ")".join(first_attested_translation.split(')')[1:])
    mapEnglishToAnglish[d] = first_attested_translation

# print(mapEnglishToAnglish.values())

# rwords = random.sample(list(englishWords.keys()), 10)

# for i in ["yours", "umbrella"]:
# for i in englishWords.keys():
# for i in rwords:

def convert(i):
    word = ""
    if ipa.isin_cmu(i):
        word = ipa.convert(i, stress_marks="primary")

    if i in mapEnglishToAnglish:
        if ipa.isin_cmu(mapEnglishToAnglish[i]):
            word = ipa.convert(mapEnglishToAnglish[i], stress_marks="primary")
    
    if word == "":
        return []

    word = word.replace("ɑ", "aa")
    word = word.replace("æ", "a")
    word = word.replace("mən", "mon")
    word = word.replace("ə", "e")
    word = word.replace("ˈ", "")
    word = word.replace("ɛ", "e")
    word = word.replace("ɪ", "i")
    word = word.replace("ɔ", "o")
    word = word.replace("ʊ", "u")
    word = word.replace("ʧ", "ch")
    word = word.replace("ŋ", "ng")
    word = word.replace("ʃ", "sh")
    word = word.replace("j", "y")
    word = word.replace("ʤ", "j")
    word = word.replace("ʒ", "j")  # z
    word = word.replace("θ", "þ")

    return [(i, word)]

ourMapping = Pool(4).map(convert, englishWords.keys())

flatten = lambda l: [item for sublist in l for item in sublist]

ourMapping = dict(flatten(ourMapping))

with open('mapping.json', 'w') as outfile:
    json.dump(ourMapping, outfile)

print(ourMapping)
