"""WSGI Server file."""
from dotenv import find_dotenv, load_dotenv

from c3po.manage import app

load_dotenv(find_dotenv())

if __name__ == "__main__":
    app.run()
