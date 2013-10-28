
The member database of Pfadikorps Glockenhof

Start hacking::

	For mac-users you'll need at least: 
	http://hackercodex.com/guide/python-virtualenv-on-mac-osx-mountain-lion-10.8/
	http://nodejs.org/
	https://npmjs.org/
	https://github.com/bower/bower

    git clone git@github.com:gloggi/etat.git
    cd etat
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
	for mac-users: pip install pil	
    bower update
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py runserver