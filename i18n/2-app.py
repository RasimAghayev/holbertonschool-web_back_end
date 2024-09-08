#!/usr/bin/env python3
"""Basic Babel setup for the Flask application."""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """Configuration for Babel, including supported languages and defaults."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BABEL_DEFAULT_LOCALE = 'en'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match for the client's preferred language.

    Returns:
        str: The best match for the language from the supported options.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def hello_world():
    """Render the initial template with a greeting message.

    Returns:
        str: Rendered HTML for the index page.
    """
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
