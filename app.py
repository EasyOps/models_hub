from flask import Flask
from flask_cors import CORS
from flask_restx import Api


from utils import Cfg, load_module
import logging


config = Cfg.load_config_from_file("config.toml")


logging.addLevelName(config['Logging']['level'])


app = Flask(__name__)
CORS(app)
app.config["ERROR_404_HELP"] = False
app.config["VALIDATOR"] = load_module(config['App']['validator'])
