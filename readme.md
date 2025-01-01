# **Projet Web - Amélioration d'une Application Django**

## **À propos de ce projet**
Ce projet consiste à améliorer une application Django existante en ajoutant de nouvelles fonctionnalités tout en corrigeant des problèmes signalés. L’objectif est de garantir une application stable, fonctionnelle et répondant aux besoins du client.

### Fonctionnalités clés :
- **Réinitialisation de mot de passe via email** : Ajout d'une fonctionnalité permettant aux utilisateurs de récupérer leur mot de passe de manière sécurisée.
- **Gestion des favoris** : Possibilité de supprimer un produit de la liste de favoris directement via l'interface utilisateur.

Ce projet inclut également des tests unitaires et fonctionnels pour valider la robustesse des nouvelles fonctionnalités.

---

## **Fonctionnalités principales**

### 1. Réinitialisation du mot de passe par email
- Envoi sécurisé d’un lien de réinitialisation via un serveur SMTP.
- **Configuration ajoutée dans `settings.py`** :
  - Utilisation de Gmail pour garantir un envoi sécurisé.
- **Intégration de la vue dans `urls.py`** :
  - Utilisation de `PasswordResetView` .

### 2. Suppression de favoris
- Ajout d’une vue dans `views.py` pour gérer les suppressions de manière sécurisée.
- Bouton interactif ajouté dans le template `favorites.html` pour rendre l’action intuitive.

---

## **Installation**

### Prérequis :
- Python 3.11 ou version compatible.
- Django 4.x ou version supérieure.
- Bibliothèques listées dans `requirements.txt`.

### Étapes d'installation :
1. Clonez ce dépôt :
   bash
   git clone https://github.com/khaledOPC/Projet11.git


### Initialiser le projet.

Naviguez dans le dossier du projet :



cd Projet11
Installer les dépendances requises :
pip install -r requirements.txt

Appliquez les migrations de la base de données :
python manage.py migrate

Lancez le serveur de développement :
python manage.py runserver


# Utiliser Coverage
Installer coverage:

- pip install coverage
- Lancez les tests avec Coverage :
- coverage run -m pytest
- Affichez le rapport de couverture :
- coverage report