import pandas as pd

df_sites = pd.read_csv("data/sites.csv")
df_materiel = pd.read_csv("data/materiel.csv")
df_associations = pd.read_csv("data/associations.csv")
df_reservations = pd.read_csv("data/reservations.csv")

df_reservations["date_debut"] = pd.to_datetime(df_reservations["date_debut"])
df_reservations["date_fin_prevue"] = pd.to_datetime(df_reservations["date_fin_prevue"])
df_reservations["date_retour_reelle"] = pd.to_datetime(df_reservations["date_retour_reelle"])


print("dimensions du matériel :")
print(df_materiel.shape)

print("informations du matériel :")
df_materiel.info()

print("valeurs manquantes du matériel :")
print(df_materiel.isnull().sum())


print("dimensions des réservations :")
print(df_reservations.shape)

print("informations des réservations :")
df_reservations.info()

print("valeurs manquantes des réservations :")
print(df_reservations.isnull().sum())

# On remplace les virgules par des points pour convertir les prix en nombres.
df_materiel["valeur_achat"] = pd.to_numeric(
    df_materiel["valeur_achat"].str.replace(",", ".", regex=False),
    errors="coerce"
)

materiel_trie = df_materiel.sort_values("valeur_achat", ascending=False)

print("Les 10 matériels les plus chers :")
print(materiel_trie[
    ["reference", "designation", "categorie", "valeur_achat"]
].head(10))
print("Nombre de matériels par catégorie :")
print(df_materiel["categorie"].value_counts())

reservations_par_site = df_reservations.groupby("code_site").agg(
    nombre_reservations=("id_reservation", "size"),
    quantite_totale=("quantite", "sum")
)

reservations_par_site = reservations_par_site.sort_values(
    "nombre_reservations", ascending=False
)

print("Nombre de réservations et quantité totale par site :")
print(reservations_par_site)

materiel_sans_doublons = df_materiel.drop_duplicates()

df_complet = df_reservations.merge(
    materiel_sans_doublons,
    on="id_materiel",
    how="left"
)

df_complet = df_complet.merge(
    df_associations,
    on="id_association",
    how="left"
)

print("Nombre de lignes après fusion :", len(df_complet))
print(
    "Nombre de lignes sans matériel correspondant :",
    df_complet["designation"].isnull().sum()
)