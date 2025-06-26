from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello() -> str:
    """Return a greeting message.

    Returns:
        str: A greeting message.
    """
    return "Hello, World!"
