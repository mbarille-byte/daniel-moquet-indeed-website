#!/usr/bin/env python3
"""Met à jour les données affichées par index.html (onglets Suivi et Résultats).

Usage : python3 maj_site.py demandes.csv resultats.csv
  demandes.csv  = export CSV de l'onglet « Demandes » du Sheet
  resultats.csv = export CSV de l'onglet « Résultats » du Sheet
Les colonnes E-mail et Commentaire ne sont jamais copiées dans la page.
"""
import csv, json, re, sys, datetime, pathlib

def lire(p):
    with open(p, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def main(dem_path, res_path):
    page = pathlib.Path(__file__).with_name('index.html')
    html = page.read_text(encoding='utf-8')

    reqs = []
    for r in lire(dem_path):
        if not (r.get('id') or '').strip():
            continue
        d = (r.get('Date demande') or '').strip()
        ts = int(datetime.datetime.strptime(d, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc).timestamp() * 1000) if d else 0
        reqs.append({
            'franchise': r['Franchisé'].strip(), 'franchiseKey': None, 'url': r['Lien annonce'].strip(),
            'title': r['Poste'].strip(), 'location': r['Lieu'].strip(), 'pack': r['Formule'].strip(),
            'price': float(r['Prix €'] or 0), 'wantedStart': r['Démarrage souhaité'].strip(),
            'status': (r['Statut'] or 'nouveau').strip(), 'createdAt': ts,
        })
    for r in reqs:
        r['price'] = int(r['price']) if r['price'] == int(r['price']) else r['price']
        del r['franchiseKey']

    rows = []
    for r in lire(res_path):
        if not (r.get('ID annonce') or '').strip():
            continue
        rows.append([r['ID annonce'].strip(), r['Poste'].strip(), r['Lieu'].strip(), r['Début'].strip(), r['Fin'].strip(),
                     int(float(r['Clics'] or 0)), int(float(r['Candidatures commencées'] or 0)),
                     float((r['Budget utilisé €'] or '0').replace(',', '.'))])
    if not rows:
        sys.exit('Résultats vides : rien écrit.')

    data = {'reqs': reqs, 'rows': rows,
            'meta': {'dataThrough': max(x[4] for x in rows),
                     'updatedAt': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
            'cfg': {'budget': 3000, 'quota': 20}}
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    m = re.search(r'else\{const D=(\{.*?\});apply\(D\)\}', html, re.S)
    if not m:
        sys.exit("Bloc de données introuvable dans index.html : rien écrit.")
    html = html[:m.start(1)] + blob + html[m.end(1):]
    page.write_text(html, encoding='utf-8')
    print(f'{len(reqs)} demandes, {len(rows)} lignes de résultats, données jusqu\'au {data["meta"]["dataThrough"]}.')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
