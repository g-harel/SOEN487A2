from flask import Flask, jsonify
from random_word import RandomWords

app = Flask(__name__)
words = RandomWords().get_random_words(limit=100)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/api/word", methods=["GET"])
def get_words():
    return jsonify(words)

@app.route("/api/word/<int:index>", methods=["GET"])
def get_word(index):
    return jsonify(words[index % len(words)])

if __name__ == "__main__":
    app.run(host="0.0.0.0")
