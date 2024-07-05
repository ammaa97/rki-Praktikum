import numpy as np
import matplotlib.pyplot as plt
from Bio import Entrez, SeqIO
import math
from biom.table import Table
from biom.util import biom_open
import pandas as pd
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


# E-Mail-Adresse für NCBI-Datenbank
Entrez.email = "Amma2@gmx.de"

# Liste der Organismen, nach denen gesucht werden soll
organismen = [
    "Salmonella enterica",
    "Bifidobacterium longum",
    "Bacteroides thetaiotaomicron",
    "Bacteroides ovatus",
    "Escherichia coli"]

# Parameter für das Abundanzprofil
taxa = 10  # Maximal Anzahl der Taxa
mean = 1.0  # Mittelwert für lognormale Verteilung
sigma = 0.5  # Standardabweichung für lognormale Verteilung

# Sucht Taxon ID zu Organismen Namen in DB
def get_taxon_id(organism_name):
    handle = Entrez.esearch(db="taxonomy", term=organism_name)
    record = Entrez.read(handle)
    handle.close()
    if record["IdList"]:
        return record["IdList"][0]  # Rückgabe der ersten gefundenen Taxonomie-ID
    else:
        return None

# Sucht Proteine in DB zu den jeweiligen Taxon IDs
def get_protein_ids(taxon_id, retmax=10000):
    handle = Entrez.esearch(db="protein", term=f"txid{taxon_id}[Organism:exp]", retmax=retmax)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"] # gibt Liste mit Protein IDs zur jeweiligen Taxon ID zurück

# Erstellen der Abundanzprofile
def generate_abundance_profile(taxon_id, mean):
    protein_ids = get_protein_ids(taxon_id)
    if len(protein_ids) == 0:
        print("keine Protein IDs gefunden für Taxon ID {taxon_id}")
        return {}
    else:
        species_richness = (np.random.geometric(p=0.01)) # Zufällige Anzahl von Arten mittels geometrischer Verteilung
        selected_taxa = np.random.choice(protein_ids, size=species_richness, replace=False)  # Zufällige Auswahl von Taxa mittels Gleichverteilung
        abundances = np.random.lognormal(mean=mean, sigma=sigma, size=species_richness)  # Abundanzen erzeugen mittels Lognormal-Verteilung
        abundances /= abundances.sum()  # Abundanzen normalisieren
        abundance_profile = {taxon_id: abundances[taxon] for taxon, taxon_id in enumerate(selected_taxa)}
        return abundance_profile  # Gibt ein dictionary zurück mit jeweils [Protein-ID]: [Abundanz]

# Funktion zum Speichern eines DataFrames in einer BIOM-Datei
def save_df_to_biom(df, filename):
    observation_ids = list(map(str, df.index.tolist()))
    sample_ids = df.columns.tolist()
    data = df.values.T  # Transponieren, da BIOM spaltenweise arbeitet
    table = Table(data=data,observation_ids=sample_ids,sample_ids=observation_ids)
    with biom_open(filename, 'w') as f:
        table.to_hdf5(f, "Amma")

# Funktion zum erhalten der Proteinsequenzen aus DB
def get_sequences(taxon_ids):
    sequences = {}
    for taxon_id in taxon_ids:
        handle = Entrez.efetch(db="protein", id=taxon_id, rettype="fasta", retmode="text")
        record = SeqIO.read(handle, "fasta")
        handle.close()
        sequences[taxon_id] = record.seq
    return sequences # gibt ein dictionary zurück mit jeweils Protein ID zugehöriger Sequenz

#Funktion zur Alpha-Diversität Berechnung
def alpha_diversity(abundances):
    total_count = sum(abundances)  # Summe der Abundanzen
    probabilities = [count / total_count for count in abundances]  # Wahrscheinlichkeiten berechnen
    alpha_diversity_shannon = -sum(p * math.log(p) if p != 0 else 0 for p in probabilities)  # Shannon-Index berechnen
    return alpha_diversity_shannon # gibt Shannon-Diversity-Index zurück

