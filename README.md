# Project Questionnair 

this is python project for creating questions that potentionaly bussiness owners could use to ask their customers some information. As i do not care if this is used in other projects or not it will be in open source MIT licence so it is free to use.

use cases: 
- massage therapist, when his clients avait for session, they can register and answer all questions that therapist might have forgotten otherwise. for example where they don't like to be touched, previous injures. or more positive things like what sort of scents do they enjoy so massage can have maximum relaxation effect. These questions are most likley forgoten, or seem irrelavant but they could mean a lot to patient/clients 

- math teacher, sends the questionner to kids to figure out if the children even enyoj math, like this kids can be honest without peer pressure, or fear from 1 on 1 interaction with the teacher. As long as questions seem warm and not in attacking format this should be a good idea

# How to install the application:

You need an inviroment with `python3`, `pip` and all modules from `requirements.txt`, this project used gnu/linux ubuntu distribution for development and has not tested it in other ones.
- setup the enviroment
take a look at config folder
.env file needs to be edited properly. the json file is the main file of the app in sence of questions since they are stored there. there is an example there of how it should look like. This can be edited in app as well. but the app will not start if json file (in this example `questionnaire.json`) is not well formated. 
- `.env` file variables
``` yml
ADMIN_USER_USERNAME = '' # still not used so no need
ADMIN_USER_PASSWORD = '' # still not used so no need
SECRET_KEY = 'some very secret key'
QUESTIONNAIRE_PATH = 'absolute path to above mentioned json'
```
- database should be initialized as well before starting the application

- starting the **Questionnair** application for the first time 
```bash
cd src/
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
python3
```
`>>>`
``` python
from app import db
db.create_all()
```
`exit()`
```bash
python3 app.py 
```
- usually how it should be started
```bash
cd src/
source env/bin/activate
python3
```

at the moment first person to login will also become the admin, so be aware of that. (this was not planed, and as it seemed to me only one admin was needed i left it so. )


