# Analyse du TP – Backend Messagerie

## 1. En quoi HTTP convient-il bien à cette application ?

HTTP fonctionne très bien pour une messagerie “classique” parce que le modèle requête/réponse correspond exactement aux actions que l’utilisateur fait de manière ponctuelle.  
Chaque action est indépendante et peut être traitée comme une requête simple.

Quelques exemples qui s’adaptent parfaitement à HTTP :

- **Créer un utilisateur** → requête POST, réponse avec l’utilisateur créé.
- **Envoyer un message** → POST /messages, on envoie les données et on reçoit le message créé.
- **Consulter sa boîte de réception** → GET /users/{id}/inbox, le serveur renvoie la liste.
- **Lire un message** → GET /messages/{id}.
- **Marquer un message comme lu** → PATCH /messages/{id}/read.

Dans tous ces cas, l’utilisateur fait une action ponctuelle, le serveur répond, et c’est terminé.  
Le protocole HTTP est donc largement suffisant pour ce type d’interactions.

---

## 2. Quelles limites apparaissent si l’on veut une vraie messagerie “vivante” ?

Dès qu’on veut quelque chose de plus dynamique, HTTP montre ses limites, car il n’est **pas conçu pour pousser des informations vers le client**.

Voici les problèmes qui apparaissent :

### • Comment savoir immédiatement qu’un nouveau message est arrivé ?
Avec HTTP, le client doit **poller** régulièrement (ex : toutes les 5 secondes) pour demander “est-ce qu’il y a du nouveau ?”.  
C’est inefficace, ça surcharge le serveur, et ce n’est pas instantané.

### • Comment mettre à jour automatiquement l’interface sans recharger la page ?
HTTP ne peut pas prévenir le navigateur tout seul.  
Le frontend doit rafraîchir manuellement ou utiliser du polling, ce qui donne une interface moins fluide.

### • Comment notifier en direct qu’un message a été lu ?
Même problème : le serveur ne peut pas envoyer l’information spontanément.  
Le client doit redemander l’état régulièrement.

En résumé :  
**HTTP est parfait pour des actions ponctuelles, mais pas pour du temps réel.**

---

## 3. Quelle solution pourrait-on introduire ensuite ?

La solution naturelle pour ajouter du temps réel est **WebSocket**.

WebSocket permet d’ouvrir une **connexion persistante** entre le client et le serveur.  
Contrairement à HTTP, cette connexion est **bidirectionnelle** :

- le serveur peut envoyer des messages au client **sans que le client demande**  
- le client peut envoyer des infos en continu  
- tout se fait en temps réel, sans polling

Avec WebSocket, on pourrait :

- afficher un nouveau message **instantanément** dès qu’il arrive  
- mettre à jour l’interface en direct  
- notifier en temps réel qu’un message a été lu  
- gérer des statuts “en ligne / hors ligne”  
- faire une vraie messagerie moderne

C’est donc une évolution logique si on veut passer d’une messagerie “statique” à une messagerie “vivante”.

---

# Note sur mes choix techniques

## Choix de modélisation

J’ai séparé les modèles SQLModel (base de données) et les schémas Pydantic (API) pour avoir :

- une base propre et cohérente,
- des schémas adaptés aux entrées (MessageCreate) et aux sorties (MessageRead),
- la possibilité d’ajouter des champs calculés (sender_name, receiver_name),
- une API plus sécurisée (on ne renvoie pas tout ce qu’il y a en base).

J’ai aussi choisi une structure simple :

- **User** : id, username, email  
- **Message** : id, sender_id, receiver_id, subject, body, is_read, sent_at  

C’est suffisant pour une messagerie basique.

---

## Routes disponibles

### Utilisateurs
- `POST /users` → créer un utilisateur  
- `GET /users` → lister les utilisateurs  
- `GET /users/{id}` → récupérer un utilisateur  

### Messages
- `POST /messages` → envoyer un message  
- `GET /users/{id}/inbox` → messages reçus  
- `GET /users/{id}/sent` → messages envoyés  
- `GET /messages/{id}` → lire un message  
- `PATCH /messages/{id}/read` → marquer comme lu  

Toutes les routes renvoient des schémas propres (`UserRead`, `MessageRead`).

---

## Limites de ma solution HTTP

- pas de temps réel : il faut recharger ou poller pour voir les nouveaux messages  
- pas de notifications instantanées  
- pas de statut “en ligne”  
- pas de synchronisation automatique entre plusieurs onglets  
- pas adapté à une messagerie moderne type WhatsApp/Discord  

Pour dépasser ces limites, il faudrait ajouter **WebSocket**.

