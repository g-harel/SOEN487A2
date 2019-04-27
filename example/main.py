from flask import Flask, jsonify, request
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
    if (index >= len(words)):
        return "Not Found", 404
    return jsonify(words[index])

@app.route("/api/word", methods=["POST"])
def post_word():
    if (not request.get_data()):
        return "Bad Request", 400
    words.append(str(request.get_data(), "utf8"))
    return str(len(words) - 1), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0")
