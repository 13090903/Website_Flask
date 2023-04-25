from flask import Flask
from flask import render_template, request
import codecs
import re
import time

app = Flask(__name__)

text = None
fileObj = codecs.open("russian.txt", "r", "utf_8_sig")
all_words = set(fileObj.read().split("\n"))
fileObj.close()


@app.route('/', methods=['post', 'get'])
def index():
    global text
    if request.method == 'POST' and text is not None:
        text_input = request.form['text_input']
        return render_template('index.html', output_text=decrypt(text_input, all_words), text_input=text_input)
    else:
        text = ""
        return render_template('index.html')


def inversion_cipher_decrypt(words):
    new_words = []
    for i in range(len(words)):
        new_words.append(words[i][::-1])
    return new_words


def caesar_cipher_decrypt(words, rot):
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    new_alphabet = ""
    new_words = []
    for i in range(len(alphabet)):
        new_alphabet += alphabet[(i - rot) % 33]
    for w in words:
        word = ""
        for letter in w:
            word += new_alphabet[alphabet.find(letter)]
        new_words.append(word)
    return new_words


def atbash_cipher_decrypt(words):
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    new_alphabet = alphabet[::-1]
    new_words = []
    for w in words:
        word = ""
        for letter in w:
            word += new_alphabet[alphabet.find(letter)]
        new_words.append(word)
    return new_words


def decrypt(text, all_words):
    counter_of_right_words = 0
    decrypted_text = ""
    decrypted_text_possible_var = []
    text1 = re.sub(r'[^\w\s]', ' ', text)
    text1 = re.sub(r'\s+', ' ', text1)
    words = text1.lower().split(" ")

    for i in range(1, 33):
        decrypted_words = caesar_cipher_decrypt(words, i)
        start_counter = 0
        for w in decrypted_words:
            decrypted_text += w
            decrypted_text += " "
            start_counter += 1
            if w in all_words:
                counter_of_right_words += 1
            if start_counter >= 2 and counter_of_right_words < start_counter - 1:
                break
        if counter_of_right_words >= (len(words) - 2 if len(words) > 5 else len(words)):
            decrypted_text_possible_var.append(decrypted_text)
            decrypted_text = ""
        else:
            decrypted_text = ""
        counter_of_right_words = 0

    decrypted_words = inversion_cipher_decrypt(words)
    for w in decrypted_words:
        decrypted_text += w
        decrypted_text += " "
        if w in all_words:
            counter_of_right_words += 1
    if counter_of_right_words >= (len(words) - 2 if len(words) > 5 else len(words)):
        decrypted_text_possible_var.append(decrypted_text)
        decrypted_text = ""
    else:
        decrypted_text = ""
    counter_of_right_words = 0

    decrypted_words = atbash_cipher_decrypt(words)
    for w in decrypted_words:
        decrypted_text += w
        decrypted_text += " "
        if w in all_words:
            counter_of_right_words += 1
    if counter_of_right_words >= (len(words) - 2 if len(words) > 5 else len(words)):
        decrypted_text_possible_var.append(decrypted_text)

    all_texts = ""
    for i in range(len(decrypted_text_possible_var)):
        all_texts += decrypted_text_possible_var[i]
        if i != len(decrypted_text_possible_var) - 1:
            all_texts += "\n" + "//" + "\n"

    return all_texts


if __name__ == "__main__":
    app.run(debug=True)
