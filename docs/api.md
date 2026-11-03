# Contrat de l'API TaskFlow

Format d'une tâche : {"id": 1, "title": "Réviser Git", "priority": "haute", "done": false}
priority ∈ {haute, moyenne, basse}

| Méthode | Route               | Corps                 | Réponse                              |
|---------|---------------------|-----------------------|--------------------------------------|
| GET     | /api/tasks?status=X | -                     | 200 + liste (X = all, active, done)  |
| POST    | /api/tasks          | {"title", "priority"} | 201 + tâche, 422 si titre vide       |
| PATCH   | /api/tasks/{id}     | {"done": true/false}  | 200 + tâche, 404 si inconnue         |
| DELETE  | /api/tasks/{id}     | -                     | 204, 404 si inconnue                 |