from wordfreq import tokenize # type: ignore
from collections import Counter
from a1Detector_project import percentages
refer_words = percentages()
words = refer_words["words"]

def repetition_counter(words):
    wordcount = Counter(words)
    repetitions = {}
    for word, count in wordcount.items():
        if count > 1:
            repetitions.setdefault(count, []).append(word)
            
    sorted_pairs = sorted(
        [(count, word) for count, words in repetitions.items() for word in words],
        key=lambda x: (x[0], x[1])
    )
    
    return sorted_pairs

def textfilewords(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    tokens = tokenize(text, "en")
    return tokens

def word_repetitions():
    words = textfilewords(r"C:\Users\Utente\projects\end2025\detector\detector.txt")
    repetitions = repetition_counter(words)

    return {
        "repetitions" : repetitions
    }