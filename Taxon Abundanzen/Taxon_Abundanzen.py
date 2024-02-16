import numpy as np
import matplotlib.pyplot as plt
import biom
from biom.table import Table

#Parameter
taxa = 10
mu = 0
sigma = 0.5
proben = 5
beobachtungen = 1000

# Aufgabe 1: Simulation der Abundanzen für jede Probe
def simulation_taxon_abundanzen():                          # Funktiomn zur Simulation der Abundanzen über eine Gruppe an Taxa
    abundanzen = np.zeros((proben, taxa, beobachtungen))    # Erstellen 3D-Matrix aus Nullen
    for i in range(proben):                                 # Füllen der Reihen mit Zufallszahlen
        for j in range(taxa):                               # Füllen der Spalten mit Zufallszahlenix
            abundanzen[i, j] = np.random.lognormal(mean=mu, sigma=sigma, size=beobachtungen)  # Erzeugen von Zufallszahlen einer Lognormalverteilung unter Beachtung der Parameter
    return abundanzen                                      # Ausgabe einer Matrix 3D-Matrix mit Zufallszahlen

# Aufgabe 2: Balkendiagramme
def mittelwert_berechnen():                                 # Funktiomn zur Berechnung des Mittelwerts der Abundanz eines Taxons über alle Proben
    arrays={}                                               # Initialisieren eines leeren arrays
    for k in range (taxa):                                  # Mitterlwert der Abundanz pro Taxon berechnen
        mittelwert_taxon=[]                                 # Erstellen einer leeren Liste
        for l in range (proben):                            # Mitterlwert der Abundanz pro Taxon über alle Proben
            mittelwert_taxon.append((simulation_taxon_abundanzen())[l][k]) # Anhängen der Abundanz für des aktuelle Taxon und die aktuelle Probe
        arrays[k]=np.mean(mittelwert_taxon)                 # Berechnung des Mittelwerts aus der Liste der  Abundanzen für das jeweilige Taxon
    return arrays                                           # gebe einen Array mit den (Anzahl Taxa) Mittelwerten zurück

def fehler_berechnen():
    fehler_arrays={}
    for p in range (taxa):
        fehler_taxon=[]
        for r in range (proben):
            fehler_taxon.append(np.std((simulation_taxon_abundanzen())[r][p]))# Berechnung Standardabweichung der Abundanzen
        fehler_arrays[p]=np.mean(fehler_taxon)
    return fehler_arrays

def diagramm_erstellen(e,f): # e= Anzahl Subplots je Reihe, f= Anzahl Subplots je Spalte
    x = []
    for i in range(1, taxa+1):                         # Beschirftung der x-Achse erstellen
        x.append('t{}'.format(i))
    fig,subplots = plt.subplots(e, f, figsize=(25, 25)) # Erstellen eines 5x5 Gitters

    r=1                                                 # Zähler für Simulationen
    for z in range(5):                                  # Füllen der Reihen mit Subplots
        for q in range(5):                              # Füllen der Spalten mit Subplots
            p=mittelwert_berechnen()                    # Mittelwerte der Abundanzen
            y=fehler_berechnen()                        # Berechnung der Fehlerbalken
            subplots[z, q].set_title('Simulation {}'.format(r)) # Festlegung der Titel für die einzelnen Balkendiagramme / Simulationen
            subplots[z,q].bar(x,p.values(), color='darkblue', width=0.8,yerr=list(y.values()), ecolor='red', capsize=10)
            r+=1                                        # für Benennung des nächsten Diagramms

    plt.tight_layout()                                  #Automatisch Anpassung des Layouts
    plt.savefig( '/home/amma/Downloads/Taxon_Abundanzen.png' ) #Speichern der Diagramme
#    plt.show()




observ_ids = ['o%d' % i for i in range(1,beobachtungen+1)] # Erstellen eindeutiger Beobachtungs-ID
data = simulation_taxon_abundanzen().reshape((proben * taxa, beobachtungen)) # Umwandeln der Daten  in BIOM-Tabelle
#samples_ids = ['s%d' % i for i in range(1,(proben*taxa)+1)]  # Erstellen eindeutiger Proben-ID
samples_ids = []
for sample_num in range(1, proben + 1): # Erstellen der Beschriftung SampleX_TaxonX
    for taxon_num in range(1, taxa + 1):
        samples_ids.append('sample{}_Taxon{}'.format(sample_num, taxon_num))
table = Table(data, samples_ids, observ_ids) # BIOM-Datei speichern
#print(table)                                                               #Test
with biom.util.biom_open('/home/amma/Downloads/simulated_abundances.biom', 'w') as doc: # Öffnen einer BIOM-Datei im Schreibmodus
    table.to_hdf5(doc, "simulated_abundances") #Tabelle wird in die geöffnete Datei geschrieben mit dem Namen unter dem sie in der Datei gespeichert wird






