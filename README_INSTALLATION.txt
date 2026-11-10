MAIRIE DE DIAGANE BARKA — VERSION AVEC MENUS ET GESTION

1) Ouvrir le dossier du projet dans VS Code.
2) Ouvrir un terminal dans le dossier qui contient manage.py.
3) Activer votre environnement virtuel Windows :
   venv\Scripts\activate
   (si le dossier venv n'existe pas : python -m venv venv)
4) Installer les dépendances :
   pip install -r requirements.txt
5) Créer les tables de la base de données :
   python manage.py makemigrations dashboard
   python manage.py migrate
6) Créer le compte administrateur Django :
   python manage.py createsuperuser
7) Démarrer le serveur :
   python manage.py runserver
8) Ouvrir http://127.0.0.1:8000/

FONCTIONNALITÉS INCLUSES
- Menus reliés à leurs pages : tableau de bord, citoyens, état civil, demandes, finances, rapports et paramètres.
- Citoyens : ajout, modification, suppression avec confirmation et recherche.
- État civil : saisie, modification, suppression et filtre des actes de naissance, mariage et décès.
- Demandes : création, changement de statut, recherche, filtre et export PDF de la fiche de suivi.
- Finances : saisie des recettes/dépenses et calcul des totaux.
- Rapports : indicateurs calculés à partir de la base de données.

IMPORTANT
- Le PDF généré est une fiche de suivi de demande. Ce n'est PAS un acte d'état civil officiel ni un certificat officiel.
- Le projet est une base fonctionnelle de développement. Avant de l'utiliser avec les données réelles des citoyens, il faut configurer l'authentification, les rôles et permissions, les sauvegardes, HTTPS et les règles locales de conservation/protection des données.
- Ne partagez pas le fichier db.sqlite3 s'il contient des données personnelles réelles.
