from bs4 import BeautifulSoup
import time
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *


def distance(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def getIncorrectWord():
    incorrect_word = misspelled_word.get(1.0, END)
    incorrect_word = incorrect_word.replace('\n', '')
    incorrect_word = incorrect_word.replace('\r', '')
    return incorrect_word 


def calculateWordsDistance(correct_words):
    incorrect_word = getIncorrectWord()
    correct_words_with_distance = {}
    for word in correct_words:
        error = distance(word, incorrect_word)
        correct_words_with_distance.update({word : error})
    return correct_words_with_distance


def getFilename():
    filename = filedialog.askopenfilename(filetypes=(("HTML files", "*.html"),))
    return filename


def getCorrectWords(filename):
    with open(filename, encoding='utf-8') as html:
        soup = BeautifulSoup(html.read(), 'html.parser')
        p = soup.find_all('p')
        correct_words = []
        for x in p:
            correct_words.append(str(x.text))
    return correct_words


def sortWordsByDistance(correct_words_with_distance):
    tuples = list(correct_words_with_distance.items())
    tuples.sort(key = lambda i : i[1])
    return tuples


def renderTextResult(tuples):
    error = number_of_errors.get(1.0, END)
    for word in tuples[::-1]:
        if int(word[1]) < int(error) + 1:
            list_box.insert(0, str(word[0]) + ' ' + str(word[1])) 

def info():
    messagebox.askquestion("Help", "1. Открыть файл  с правильными словами.\n"
                                   "2. Написать в первой строке неправильное слово.\n"
                                   "3. Написать во второй строке количество допустимых ошибок.\n"
                                   "4. Снизу увидите упорядоченный список с вариантами.", type='ok')



def showResult():
    start=time.time()
    if (misspelled_word.get(1.0, END) != '\n' and number_of_errors.get(1.0, END) != '\n'):
        list_box.delete(0,'end')
        filename = getFilename()
        correct_words = getCorrectWords(filename)
        correct_words_with_distance = calculateWordsDistance(correct_words)
        tuples = sortWordsByDistance(correct_words_with_distance)
        renderTextResult(tuples)
    else:
        return
    end=time.time()
    print("Total time: {:.1f}".format(end - start))


root = Tk()
root.title("Words founder")
root.resizable(width=False, height=False)
root.geometry("480x250+300+300")
label = Label(root, text='Enter the word:')
label.grid(row=1, column=1)
misspelled_word = Text(root, height=1, width=20)
misspelled_word.grid(row=1, column=2, sticky='nsew', columnspan=3)
label2 = Label(root, text='Number of errors:')
label2.grid(row=2, column=1)
number_of_errors = Text(root, height=1, width=5)
number_of_errors.grid(row=2, column=2, sticky='nsew', columnspan=3)

b1 = Button(text="Done", command = showResult)
b1.grid(row=2, column=0)
b2 = Button(text="Help", command = info)
b2.grid(row=1, column=5)
list_box = Listbox(root, height=10, width=65)
scrollbar = Scrollbar(root, command=list_box.yview)
scrollbar.grid(row=4, column=4, sticky='nsew')
list_box.grid(row=4, column=0, sticky='nsew', columnspan=3)
list_box.configure(yscrollcommand=scrollbar.set)
root.mainloop()
