#
# Author: Rohtash Lakra
# References:
#  - https://blog.mcpolemic.com/2016/01/18/adding-request-ids-to-flask.html
import logutils
import log
import logging
from flask import Flask

# set up a small Flask app to show it in action.
logger = logging.getLogger(__name__)
app = Flask(__name__)
app.app_context()


# route
# curl http://127.0.0.1:5000/
# curl --header 'X-Request-Id:cc4edc3c-ba0d-40c9-b76d-563f8fe08bd9' http://127.0.0.1:5000/
@app.route("/")
def hello():
    logger.info("Sending our hello")
    return "Hello World!"


if __name__ == "__main__":
    app.run()
