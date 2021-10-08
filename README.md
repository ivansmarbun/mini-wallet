# Mini Wallet
## Install Virtual ENV
```
# Install Virtual Environment
~$ pip install virtualenv virtualenvwrapper                 # Install virtualenv
~$ source /usr/local/bin/virtualenvwrapper.sh               # For WSL (Windows user) source ~/.local/bin/virtualenvwrapper.sh
~$ mkvirtualenv mini-wallet -p python3.7                    # Create virtual environment with python3.7
~$ workon mini-wallet                                       # Ready to work on environment
```

## Install all necessary packages
```
pip install -r requirements.txt
```

## Do Migration
```
python manage.py migrate
```

## Run Project
```
python manage.py runserver
```

The program will be run on default port, which is 8000