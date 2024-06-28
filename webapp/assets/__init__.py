import os

assets = "assets"
folder = os.path.dirname(os.path.abspath(__file__))
app.static_folder=os.path.join(folder, assets)
print(f"assets: {app.static_folder}")