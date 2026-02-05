from wordfreq import zipf_frequency # type: ignore
from wordfreq import tokenize # type: ignore
import PyPDF2

lang = "it"
words = []
frequency = []
pdf_path_en = r"C:\Users\Utente\projects\end2025\detector\book_en.pdf"
pdf_path_it = r"C:\Users\Utente\projects\end2025\detector\book_it.pdf"
txt_path_en = r"C:\Users\Utente\projects\end2025\detector\book_en.txt"
txt_path_it = r"C:\Users\Utente\projects\end2025\detector\book_it.txt"


def reader():
    if lang == "en":
        pdf_path = pdf_path_en
        txt_path = txt_path_en
    if lang == "it":
        pdf_path = pdf_path_it
        txt_path = txt_path_it
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:  # only append if not None
                text += page_text + "\n"
            else:
                print(f"Warning: page {i} returned no text")

    # Write to file
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    
def textfilewords(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    tokens = tokenize(text, "en")
    return tokens

def frequency_word(wordlist, language):
    freq_list = []
    for word in wordlist:
        frequency = zipf_frequency(word, language)
        freq_list.append(frequency)
    return freq_list

def frequency_decoder(frequency):
    freqnumbers = []
    for value in frequency:
        uNlog = 10**value
        unlog = int(round(uNlog))
        freqnumbers.append(unlog)
    return freqnumbers

def frequency_counter(values):
    magnitudes = {i: [] for i in range(1, 9)}

    for zipf in values:
        z = int(round(zipf))
        if 1 <= z <= 8:
            magnitudes[z].append(zipf)
            
    frequencynumber = []
    for mag in magnitudes:
        frequencynumber.append(len(magnitudes[mag]))
        
    return frequencynumber

def wordlist():
    wordlist = []
    while True:
        word = input("> ").strip()
        if not word:
            break
        wordlist.append(word)
    return wordlist


def percentages():
    reader()
    reference = textfilewords(r"C:\Users\Utente\projects\end2025\detector\readings.txt")
    count2 = sum(int(n) for n in reference)
    ref_percentages = [int(n)/count2*100 for n in reference]
    
    words = textfilewords(r"C:\Users\Utente\projects\end2025\detector\detector.txt")
    #words = wordlist() #using a file instead of inputs
    frequency = frequency_word(words, lang)
    freqnumber = frequency_decoder(frequency)
    magnitude_count = frequency_counter(frequency)
    
    count1 = sum(magnitude_count)
    magnitude_percentages = [int(c)/count1*100 for c in magnitude_count]
    
    #print("valori su 1 miliardo: ", "\n", freqnumber)
    #print("quante parole di rarità da 1 a 8 magnitudo:", "\n", magnitude_count)
    #print("-------------------------------------------------------------------------")
    #print(repetitions)
    
    return {
        "reference_raw": reference,
        "reference_percentages": ref_percentages,
        "words": words,
        "frequency_values": frequency,
        "freqnumber": freqnumber,
        "magnitude_count": magnitude_count,
        "magnitude_percentages": magnitude_percentages,
    }
    
if __name__ == "__main__":
    data = percentages()
    print("\nReturned data keys:", list(data.keys()))