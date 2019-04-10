#Initialisation for the catalog package.

from flask import Flask

# Initialise the Flask app object
app = Flask(__name__)

import catalog.routes
import catalog.auth