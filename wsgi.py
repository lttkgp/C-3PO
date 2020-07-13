"""WSGI Server file."""
from c3po.manage import app, sched

if __name__ == "__main__":
    app.run()
    sched.start()
