#!/usr/bin/env python
# encoding: utf-8

from app import create_app
from app import scheduler

app = create_app()

scheduler.start()
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    # app.run(use_reloader=False)
