import csv
from collections import Counter

CHEMIN_SITES = "data/sites.csv"
CHEMIN_MATERIEL = "data/materiel.csv"
CHEMIN_ASSOCIATIONS = "data/associations.csv"
CHEMIN_RESERVATIONS = "data/reservations.csv"


def lire_csv(chemin):
    with open(chemin, encoding="utf-8", newline="") as fichier:
        lecteur = csv.DictReader(fichier)
        return list(lecteur)


def compter_par(lignes, colonne):
    compteur = Counter()

    for ligne in lignes:
        valeur = ligne[colonne]
        compteur[valeur] += 1

    return dict(compteur)


def total_par(lignes, colonne_groupe, colonne_valeur):
    totaux = {}

    for ligne in lignes:
        groupe = ligne[colonne_groupe]
        valeur = int(ligne[colonne_valeur])

        if groupe in totaux:
            totaux[groupe] += valeur
        else:
            totaux[groupe] = valeur

    return totaux


class Site:
    def __init__(self, code_site, nom, commune, annee_ouverture, surface_m2):
        self.code_site = code_site
        self.nom = nom
        self.commune = commune
        self.annee_ouverture = int(annee_ouverture)
        self.surface_m2 = int(surface_m2)

    def anciennete(self, annee_reference):
        return annee_reference - self.annee_ouverture

    def __str__(self):
        return f"{self.code_site}, {self.nom}, {self.commune}, {self.surface_m2} m²"


def reservations_en_cours(reservations):
    en_cours = []

    for reservation in reservations:
        if reservation["date_retour_reelle"] == "":
            en_cours.append(reservation)

    return en_cours


def valeur_de_tri(element):
    return element[1]


def main():
    sites = lire_csv(CHEMIN_SITES)
    materiel = lire_csv(CHEMIN_MATERIEL)
    associations = lire_csv(CHEMIN_ASSOCIATIONS)
    reservations = lire_csv(CHEMIN_RESERVATIONS)

    print("Nombre de sites :", len(sites))
    print("Nombre de matériels :", len(materiel))
    print("Nombre d'associations :", len(associations))
    print("Nombre de réservations :", len(reservations))

    print("\nSites et ancienneté :")
    for ligne in sites:
        site = Site(
            ligne["code_site"],
            ligne["nom"],
            ligne["commune"],
            ligne["annee_ouverture"],
            ligne["surface_m2"]
        )
        print(site)
        print("Ancienneté en 2026 :", site.anciennete(2026), "ans")

    reservations_par_site = compter_par(reservations, "code_site")
    reservations_triees = sorted(
        reservations_par_site.items(),
        key=valeur_de_tri,
        reverse=True
    )

    print("\nNombre de réservations par site :")
    for code_site, nombre in reservations_triees:
        print(code_site, ":", nombre)

    quantites_par_site = total_par(reservations, "code_site", "quantite")
    quantites_triees = sorted(
        quantites_par_site.items(),
        key=valeur_de_tri,
        reverse=True
    )

    print("\nQuantité totale réservée par site :")
    for code_site, quantite in quantites_triees:
        print(code_site, ":", quantite)

    materiel_par_etat = compter_par(materiel, "etat")

    print("\nNombre de matériels par état :")
    for etat, nombre in materiel_par_etat.items():
        print(etat, ":", nombre)

    categories = compter_par(materiel, "categorie")
    print("\nNombre de catégories distinctes :", len(categories))

    en_cours = reservations_en_cours(reservations)
    print("Nombre de réservations en cours :", len(en_cours))


if __name__ == "__main__":
    main()