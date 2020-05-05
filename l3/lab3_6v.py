import nltk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
import time


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def open_file_and_input_text():
    file_name = fd.askopenfilename(filetypes=(("Pdf files", "*.pdf"),))
    if file_name != '':
        with open(file_name, 'r') as file:
            text = file.read()
            replace_text(text)


def replace_text(text):
    text.replace('\n', '')
    calculated_text.delete(1.0, END)
    calculated_text.insert(1.0, text)


def information():
    messagebox.askquestion("Help", "1. Input text or open file.\n"
                                   "2. Send button 'Ok'.\n"
                                   "3. Look at the painted syntax tree.", type='ok')


grammar = r"""
        NP: {<DT|JJ|NN.*>+}
        PP: {<IN><NP>}
        VP: {<VB.*><NP|PP|CLAUSE>+$}
        CLAUSE: {<NP><VP>}
        """


def draw_syntax_tree():
    start=time.time()
    text = calculated_text.get(1.0, END)
    text = text.replace('\n', '')
    if text != '':
        doc = nltk.word_tokenize(text)
        doc = nltk.pos_tag(doc)
        list_word_with_tag = []
        for item in doc:
            if item[1] != ',' and item[1] != '.':
                list_word_with_tag.append(item)
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(list_word_with_tag)
        result.draw()
    end=time.time()
    print("Total time: {:.1f}".format(end - start))


root = Tk()
root.title("Syntax parse tree")
root.resizable(width=False, height=False)
root.geometry("415x120+300+300")

label = Label(root, text='Input text: ')
label.grid(row=0, column=0)

calculated_text = Text(root, height=5, width=40, bd=3)
calculated_text.grid(row=0, column=1, sticky='nsew', columnspan=3, rowspan=4)

button1 = Button(text="Ok", width=10, command=draw_syntax_tree)
button1.grid(row=1, column=0)

button2 = Button(text="Open file", width=10, command=open_file_and_input_text)
button2.grid(row=2, column=0)

button3 = Button(text="Help?", width=10, command=information)
button3.grid(row=3, column=0)

root.mainloop()
