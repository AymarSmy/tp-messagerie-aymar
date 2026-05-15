# TP Messagerie – Backend FastAPI

Ce projet est une petite API de messagerie.  
Le but est de comprendre comment créer une API REST simple avec FastAPI et une base SQLite.

## Objectif du projet

L’application permet :
- de créer des utilisateurs,
- d’envoyer des messages,
- de consulter sa boîte de réception,
- de consulter les messages envoyés,
- de lire un message,
- de marquer un message comme lu.

J’ai aussi ajouté deux améliorations :
- filtrer les messages non lus,
- rechercher un message par mot-clé dans le sujet.

## Technologies utilisées

- FastAPI  
- SQLModel  
- SQLite  
- Pydantic  
- CORS pour la communication avec le frontend  

## Structure du projet

Le projet est organisé en plusieurs fichiers :
- `main.py` : routes de l’API
- `models.py` : modèles de la base de données
- `schemas.py` : schémas de validation
- `database.py` : création de la base SQLite
- `frontend/` : interface HTML/JS

## Fonctionnement général

Le backend expose plusieurs routes pour gérer les utilisateurs et les messages.  
Le frontend envoie des requêtes HTTP pour afficher la messagerie.

## Résultat

On obtient une messagerie simple mais fonctionnelle, qui permet de comprendre :
- la structure d’une API REST,
- la gestion d’une base de données,
- la communication frontend/backend.

