import wikipedia

word = "Mrocco"

def wiki_search(title):
    print(title)
    print(wikipedia.summary(title))

try:
    title = wikipedia.search(word)[0]
    wiki_search(title)
except:
    suggest = wikipedia.suggest(word)
    if suggest is None :
        print("Not found.")
    else:
        wiki_search(suggest.capitalize())