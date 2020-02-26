from flask_ngrok import run_with_ngrok
from src.app import app

__author__ = 'Franke'

if __name__ == '__main__':
  run_with_ngrok(app)
	app.run()
