---
name: maj-site
description: Met à jour les onglets Suivi et Résultats du site Daniel Moquet (sponsorisation franchisés) à partir du Google Sheet « Daniel Moquet – Suivi sponsorisation (données site) ». Use when someone says « mets à jour le site », « maj du site », « rafraîchis le suivi ».
---

# Mise à jour du site depuis le Sheet

La page `index.html` charge `data.json`. Le script `maj_site.py` remplace ce fichier. Le formulaire n'est pas concerné : il envoie déjà la demande au Google Form.

Une publication automatique a lieu chaque matin après la mise à jour du classeur. Cette procédure sert si la personne veut publier tout de suite.

## Étapes

1. **Lire le Sheet** « Daniel Moquet – Suivi sponsorisation (données site) ». Lecture seule. Ne pas réécrire le classeur.
2. **Exporter deux onglets en CSV**, hors du dépôt : `Demandes` → `demandes.csv`, `Résultats` → `resultats.csv`. Garder les en-têtes.
3. **Lancer** depuis le dossier du dépôt :
   ```bash
   python3 maj_site.py <chemin>/demandes.csv <chemin>/resultats.csv
   ```
4. **Contrôler** : les nombres affichés correspondent aux lignes des deux onglets. Ouvrir `index.html` via un petit serveur local (le fichier charge `data.json`) et regarder Suivi et Résultats.
5. **Publier** : demander l'accord de la personne, puis commit et push de `data.json` sur `main`. GitHub Pages met la page à jour en une minute environ.

## Garde-fous

- Ne jamais copier les colonnes E-mail et Commentaire dans `data.json`.
- Ne pas modifier le Sheet, le Google Form, ni la ligne `const FORM=` de `index.html`.
- L'onglet Résultats est alimenté chaque matin depuis le Data Platform. Si la personne veut des chiffres plus récents, cet onglet est mis à jour d'abord, puis ces étapes.
