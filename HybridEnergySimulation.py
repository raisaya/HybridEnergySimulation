# Importation de la bibliothèque NumPy
# Elle sert à faire des calculs numériques et à manipuler des tableaux
import numpy as np

# Importation de matplotlib pour tracer des graphiques
import matplotlib.pyplot as plt


# ============================
# 1) Définition du temps
# ============================

# Création d'un tableau d'heures de 0 à 23 avec un pas de 1 heure
# np.arange(début, fin, pas)
heures = np.arange(0, 24, 1)


# ============================
# 2) Production photovoltaïque (PV)
# ============================

# On modélise la production solaire :
# - 0 la nuit
# - Maximum à midi
# sin(...) crée une courbe en cloche
# np.maximum(0, ...) empêche les valeurs négatives (pas de soleil la nuit)
pv = np.maximum(0, 50 * np.sin((heures - 6) * np.pi / 12))


# ============================
# 3) Production Diesel
# ============================

# np.where(condition, valeur_si_vrai, valeur_si_faux)
# Le diesel fonctionne :
# - avant 6h du matin
# - après 20h le soir
# Puissance fixée à 20 kW quand il fonctionne
diesel = np.where((heures < 6) | (heures > 20), 20, 0)


# ============================
# 4) Charge (consommation)
# ============================

# Consommation totale du réseau
# - Valeur moyenne de 30 kW
# - Variation journalière avec un sinus
charge = 30 + 10 * np.sin((heures - 3) * np.pi / 12)


# ============================
# 5) État de charge de la batterie (SOC)
# ============================

# SOC = State Of Charge
# Batterie qui oscille entre 30% et 90%
# Moyenne à 60%
soc = 60 + 30 * np.sin((heures - 5) * np.pi / 24)


# ============================
# 6) Calcul de la répartition d'énergie
# ============================

# Énergie totale produite (somme PV + Diesel)
total_production = pv.sum() + diesel.sum()

# Calcul des pourcentages de contribution
parts = [
    pv.sum() / total_production * 100,      # Part du PV
    diesel.sum() / total_production * 100,  # Part du diesel
    15                                       # Batterie (valeur supposée)
]


# ============================
# 7) Graphique : Production vs Charge
# ============================

# Création de la figure
plt.figure(figsize=(10, 5))

# Tracé de la production photovoltaïque
plt.plot(heures, pv, label="Production PV", linewidth=2)

# Tracé de la production diesel
plt.plot(heures, diesel, label="Production Diesel", linewidth=2)

# Tracé de la consommation
plt.plot(heures, charge, label="Charge (Demande)", linewidth=2)

# Nom des axes
plt.xlabel("Heure (h)")
plt.ylabel("Puissance (kW)")

# Titre du graphique
plt.title("Production vs Charge - Micro-réseau Off-grid")

# Affichage de la légende
plt.legend()

# Affichage de la grille
plt.grid()

# Affichage du graphique
plt.show()


# ============================
# 8) Graphique : État de charge de la batterie
# ============================

plt.figure(figsize=(10, 5))

# Tracé du SOC
plt.plot(heures, soc, label="SOC Batterie", linewidth=2)

# Noms des axes
plt.xlabel("Heure (h)")
plt.ylabel("SOC (%)")

# Titre
plt.title("État de Charge de la Batterie")

# Limites de l'axe Y (0 à 100 %)
plt.ylim(0, 100)

# Grille
plt.grid()

# Affichage
plt.show()


# ============================
# 9) Graphique : Répartition des sources
# ============================

# Étiquettes du diagramme circulaire
labels = ["PV (%)", "Diesel (%)", "Batterie (%)"]

plt.figure(figsize=(6, 6))

# Diagramme en secteurs (camembert)
# autopct affiche les pourcentages
plt.pie(parts, labels=labels, autopct="%1.1f%%")

# Titre
plt.title("Répartition des Sources d'Énergie")

# Affichage
plt.show()