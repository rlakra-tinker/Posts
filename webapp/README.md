# webapp

---

The ```webapp``` represents an external webapp service.

## Folder Structure Conventions

---

```
    /
    ├── modules                     # The modules
    ├── webapps                     # The webapp external service
    |    ├── assets                 # an assets of external service
    |    |    ├── css
    |    |    ├── js
    |    |    ├── templates
    |    ├── views                 # The webapp views
    |    └── README.md
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

```source``` is linux/Mac OS command and doesn't work in Windows.

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
http://127.0.0.1:5000/ews-posts
http://localhost:8080/ews-posts
```


# Author

---

- Rohtash Lakra
