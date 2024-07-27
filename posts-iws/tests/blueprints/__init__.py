#
# Author: Rohtash Lakra
#
from webapp import create_app

# setup webapp for testing
app = create_app(testMode=True)
app.app_context = app.app_context()
app.app_context.push()

