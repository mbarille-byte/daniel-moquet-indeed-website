#!/usr/bin/env python3
"""Met à jour data.json, lu par index.html (onglets Suivi et Résultats).

Usage : python3 maj_site.py demandes.csv resultats.csv
Les colonnes E-mail et Commentaire ne sont jamais copiées dans la page.
"""
import csv, json, sys, datetime, pathlib

SKIP = {"e-mail contact", "e-mail", "email", "commentaire", "comment"}

def lire(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def col(row, *names):
    for name in names:
        if name in row and str(row[name]).strip():
            return str(row[name]).strip()
    return ""

def main(dem_path, res_path):
    page = pathlib.Path(__file__).with_name("data.json")
    reqs = []
    for r in lire(dem_path):
        rid = col(r, "ID", "id")
        if not rid:
            continue
        d = col(r, "Date de création", "Date demande")
        ts = int(datetime.datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp() * 1000) if d else 0
        price = float((col(r, "Prix €") or "0").replace(",", "."))
        price = int(price) if price == int(price) else price
        reqs.append({
            "id": rid,
            "franchise": col(r, "Franchisé"),
            "url": col(r, "Lien annonce"),
            "title": col(r, "Poste"),
            "location": col(r, "Lieu"),
            "pack": col(r, "Formule"),
            "price": price,
            "wantedStart": col(r, "Démarrage souhaité"),
            "status": col(r, "Statut") or "nouveau",
            "createdAt": ts,
        })
        for key in list(r):
            if key and key.strip().lower() in SKIP and str(r[key]).strip():
                pass
    rows = []
    for r in lire(res_path):
        job = col(r, "ID annonce")
        if not job:
            continue
        rows.append([
            job, col(r, "Poste"), col(r, "Lieu"), col(r, "Début"), col(r, "Fin"),
            int(float(col(r, "Clics") or 0)),
            int(float(col(r, "Candidatures commencées") or 0)),
            float((col(r, "Budget utilisé €") or "0").replace(",", ".")),
        ])
    if not rows:
        sys.exit("Résultats vides : rien écrit.")
    blob_check = json.dumps(reqs, ensure_ascii=False)
    if "@" in blob_check:
        sys.exit("Une adresse e-mail est présente : rien écrit.")
    data = {
        "reqs": reqs,
        "rows": rows,
        "meta": {
            "dataThrough": max(x[4] for x in rows),
            "updatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "cfg": {"budget": 3000, "quota": 20},
    }
    page.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(reqs)} demandes, {len(rows)} lignes de résultats, données jusqu'au {data['meta']['dataThrough']}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage : python3 maj_site.py demandes.csv resultats.csv")
    main(sys.argv[1], sys.argv[2])
