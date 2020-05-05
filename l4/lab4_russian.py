# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from wordcloud import WordCloud
from tkinter import filedialog as fd
from wiki_ru_wordnet import WikiWordnet


def info():
    messagebox.askquestion("Help", "1. Введите одно слово или откройте файл с одним словом.\n"
                                   "2. Нажмите кнопку 'Готово'.\n"
                                   "3. Посмотрите на картинку.", type='ok')


def get_file():
    file_name = fd.askopenfilename(filetypes=(("Txt files", "*.txt"),))
    if file_name != '':
        with open(file_name, 'r') as file:
            text = file.read()
            calculated_text.delete(1.0, END)
            calculated_text.insert(1.0, text)


def check_word(word):
    list_symbol = list(word)
    for i in list_symbol:
        if i == ' ':
            return False
    return True


def viewWindow():
    text = calculated_text.get(1.0, END)
    text = text.replace('\n', '')
    if text != '':
        check = check_word(text)
        if not check:
            messagebox.showwarning('Внимание!!!', 'Одно слово!', type='ok')
        else:
            wiki_wordnet = WikiWordnet()
            syn=wiki_wordnet.get_synsets(text.lower())
            text = ''
            for l in syn[0].get_words():
                text += l.lemma() + ' '
            for i in wiki_wordnet.get_hyponyms(syn[0]):
                for hyponym in i.get_words():
                    text += hyponym.lemma() + ' '
            for j in wiki_wordnet.get_hypernyms(syn[0]):
                for hypernym in j.get_words():
                    text += hypernym.lemma() + ' '
            wordcloud = WordCloud(
                relative_scaling=1.0,
            ).generate(text)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()


root = Tk()
root.title("Семмантическое разбиение русского слова")
root.resizable(width=False, height=False)
root.geometry("420x60+300+300")

label = Label(root, text='Введите слово:')
label.grid(row=2, column=0)
calculated_text = Text(root, height=1, width=40)
calculated_text.grid(row=2, column=1, sticky='nsew', columnspan=3)
button1 = Button(text="Готово", width=10, command=viewWindow)
button1.grid(row=3, column=1)
button2 = Button(text="Открыть", width=10, command=get_file)
button2.grid(row=3, column=2)
button3 = Button(text="Помощь?", width=10, command=info)
button3.grid(row=3, column=3)

root.mainloop()
