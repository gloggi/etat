
The member database of Pfadikorps Glockenhof

Start hacking::

    git clone git@github.com:gloggi/etat.git
    cd etat
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    bower update
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py runserver