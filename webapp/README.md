# webapp

---

The ```webapp``` represents an external webapp service.

## Folder Structure Conventions

---

```
    /
    ├── modules                     # The name of the module
    ├── webapp                      # The webapp external module/service
    |    ├── api                    # The API of the client
    |    ├── blueprints             # The routes of the views
    |    ├── static                 # an assets of external service
    |    |    ├── css               # css files
    |    |    ├── images            # image files
    |    |    ├── js                # JavaScript files
    |    ├── templates              # The templates and html files
    |    |    ├── views             # The HTML views/pages
    |    └── README.md              # The README file of webapp module
    └── README.md
```


# Building Application

---

## Create Virtual Env
```shell
python3 -m pip install virtualenv
python3 -m venv venv
```

## Activate ```venv```

```source``` is Linux/MAC OS command and doesn't work in Windows.

- Windows

    ```shell
    venv\Scripts\activate
    ```

- Mac OS/Linux

    ```shell
    source venv/bin/activate
  
  OR
  
    . ./venv/bin/activate
    ```

The parenthesized (venv) in front of the prompt indicates that you’ve successfully activated the virtual environment.

## Upgrade ```pip``` release

```shell
pip install --upgrade pip
```


## Install Requirements

**Note**: - You can ignore ```Install Packages``` steps if you've successfully run this section.

```shell
python3 -m pip install -r requirements.txt
```

## Install Packages

- Install Flask

**Note**: - Only if you didn't install the 'requirements.txt' file.

```shell
python3 -m pip install Flask
```


## Save Requirements (Dependencies)
```shell
pip freeze > requirements.txt
```


## Configuration Setup

Set local configuration file.

```shell
cp default.env .env
```

Now, update the default local configurations as follows:

```text
APP_HOST = 0.0.0.0
APP_PORT = 8080
```


## Run Flask Application

```shell
flask --app wsgi run

http://127.0.0.1:5000/ews-posts

OR

python3 wsgi.py

OR

python -m flask --app wsgi run --port 8080 --debug
```

**Note**:- You can stop the development server by pressing ```Ctrl+C``` in your terminal.


## Access Application
```shell
http://127.0.0.1:5000/posts-ews
http://localhost:8080/posts-ews
```


# Author

---

- Rohtash Lakra
