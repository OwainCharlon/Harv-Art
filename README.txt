Installer flask: pip install flask
->version installées:
-flask 1.1.1
Jinja 2.10.1

Installer Sql alchemy: pip install flask-sqlalchemy
->version installée 2.4.1

Installer mySQLClient: pip install mysqlclient
->version installée 1.4.6

Lancer une appliccation flask: python "nomDeLapp.py"


Mettre ses templates dans un dossier nommé templates (respecter l'architecture du framework).
Mettre ses fichiers static (scripts js, feuille de style css, images...) dans un fichier static.
Appeller un fichier dans le dossier static :
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}>