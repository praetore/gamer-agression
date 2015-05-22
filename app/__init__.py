from flask import Flask
from app.config import default

__author__ = 'Darryl'

app = Flask(__name__)
app.config.from_object(default)

if __name__ == '__main__':
    app.run(debug=True)