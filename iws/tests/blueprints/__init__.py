#
# Author: Rohtash Lakra
#
from webapp.app import WebApp

# setup webapp for testing
webApp = WebApp()
# create an app
app = webApp.create_app(test_mode=True)
app.app_context = app.app_context()
app.app_context.push()



