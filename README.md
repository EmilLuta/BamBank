# BamBank

Basic Flask app with Bootstrap, webassets, WTForms aimed for BamBank Software Inc.


### What's this? ###

Nothing more than a simple application which allows authentication and money transfer between users.

### Getting into the deal ###
* cd to a comfortable location
* git clone git@github.com:EmilLuta/BamBank.git
* sudo npm install -g less
* sudo ln -s /usr/bin/nodejs /usr/bin/node # in case you get "node: command not found" in bash
* cd Bambank
* virtualenv -p $(which python3) venv
* source venv/bin/activate
* pip install -r requirements.txt
* cp config_example.py config.py
* update the config.py file to suit your needs
* ./manage.py db_create
* ./manage.py runserver
* open [http://localhost:5000/](http://localhost:5000/)


### Confused? You can easily get in touch with me at [virgil.luta@gmail.com](mailto:virgil.luta@gmail.com) ###

If you need any sort of support from running to deploying, feel free to contact me. ;)