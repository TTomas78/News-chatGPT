# News GPT

How to run:

Install virtualenv

```bash
  pip install virtualenv
```

Create one 

```bash
  virtualenv venv
```

Get into it

(Windows)
```bash
./venv/Script/Activate
```

(Linux)
```bash
./venv/bin/activate
```


Install dependencies

```bash
pip install -m requirements.txt
```

Create a config.ini with the following information on your root directory

```bash
[DEFAULT]
API-KEY = {fill the value with your API Key}
NEWS-NUMBER = 3 {fill with an integer number, will be used as a limit number of news to resume}
```

Run the app

```bash
uvicorn main:app --reload 
```

To use the google chrome extension

There's a folder file called "extension". Import the folder as a google chrome extension
