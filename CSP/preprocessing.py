import pandas as pd
from unidecode import unidecode # per togliere tutti gli accenti dalle lettere

def preprocessing():
    # Dizionario per sostituzioni delle sigle delle posizioni
    mappa_posizioni = {'GK': 'Portiere', 'RB': 'Terzino destro', 'CB': 'Difensore centrale',
                       'LB': 'Terzino sinistro', 'CM': 'Centrocampista centrale', 'CDM': 'Mediano',
                       'CAM': 'Trequartista', 'RW': 'Ala destra', 'ST': 'Prima punta', 'LW': 'Ala sinistra',
                       'LM': 'Esterno sinistro', 'RM': 'Esterno destro'}

    # Caricamento dataset
    dataset = pd.read_csv('dataset/dataset.csv')
    # Colonne da mantenere
    colonne = ['Known As', 'Overall', 'Positions Played', 'Value(in Euro)']
    # Selezione delle colonne
    ds = dataset[colonne]
    # Selezione dei primi 500 elementi
    ds = ds.iloc[:500]
    # Conversione da euro in milioni di euro del valore
    ds['Value(in Euro)'] = ds['Value(in Euro)'] / 1000000


    lista_giocatori = []
    for index, row in ds.iterrows():
        # Creazione di una tupla per ogni posizione di ogni singolo giocatore
        posizioni = [pos.strip() for pos in row['Positions Played'].split(',')]

        # Creazione di una tupla per ogni posizione del giocatore
        for posizione in posizioni:
            # Sostituzione sigla posizione con nome posizione
            nome_posizione = mappa_posizioni.get(posizione, posizione)
            giocatore = (row['Known As'], row['Overall'], nome_posizione, row['Value(in Euro)'])

            # Inserimento giocatore nel vettore
            lista_giocatori.append(giocatore)
    return lista_giocatori


# preprocessing del dataset csv
def pre(nazionalita):
    # caricamento del dataset dal file csv
    dataset = pd.read_csv('dataset/dataset.csv')

    if (nazionalita.lower() != 'all'):
        # rimozione di tutti i giocatori tranne quelli della nazionalita in input
        dataset = dataset[dataset['Nationality'].str.lower() == nazionalita]

    if (nazionalita.lower() == 'all' or len(dataset) > 0):
        # colonne utili da mantenere nel dataset
        colonne = ['Known As', 'Overall', 'Positions Played']

        # rimozione delle colonne inutili
        dataset_troncato = dataset[colonne]

        # mantenere solo i primi 100 calciatori in ordine di overall
        dataset_troncato = dataset_troncato.iloc[:100]

        # esportare il dataset su file
        dataset_troncato.to_csv("dataset\dataset_CSP.csv", index = False)

        # creare file prolog con i fatti sui giocatori della nazionale
        creare_clausole_prolog()

        return (1)
    
    else:
        return (0)

# creazione del file prolog
def creare_clausole_prolog():
    # caricamento del dataset
    dataset = pd.read_csv('dataset/dataset_CSP.csv')

    # creazione delle clausole
    with open('prolog_files/kb_calciatori_CSP.pl', 'w') as prolog_file:
        # ciclo per recuperare le tuple dal dataset
        for index, row in dataset.iterrows():
            # recupero dati singola tupla
            nome = row['Known As']
            ruoli = row["Positions Played"].split(",")
            overall = row['Overall']

            # normalizzazione delle stringhe
            nome = normalizzazione(nome)

            # inserimento di una tupla per ogni ruolo del singolo giocatore nel vettore
            for ruolo in ruoli:
                ruolo = normalizzazione(ruolo)
                clausola = f"calciatore('{nome}', '{ruolo}', {overall})."
                prolog_file.write(clausola + "\n")

# normalizzazione delle parole
def normalizzazione(parola):
    # trasformare tutte le lettere in minuscolo
    parola = parola.lower()
    # togliere i puntini che abbreviano i nomi
    parola = parola.replace(".", "")
    # togliere gli apostrofi dai cognomi
    parola = parola.replace("'", "")
    # togliere gli spazi
    parola = parola.replace(" ", "_")
    # togliere i trattini dai cognomi
    parola = parola.replace("-", "_")
    # togliere tutti gli accenti dalle lettere
    parola = unidecode(parola)

    return parola