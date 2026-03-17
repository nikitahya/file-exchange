# File-Exchange (FEX)

File-Exchange is a private self-hosted service for fast file and text exchange between devices and trusted 
people.

## Why I built it

I wanted a simple way to exchange files and text between my own devices and with my girlfriend without 
using messengers or third-party cloud services.

The core use case is very practical:  
I upload a file or a text in my private dashboard, publish it to a private showcase link, and the other 
person can open the same stable link and download or copy the content.

It also supports a reverse flow:  
I can switch the showcase into **request mode**, and the other person can send me a response with text 
and/or a file. That response appears in my dashboard as an incoming post.

## Features

- owner-only login
- private dashboard
- create posts with text and file attachments
- publish a post to a private showcase
- stable private showcase link
- request mode for receiving responses
- incoming/outgoing post flow
- file download from dashboard and showcase
- permanent deletion of posts and files
- free disk space indicator

## Tech stack

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- Jinja2
- Werkzeug
- Gunicorn

## Project structure

```text
file-exchange/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── showcase.py
│   ├── storage.py
│   ├── utils.py
│   ├── views.py
│   └── templates/
├── data/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py

```
## Local setup

1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Create .env
Example:
SECRET_KEY=change
DATABASE_URL=sqlite:///fex.db
SHOWCASE_TOKEN=change
MAX_CONTENT_LENGTH=1073741824
OWNER_USERNAME=change
OWNER_PASSWORD=change

4. Run the app
python run.app

5. Then open:
http://127.0.0.1:500/login
http://127.0.0.1:500/showcase/<your_token>

## Status

MVP is implemented and working locally.
Next steps:
1. improve UI/UX
2. add styling
3. deploy to production
4. configure subdomain and HTTPS
