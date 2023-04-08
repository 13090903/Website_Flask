from flask import Flask
from flask import render_template, request
import codecs

app = Flask(__name__)


@app.route('/', methods=['post', 'get'])
def home():
    params_post = {}
    text = ""
    for p in request.form:
        params_post[p] = request.form[p]
        text = params_post[p]
    return render_template('index.html', params_post=decrypt(text))


def inversion_cipher_decrypt(words):
    new_words = []
    for i in range(len(words)):
        new_words.append(words[i][::-1])
    return new_words


def caesar_cipher_decrypt(words, rot):
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
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


def decrypt(text):
    fileObj = codecs.open("russian.txt", "r", "utf_8_sig")
    all_words = fileObj.read().split("\n")
    fileObj.close()
    counter_of_right_words = 0
    decrypted_text = ""
    decrypted_text_possible_var = []
    words = text.lower().split(" ")

    for i in range(1, 33):
        decrypted_words = caesar_cipher_decrypt(words, i)
        for w in decrypted_words:
            if w in all_words:
                counter_of_right_words += 1
                decrypted_text += w
        if counter_of_right_words == len(words):
            decrypted_text_possible_var.append(decrypted_text)
        counter_of_right_words = 0

    decrypted_words = inversion_cipher_decrypt(words)
    for w in decrypted_words:
        decrypted_text += w
        decrypted_text += " "
        if w in all_words:
            counter_of_right_words += 1
    if counter_of_right_words >= len(words) if len(words) < 3 else len(words) // 2:
        decrypted_text_possible_var.append(decrypted_text)

    return decrypted_text_possible_var


print(decrypt("тевирп ток аааа"))

if __name__ == "__main__":
    app.run()
