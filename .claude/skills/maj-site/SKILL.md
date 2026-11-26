---
name: maj-site
description: Met à jour les onglets Suivi et Résultats du site Daniel Moquet (sponsorisation franchisés) à partir du Google Sheet « Daniel Moquet – Sponsorisation franchisés (base du site) ». Use when someone says « mets à jour le site », « maj du site », « rafraîchis le suivi ».
---

# Mise à jour du site depuis le Sheet

Le site est un fichier unique, `index.html`. Les onglets Suivi et Résultats y affichent une photo des données. Le script `maj_site.py` la remplace. Le formulaire n'est pas concerné : il écrit déjà tout seul dans le Sheet.

## Étapes

1. **Lire le Sheet** « Daniel Moquet – Sponsorisation franchisés (base du site) » (le chercher par son nom dans Drive, ou demander l'URL). Lecture seule.
2. **Exporter deux onglets en CSV**, hors du dépôt (dossier temporaire) : `Demandes` → `demandes.csv`, `Résultats` → `resultats.csv`. Garder les en-têtes de la première ligne, tels quels.
3. **Lancer** depuis le dossier du dépôt :
   ```bash
   python3 maj_site.py <chemin>/demandes.csv <chemin>/resultats.csv
   ```
   Le script affiche le nombre de demandes, de lignes de résultats et la date des données.
4. **Contrôler** : ces nombres doivent correspondre aux lignes des deux onglets. Ouvrir `index.html` dans le navigateur (`open index.html`) et regarder les onglets Suivi et Résultats.
5. **Publier** : demander l'accord de la personne, puis commit et push sur `main`. GitHub Pages met la page à jour en une minute environ.

## Garde-fous

- Ne jamais copier les colonnes E-mail et Commentaire dans la page (le script les ignore).
- Ne pas modifier le Sheet, le Google Form, ni la ligne `const FORM=` de `index.html`.
- L'onglet `Résultats` (clics, candidatures, budget par annonce) est alimenté depuis le Data Platform. Si la personne veut des chiffres plus récents, elle met d'abord cet onglet à jour, puis relance ces étapes.
- Si le script s'arrête avec un message, ne rien écrire à la main dans `index.html` : corriger l'export et relancer.
