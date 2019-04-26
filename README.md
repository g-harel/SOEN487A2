# SOEN487A2

---

# Flask Web Service Tutorial

This document will guide you through the creation of a Flask web service, from an empty directory to a simple REST api.

_The [`/example`](/example) folder contains all the files we will create for this tutorial._

### Setup

The only required software to follow this tutorial is `pipenv` which helps to keep the environment consistent. You can find the installation instructions [here](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv).

We will also be using a text editor, you are free to use the one bundled with your operating system, or use your preferred option.

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

The contents of the `Pipfile` should now have changed to include a `[packages]` section, with an entry for Flask. This will also create a new `Pipfile.lock` file which is what is used to ensure collaborators always use the same version of the Flask library (and it's dependencies).

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

You can now open [`http://localhost:5000/`](http://localhost:5000/) in your browser, it will display the hello message.

_The same command can be reused to start the application again after making changes._

To stop the running app, return to the shell and press `ctrl+c`.

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

Notice that the only allowed method for this endpoint is `GET`. This is partly by convention, but also because we will be adding a handler for different methods later in the tutorial. In a similar vein, the route for this endpoint is prefixed with `/api` to makes it clear that it is indeed an api.

Like before, we can use the browser to see our endpoint in action at `http://localhost:5000/api/word`. (Remember to restart the application to make the changes take effect)

We will also add an endpoint to return single words from the list using their index:

```python
@app.route("/api/word/<int:index>", methods=["GET"])
def get_word(index):
    return words[index % len(words)]
```

For this endpoint, the path contains special syntax which reads the integer index before running our handler.

With these two endpoints, we have the established the basic pattern for how resources (in our case words) are made accessible using the REST pattern.
