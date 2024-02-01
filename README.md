## Progetto di Algoritmi e Strutture Dati

Progetto per il corso di Algoritmi e Strutture Dati della laurea magistrale
in Ingegneria Informatica presso l'Università degli Studi di Brescia.


In questo documento sono riportate esclusivamente le istruzioni per l'avvio dell'applicazione.
Le scelte progettuali sono documentate nella relazione.
I test per verificare la performance dell'implementazione si trovano nel notebook Jupyter `test.ipynb`.

- [Progetto di Algoritmi e Strutture Dati](#progetto-di-algoritmi-e-strutture-dati)
- [Struttura progetto](#struttura-progetto)
- [Requisiti](#requisiti)
- [Avvio applicazione](#avvio-applicazione)
- [gen](#gen)
- [run](#run)
- [man](#man)
- [Formato file](#formato-file)
  - [File di input](#file-di-input)
    - [file csv](#file-csv)
    - [file pickle](#file-pickle)
- [file di output](#file-di-output)
  - [file markdown](#file-markdown)
  - [file csv](#file-csv-1)
  
## Struttura progetto
Di seguito si riporta la struttura dei file e delle cartelle.
- `benchmarks` contiene i file necessari per generare, testare e risolvere i problemi di ricerca.
- `pf4ea` contiene il codice sorgente del programma.
```
 [benchmarks]
    ├── [generators]        # file csv con le specifiche dei problemi 
    ├── [output_csv]        # file csv di output usati nei test
    ├── [problems]          # salva istanze problema
    └── [report]            # file report
        └── [media] 
[pf4ea]
    ├── __main__.py          # Punto di ingresso dell'applicazione
    ├── agents.py            # Generazione di percorsi agenti  
    ├── cli.py               # Interfaccia a riga di comando
    ├── constants.py         # Costanti utilizzate nel progetto
    ├── gridGraph.py         # Generazione griglia
    ├── heuristic.py         # Euristiche del problema 
    ├── input_handler.py     # Gestore input nella modalità manuale
    ├── plotGraph.py         # Rappresenta graficamente la griglia
    ├── problem.py           # Definisci il problema PF4EA
    ├── repository.py        # Gestisce le operazioni su file
    ├── result.py            # Gestisce i risultati della ricerca
    ├── search.py            # Implementa algoritmi ReachGoal e variante
    ├── state.py             # Generazioni istanze stato del problema   
    ├── utils.py             # Funzioni ausiliarie
    ├── visualize.py         # Visualizzazione grafica griglia

README.md                    # Questo file
requirements.txt             # Dipendenze Python
test.ipynb                   # notebook Jupyter per i test sulle performance
```
## Requisiti
Per avviare il programma è richiesto Python 3.10.11 o superiore.
Per il corretto funzionamento del programma devi installare le dipendenze indicate in `requirements.txt`. Per farlo, puoi usare il gestore di pacchetti `pip`, con il comando:
```python
pip install -r requirements.txt
```
## Avvio applicazione
Una volta installate le dipendenze, puoi avviare l'applicazione usando l'interprete di Python, specificando uno dei seguenti comandi:
- `gen` : genera da file i problemi e li risolve
- `run` : carica da file un problema e lo risolve
- `man` : genera e risolve un problema interagendo da terminale.

In qualsiasi momento è possibile possibile utilizzare l'opzione `-h` (o `--help`) per ottenere una descrizione delle opzioni disponibili.

Per esempio, per mostrare l'help del comando principale:
```
python gen -h
```

Di seguito vediamo nel dettaglio il funzionamento dei comandi
## gen
Il comando `gen` legge da file le specifiche dei problemi che si vogliono sottoporre all'algoritmo di ricerca , crea le relative istanze e le risolve. Le opzioni disponibili sono:
- `-f`, `--file`: file di input da cui leggere le specifiche dei problemi.
- `h`, `--hueristic`:  per l'euristica da adottare nella ricerca (h1,h2,h3,h4).
- `-v`,`--variant`: seleziona la variante di *ReachGoal*.
- `-r`, `--report`: salva il risultato dell'esecuzione su file markdown.
- `--show`: mostra a video la soluzione graficamente, usando matplotlib.
- `-s`, `--save`: salva l'istanza del problema su file pickle.
- `--csv_output`: scrive l'output su un file csv. (usato per il test sulle performance)

Per esempio, una volta definiti i problemi sul file, puoi sottoporli al programma nel seguente modo:
```
python pf4ea gen -f exp_0.csv --h h1 -r
```
Questo comando genererà e risolverà i problemi specificati nel file exp_0.csv, usando l’euristica h1 e salvando il report su file markdown.

Chiariamo che l'euristica viene inserita nel seguente modo:
- `h1`: Diagonal Distance,
- `h2`: Chebyshev Distance,
- `h3`: Manhattan Distance,
- `h4`: Euclidean Distance,
- `h5`: Heuristic Relax Path,

## run
Il comando `run` consente di caricare nel programma una istanza del problema precedentemente generata e di risolverla con l'algoritmo `ReachGoal` o la sua variante. Le opzioni supportate sono:
- `-i`, `--file`: file da cui caricare l'istanza del problema.
- `-o`, `--output`: file su cui salvare il risultato dell'algoritmo.
- `h`, `--hueristic`: per l'euristica da adottare (h1,h2,h3,h4),
- `-v`,`--variant`: seleziona la variante di *ReachGoal*.
- `-r`, `--report`: salva il risultato dell'esecuzione su file markdown.
- `--show`: mostra a video la soluzione graficamente.

Per esempio, per caricare e risolvere un problema dal file pickle, puoi scrivere:
```
python pf4ea run -i 50x50_08_01_20_60_2190_2460.pkl --h h1 -r
```
Questo comando caricherà il problema dal file pickle, lo risolverà con l’euristica h1 e salverà il report su file markdown.
## man
Il comando `man` consente di interagire con il programma attraverso il terminale, inserendo i dati del problema a mano. La soluzione verrà comunque mostrata sul file markdown.

## Formato file
### File di input
#### file csv
Il file di input contenente le specifiche dei problemi deve essere in formato csv.

```csv
# exp_0.csv
rows,cols,traversability_ratio,obstacle_agglomeration_ratio,num_agents,maximum_time
10,10,0.1,1,0,30
100,10,1,1,30,30
106,10,1,1,30,30
10,105,1,1,30,30
105,107,1,1,30,30
108,104,1,1,30,30
10564,102,1,1,30,30
```
Il file di input di default si trova nel percorso `benchmarks\generators\exp_0.csv`.
#### file pickle
il file pickle è un formato di Python per memorizzare un oggetto serializzato. I file contenenti le istanze si trova di default nel percorso `benchmarks\problems\50x50_08_01_20_60_2190_2460.pkl`.

## file di output
### file markdown
I report sono dei file markdown che contengono le seguenti informazioni:
- Dati del problema
- Risultati della ricerca
- Performance
- Immagine con la soluzione grafica
- video animazione della soluzione
Il file di report di default si trova nel percorso`benchmarks\report\50x50_08_01_20_60_247_73_DiagonalDistance.md.`
### file csv
Hai finiti del test sulle performance è possibile salvare l'output su un file csv.
Ad esempio:
```
rows,cols,traversability_ratio,obstacle_agglomeration_ratio,num_agents,maximum_time,init,goal,h_type,path_length,path_cost,tot_states,percentage_visited_nodes,unique_node_visited,wait,problem_time,heuristic_time,search_time,mem_grid,mem_heuristic,mem_open,mem_closed,mem_path

50,50,0.8,0.1,20,60,645,2285,DiagonalDistance,34,37.14213562373095,947,12.15,243,0,0.0,0.0,0.109375,0.046875,0.046875,0.046875,8.2109375,0.3203125
```
Di default viene salvato nel percorso `benchmarks\output_csv\output_exp_0.csv`.

