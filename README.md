![](https://svgsaur.us/?o=b&s=24&h=40&x=0&y=26&c=888&t=SOEN487A2)

# Flask Web Service Tutorial

This document will guide you through the creation of a Flask web service, from an empty directory to a simple REST api.

_The [`/example`](/example) folder contains all the files we will create for this tutorial._

### Setup

To follow along, you will need a few tools. First, we will need to have [`python`](https://www.python.org/downloads/) installed to be able to run the code. To help keep the dependency versions consistent, we will use [`pipenv`](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv). To make sure our api is behaving correctly, we will be calling it using `curl`, but anything that can send HTTP requests should work. We will also be using a text editor, you are free to use the one bundled with your operating system, or use your preferred option.

### Installation

Once you've picked a working directory, we will open a shell window in that directory and run:

```shell
$ pipenv shell --three
```

This will create a file named `Pipfile` and open a new shell (in the same window) which uses that `Pipfile`'s settings.

We can now install the Flask using:

```shell
$ pipenv install Flask
```

The contents of the `Pipfile` should now have changed to include a `[packages]` section, with an entry for Flask. This will also create a new `Pipfile.lock` file which is what is used to ensure collaborators always use the same version of the dependencies.

### Hello World

We are now ready to start writing our application. We start by creating a file called `main.py`, your working directory should now look like this:

```tree
.
├── main.py
├── Pipfile
└── Pipfile.lock
```

Opening `main.py` in the selected text editor, we can write our first endpoint:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
```

This code first imports Flask and creates an `app` instance. We then define a route handler to respond to requests with `Hello World!`.

To run the application, navigate back to the `pipenv` shell and run:

```shell
$ python main.py
```

_The same command can be reused to start the application again after making changes._

_To stop the running app, return to the shell and press `ctrl+c`._

You can now open [`http://localhost:5000/`](http://localhost:5000/) in your browser, it will display the hello message.

Alternatively, we can use the `curl` command in a different shell:

```shell
$ curl http://localhost:5000/
Hello World!
```

### Random words

The application we are building will be used to store and retrieve words. To make sure we have something to read from, we will generate a list of random words every time the app starts. This means we will need to install a second package to help generate these random words

```shell
$ pipenv install random-words
```

Back in the `main.py` file, we can now import this new package and use it to generate a list of 100 random words.

We also want to import a new function from Flask to help us return JSON-encoded data, which is a standard format that is easy to consume for the users of our api.

```diff
- from flask import Flask
+ from flask import Flask, jsonify
+ from random_word import RandomWords

  app = Flask(__name__)
+ words = RandomWords().get_random_words(limit=100)
```

We will now add an endpoint in `main.py` which will return all the words we have stored

```python
@app.route("/api/word", methods=["GET"])
def get_words():
    return jsonify(words)
```

Notice that the only allowed method for this endpoint is `GET`. This is partly by convention, but also because we will be adding a handler for different methods later in the tutorial. In a similar vein, the route for this endpoint is prefixed with `/api` to make it clear that it is indeed an api.

Like before, we can use the browser (or shell command) to see our endpoint in action at `http://localhost:5000/api/word`. (Remember to restart the application to make the changes take effect)

We will also add an endpoint to return single words from the list using their index:

```python
@app.route("/api/word/<int:index>", methods=["GET"])
def get_word(index):
    return jsonify(words[index])
```

For this endpoint, the path contains special syntax which reads the integer index before running our handler.

With these two endpoints, we have the established the basic pattern for how resources (in our case words) are made accessible using the REST pattern.

### Adding Words

We now want to allow the users of the api to be able to submit new words to the list. To follow the REST pattern, we will add a new handler for requests using the `POST` verb and use the same resource path as in the previous section.

We must first import `request` from Flask to be able to access the data being sent:

```diff
- from flask import Flask, jsonify
+ from flask import Flask, jsonify, request
```

The new endpoint can be written as follows:

```python
@app.route("/api/word", methods=["POST"])
def post_word():
    words.append(str(request.get_data(), "utf8"))
    return str(len(words) - 1)
```

Using `curl`, we can now add words to the list using the following command:

```shell
$ curl -X POST -d 'new-word' http://localhost:5000/api/word
100
```

Our handler will add the word to the list and respond with the index of the newly inserted word. For example, given the previous output, we can query for the new word using:

```shell
$ curl http://localhost:5000/api/word/100
"new-word"
```

We should also see the new word at the end of the complete list of words (`/api/word`).

### Handling Errors

As you may have noticed, our api is missing critical error handling. Notably, when getting a word by its index, there are no checks that the index is inside the list of words. To make sure that the client understands the reason why their request failed, REST apis should use _status codes_. These codes has a specific meaning, which will help diagnose the reason for the failure and act accordingly.

Until now, our handlers have been returning a status code of `200` (if they do not encounter an error). This code is the generic "everything is ok", and means the request was successfully handled.

Another status code in the "success" range is `201`, which means "resource created successfully". We will start by making our word-adding endpoint respond with this status after it enters a new word successfully:

```diff
  @app.route("/api/word", methods=["POST"])
  def post_word():
      words.append(str(request.get_data(), "utf8"))
-     return str(len(words) - 1)
+     return str(len(words) - 1), 201
```

Next, we will be adding a check to the word-getting endpoint. We want to tell the client if the index they requested is out of range of the list of words using status code `404`, which means "not found":

```diff
  @app.route("/api/word/<int:index>", methods=["GET"])
  def get_word(index):
+     if (index >= len(words)):
+         return "Not Found", 404
      return jsonify(words[index])
```

For our last example, we will be adding validation to the word-adding endpoint. We want to validate that the request actually contains a word. If the request body has no data, it should respond with status code `400`, which means "bad request" or "client error":

```diff
  @app.route("/api/word", methods=["POST"])
  def post_word():
+     if (not request.get_data()):
+         return "Bad Request", 400
      words.append(str(request.get_data(), "utf8"))
      return str(len(words) - 1), 201
```

### Next Steps

Although many of the basics for creating a REST api are covered in this document, there is still much to explore. Almost every website will need to store and retrieve data for its users. We have been using an in-memory list until now, but this would be a totally inappropriate way to handle real user data. Instead, we should use one of the many database management systems (like [PostgreSQL](https://www.postgresql.org/), [MySQL](https://www.mysql.com/) or [SQLite](https://www.sqlite.org/index.html)) and packages to interface with them (like [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)).

In terms of code organization, we will also want to split up our handlers into multiple files as the number of them grows with our application. This can be done using Flask [blueprints](http://flask.pocoo.org/docs/1.0/tutorial/views/).

It is also critical to make sure that our api is well documented to help the developers tasked with taking advantage of it. The current industry standard to describe REST apis is the [OpenAPI Specification](https://swagger.io/docs/specification/about/).

![](https://svgsaur.us/?s=60&w=200&h=80&x=20&y=60&t=🚀)
