
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


Required stuff:
 * http://python.org
 * http://pip-installer.org
 * http://nodejs.org
 * https://npmjs.org
 * https://github.com/bower/bower

If you're on OSX, also check those:
 * https://developer.apple.com/xcode/
 * http://hackercodex.com/guide/python-virtualenv-on-mac-osx-mountain-lion-10.8/