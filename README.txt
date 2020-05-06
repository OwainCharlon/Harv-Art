Installer flask: pip install flask
- flask 1.1.1
- jinja2 2.10.1
- flask-sqlalchemy 2.4.1
- mysqlclient 1.4.6

Mettre ses templates dans un dossier nommé templates (respecter l'architecture du framework).
Mettre ses fichiers static (scripts js, feuille de style css, images...) dans un fichier static.
Appeller un fichier dans le dossier static :
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}>
