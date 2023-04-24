from cltk.stem.telugu.indian_stemmer import IndianStemmer

stemmer = IndianStemmer()

word = 'తెలుగు'

morphological_forms = stemmer.generate(word)

print(morphological_forms)
