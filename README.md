# Posts

---

The ```Posts``` repository contains the Posts python project.


## Folder Structure Conventions

---

```
    /
    ├── modules                     # The modules
    ├── Posts                       # The Posts Service
    |    ├── posts-iws              # The IWS Service
    |    ├── webapp                 # The WebApp Service
    |    └── README.md
    └── README.md
```


# Building Application

---


## Create Virtual Env
```shell
python -m pip install virtualenv
python -m venv venv

OR

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


## Install Requirements

```shell
python -m pip install -r requirements.txt

OR

python3 -m pip install -r requirements.txt
```

## Save Requirements (Dependencies)
```shell
pip freeze > requirements.txt
```



# Author

---

- Rohtash Lakra