# Erstellt ein Balken-Diagramm für einen bestimmten Organismus
def plot_abundances(abundance_profile, subplot_index, organism_name):
    IDs = list(abundance_profile.keys())  # x-Werte
    abundances = list(abundance_profile.values())  # y-Werte

    plt.subplot(2, 3, subplot_index)  # Subplot festlegen
    plt.bar(IDs, abundances, color='darkgreen')  # Säulendiagramm
    plt.xticks(rotation=45, ha='right', fontsize=8)  # x-Achse Beschriftung drehen und kleiner machen
    plt.yticks(fontsize=8)
    plt.xlabel('Taxon IDs', fontsize=8)
    plt.ylabel('Abundance', fontsize=8)
    alpha_diversity_text = f"Alpha diversity: {alpha_diversity(abundances):.2f}"  # Alpha-Diversität Text
    plt.text(0.5, 0.95, alpha_diversity_text, transform=plt.gca().transAxes, fontsize=8,
             horizontalalignment='center', verticalalignment='top')
    plt.title(organism_name, fontsize=10)  # Organismus als Titel für das Subplot
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

# erstellt eine FASTA Datei in der alle Proteine im Verhältnis zu ihrer Probe gelistet sind
def protein_fasta_with_absolute_abundances(absolute_abundance_profiles, organismen, fasta_filename):
    Entrez.email = "Amma2@gmx.de"  # erneut E-Mail-Adresse für DB Abfrage
    with open(fasta_filename, 'w') as f:
        all_records = []
        for i, abundance_profile in enumerate(absolute_abundance_profiles):
            for taxon_id, abundance in abundance_profile.items():
                try:
                    handle = Entrez.efetch(db="protein", id=taxon_id, rettype="fasta", retmode="text")
                    sequence = SeqIO.read(handle, "fasta").seq
                    handle.close()
                    for _ in range(abundance):
                        record = SeqRecord(Seq(sequence), id=f"ID_{taxon_id}", description=f"{organismen[i]}, abundance: {_+1}")
                        all_records.append(record)
                except Exception as e:
                    print(f"Fehler beim Abrufen von Sequenz für Taxon-ID {taxon_id}: {e}")
        SeqIO.write(all_records, f, "fasta")
        print(f"Proteinsequenzen aller Organismen wurden in '{fasta_filename}' gespeichert.")

# Erstellen der Liste mit dictionaries
abundance_profiles = []
absolute_abundance_profiles = []

for organism in organismen:
    taxon_id = get_taxon_id(organism)
    if taxon_id:
        abundance_profile = generate_abundance_profile(taxon_id, mean)
        absolute_abundance_dict = {key: int(round(value, 2)*100) for key, value in abundance_profile.items()}
        absolute_abundance_profiles.append(absolute_abundance_dict)
        abundance_profiles.append(abundance_profile)


# Erstellen der DataFrames für Abundanzen
abundance_df = pd.DataFrame(abundance_profiles).fillna(0).T
absolute_abundance_df = pd.DataFrame(absolute_abundance_profiles).fillna(0).T

# Setzen der Organismennamen als Index mit maximal `taxa` Spalten
abundance_df.columns = organismen[:taxa]
absolute_abundance_df.columns = organismen[:taxa]


# Test, ob abundance_df korrekt erstellt wird
print(abundance_df)

# Speichern der des DataFrames
save_df_to_biom(abundance_df,"Abundance_Profiles.biom")
print("Abundance_Profiles.biom wurde erstellt.")

# Erstellt FASTA Datei, die später für MS2Pip genutzt wird
protein_fasta_with_absolute_abundances(absolute_abundance_profiles,organismen,"all_organismen.fasta")

# erstellt eine Figur, die alle Diagrammme zusammen anzeigt
plt.figure(figsize=(15, 15))  # Größe der Figur festlegen
total_subplots = len(organismen)  # Anzahl der Subplots
for subplot_index, (abundance_profile, organism) in enumerate(zip(abundance_profiles, organismen), start=1):
    plot_abundances(abundance_profile, subplot_index, organism)
plt.suptitle('Abundance Profiles', fontsize=16)  # Titel für die gesamte Figur
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Layout anpassen
plt.savefig('abundance_diagramm.png') # Speichern der Figur als PNG-Datei
plt.show() # Anzeigen des Diagramms
