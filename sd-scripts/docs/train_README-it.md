__Documento in fase di aggiornamento, potrebbero esserci errori nelle descrizioni.__

# Studio: Edizione condivisa

In questo repository supportiamo l'addestramento dei modelli, DreamBooth e LoRA insieme all'inversione testuale (XTI:P+ incluso). Questo documento spiega i metodi comuni per la preparazione dei dati di addestramento e le opzioni correlate.

# Panoramica

Prima di tutto, consultare il README di questo repository e preparare l'ambiente.

Verranno fornite spiegazioni su:

1. Preparazione dei dati di addestramento (nuovo formato con file di configurazione)
2. Breve glossario dei termini utilizzati nell'addestramento
3. Formato precedente (specificare tramite riga di comando senza file di configurazione)
4. Generazione di immagini campione durante l'addestramento
5. Opzioni comuni utilizzate in ciascuno script
6. Preparazione dei metadati per l'addestramento del fine tuning: ad esempio, annotazione delle immagini

Eseguendo solo il punto 1, è possibile iniziare l'addestramento (fare riferimento alla documentazione di ciascuno script per l'addestramento). Gli altri punti possono essere consultati in seguito, se necessario.

# Preparazione dei dati di addestramento

Preparare le immagini di addestramento in una o più cartelle. Supportiamo i formati `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`. In genere, non è necessaria alcuna pre-elaborazione come il ridimensionamento delle immagini.

Tuttavia, evitare di utilizzare immagini estremamente piccole rispetto alla risoluzione di addestramento (di seguito). È consigliabile ingrandire in anticipo le immagini estremamente piccole utilizzando l'intelligenza artificiale per la super risoluzione. Inoltre, ridimensionare le immagini estremamente grandi (circa 3000x3000 pixel?) prima dell'addestramento per evitare errori.

Durante l'addestramento, è necessario organizzare i dati delle immagini da far imparare al modello e specificarli agli script. È possibile specificare i dati di addestramento in diversi modi, a seconda del numero di dati di addestramento, dell'oggetto di addestramento e della disponibilità di annotazioni (descrizioni delle immagini). Di seguito sono riportati i metodi disponibili (i nomi utilizzati non sono comuni e sono specifici per questo repository). Le immagini di regolarizzazione verranno discusse in seguito.

1. DreamBooth, modalità class+identifier (con immagini di regolarizzazione)

   Addestramento associato a un determinato termine (identificatore). Non è necessario fornire descrizioni. È più semplice da usare per addestrare un personaggio specifico senza la necessità di descrizioni, ma poiché tutti gli elementi dei dati di addestramento sono collegati all'identificatore, potrebbe verificarsi un caso in cui non è possibile modificare gli abiti durante la generazione a causa di questo collegamento.

2. DreamBooth, modalità con descrizione (con immagini di regolarizzazione)

   Addestramento basato su file di testo che contiene descrizioni per ciascuna immagine. Ad esempio, addestrare un personaggio specifico con dettagli specifici (ad esempio, indossa una camicia bianca, indossa una camicia rossa, ecc.) permette di separare il personaggio da altri elementi, consentendo al modello di concentrarsi esclusivamente sul personaggio.

3. Modalità di fine tuning (senza immagini di regolarizzazione)

   Preparare i metadati (descrizioni) in un file separato. Supporta funzionalità come la gestione dei tag e delle descrizioni per accelerare l'addestramento (spiegato in documenti separati).

La combinazione dell'oggetto di addestramento e del metodo di specifica disponibile è la seguente:

| Oggetto di addestramento o metodo | Script | DB / class+identifier | DB / con descrizione | fine tuning |
| ----- | ----- | ----- | ----- | ----- |
| Fine tuning del modello | `fine_tune.py`| x | x | o |
| DreamBooth del modello | `train_db.py`| o | o | x |
| LoRA | `train_network.py`| o | o | o |
| Inversione testuale | `train_textual_inversion.py`| o | o | o |

## Scegliere il metodo

Per LoRA e l'inversione testuale, se si desidera addestrare senza dover preparare file di descrizione, la modalità DreamBooth class+identifier è preferibile se disponibile. Se il numero di immagini di addestramento è elevato e non si utilizzano immagini di regolarizzazione, è consigliabile considerare anche il metodo di fine tuning.

Per DreamBooth, lo stesso discorso si applica, ma non è possibile utilizzare il metodo di fine tuning. Questo metodo è utilizzabile solo per il fine tuning.

# Metodo di specifica per ciascun approccio

In questa sezione, vengono spiegati i modi tipici per specificare i dati per ciascun metodo. Per ulteriori dettagli, vedere [Configurazione del dataset](./config_README-ja.md).

# DreamBooth, modalità class+identifier (con immagini di regolarizzazione)

In questo metodo, ogni immagine viene addestrata con una descrizione nel formato "classe identificatore" (ad esempio, "shs cane").

## Passaggio 1: Scegliere identificatore e classe

Decidere l'identificatore (parola chiave) e la classe associata all'oggetto che si desidera addestrare.

Le classi rappresentano tipi generici di oggetti di addestramento. Ad esempio, se si vuole addestrare una razza specifica di cane, la classe sarà "cane". Per i personaggi di anime, le classi potrebbero essere "ragazzo" o "ragazza", oppure "1ragazzo" o "1ragazza" a seconda del modello.

Gli identificatori sono parole chiave per identificare gli oggetti di addestramento. Possono essere qualsiasi parola, ma secondo il paper originale, è consigliabile utilizzare parole


Utilizzo di identificatore e class per addestrare modelli utilizzando ad esempio "shs dog" per identificare la classe desiderata durante l'addestramento.

Durante la generazione delle immagini, utilizzando ad esempio "shs dog", verranno generate immagini della razza di cane appresa.

(Come riferimento, gli identificatori che ho recentemente utilizzato includono ``shs sts scs cpc coc cic msm usu ici lvl cic dii muk ori hru rik koo yos wny``. Idealmente, sarebbe preferibile utilizzare quelli non inclusi nei tag di Danbooru.)

## Passo 2: Decidere se utilizzare o meno immagini di regolarizzazione e, in caso affermativo, generare immagini di regolarizzazione

Le immagini di regolarizzazione sono immagini utilizzate per prevenire che l'intera classe sopra menzionata sia distorta durante l'addestramento (deriva del linguaggio). Senza immagini di regolarizzazione, ad esempio, se si addestra un personaggio specifico con "shs 1girl", anche generando semplicemente con "1girl", l'output tenderà ad assomigliare a quel personaggio specifico. Questo è dovuto alla presenza di "1girl" durante l'addestramento.

Addestrando contemporaneamente le immagini di interesse e le immagini di regolarizzazione, la classe rimarrà invariata mentre solo quando si aggiunge l'identificatore al prompt verranno generate le immagini di interesse.

Per utilizzi come LoRA o DreamBooth, in cui è necessario che compaiano solo personaggi specifici, potrebbe non essere necessario utilizzare immagini di regolarizzazione.

Non sono necessarie per l'inversione testuale (Textual Inversion) (poiché se la stringa del token da apprendere non è presente nella didascalia, non viene appreso nulla).

Le immagini di regolarizzazione di solito sono generate utilizzando il modello di interesse utilizzando solo i nomi delle classi (ad esempio "1girl"). Tuttavia, se la qualità delle immagini generate è scarsa, è possibile migliorare il prompt o utilizzare immagini scaricate separatamente da internet.

(Poiché le immagini di regolarizzazione vengono anch'esse apprese durante l'addestramento, ne influenzano la qualità.)

Di solito è consigliabile prepararne diverse centinaia (poiché un numero inferiore potrebbe portare a una generalizzazione insufficiente delle immagini di classe).

Se si utilizzano immagini generate, è consigliabile adattarne le dimensioni alla risoluzione dell'addestramento (o, più precisamente, alla risoluzione del bucket, come verrà spiegato in seguito).

## Passo 2: Descrizione del file di configurazione

Creare un file di testo e assegnargli l'estensione `.toml`. Ad esempio, si può scrivere come segue.

(Le parti che iniziano con `#` sono commenti e possono essere mantenute o eliminate senza problemi.)

```toml
[general]
enable_bucket = true                        # Decidere se utilizzare il bucketing dell'aspect ratio o meno

[[datasets]]
resolution = 512                            # Risoluzione dell'addestramento
batch_size = 4                              # Dimensione del batch

  [[datasets.subsets]]
  image_dir = 'C:\hoge'                     # Percorso della cartella contenente le immagini di addestramento
  class_tokens = 'hoge girl'                # Specificare le classi degli identificatori
  num_repeats = 10                          # Numero di ripetizioni delle immagini di addestramento

  # Da qui in poi è necessario solo se si utilizzano immagini di regolarizzazione. Se non necessario, eliminare.
  [[datasets.subsets]]
  is_reg = true
  image_dir = 'C:\reg'                      # Percorso della cartella contenente le immagini di regolarizzazione
  class_tokens = 'girl'                     # Specificare le classi
  num_repeats = 1                           # Numero di ripetizioni delle immagini di regolarizzazione, di solito 1 è sufficiente
```

Normalmente, è sufficiente modificare i seguenti parametri per addestrare il modello.

1. Risoluzione dell'addestramento

   Specificare un singolo valore per una forma quadrata (ad esempio, 512x512) o due valori separati da virgola per specificare larghezza e altezza (ad esempio, [512,768]). Per SD1.x, la risoluzione predefinita è 512. Per SD2.x 768, è 768.

1. Dimensione del batch

   Specificare quante immagini vengono addestrate contemporaneamente. Dipende dalla dimensione della VRAM della GPU e dalla risoluzione dell'addestramento. È possibile trovare maggiori dettagli nei rispettivi script di fine-tuning, DreamBooth, LoRA, ecc.

1. Specificare il percorso della cartella

   Specificare la cartella contenente le immagini di addestramento e, se necessario, quelle di regolarizzazione. Il percorso dovrebbe essere quello della cartella contenente i file di immagine stessi.

1. Specificare gli identificatori e le classi

   Come illustrato nell'esempio sopra.

1. Numero di ripetizioni

   Come spiegato di seguito.

### Sulla ripetizione

Il numero di ripetizioni viene utilizzato per bilanciare il numero di immagini di addestramento e di regolarizzazione. Poiché di solito ci sono più immagini di regolarizzazione rispetto alle immagini di addestramento, si ripetono le immagini di addestramento in modo da avere un rapporto 1:1 con le immagini di regolarizzazione.

Il numero di ripetizioni dovrebbe essere impostato in modo che "numero di ripetizioni delle immagini di addestramento × numero di immagini di addestramento ≥ numero di ripetizioni delle immagini di regolarizzazione × numero di immagini di regolarizzazione".

(Il numero di dati per un'epoca, ovvero il numero di volte che tutti i dati vengono passati attraverso la rete, è "numero di ripetizioni delle immagini di addestramento × numero di immagini di addestramento". Se il numero di immagini di regolarizzazione è maggiore, le immagini di regolarizzazione in eccesso non vengono utilizzate.)

## Passo 3: Addestramento
Per ulteriori approfondimenti si rimanda ai rispettivi documenti.

## DreamBooth, Metodo a Didascalie (Immagine con Regolarizzazione Consentita)

In questo metodo, ogni immagine viene addestrata con una didascalia.

### Passo 1: Preparare il file di didascalie

Nella cartella delle immagini di addestramento, inserisci un file con estensione `.caption` (può essere modificato nelle impostazioni) con lo stesso nome dell'immagine. Ogni file deve contenere solo una riga. L'encoding deve essere in `UTF-8`.

### Passo 2: Decidere se utilizzare un'immagine regolarizzata e, in caso affermativo, generarla

È simile alla forma class+identifier. Si può aggiungere una didascalia anche alle immagini regolarizzate, ma di solito non è necessario.

### Passo 3: Descrivere il file di configurazione

Crea un file di testo con estensione `.toml`. Ad esempio, scrivi quanto segue:

```toml
[generale]
enable_bucket = true                        # Utilizzare o meno l'Aspect Ratio Bucketing

[[datasets]]
resolution = 512                            # Risoluzione dell'addestramento
batch_size = 4                              # Dimensione del batch

  [[datasets.sottoinsiemi]]
  image_dir = 'C:\hoge'                     # Specifica la cartella delle immagini di addestramento
  caption_extension = '.caption'            # Estensione del file di didascalia, cambialo se si utilizza un'estensione diversa da .txt
  num_repeats = 10                          # Numero di ripetizioni delle immagini di addestramento

  # Descrivi solo se si utilizzano immagini regolarizzate. Elimina altrimenti
  [[datasets.sottoinsiemi]]
  is_reg = true
  image_dir = 'C:\reg'                      # Specifica la cartella delle immagini regolarizzate
  class_tokens = 'girl'                     # Specifica la classe
  num_repeats = 1                           # Numero di ripetizioni delle immagini regolarizzate, di solito 1 è sufficiente
```

Fondamentalmente, basta modificare i luoghi indicati per effettuare l'addestramento. Le parti non menzionate sono simili al metodo class+identifier.

1. Risoluzione dell'addestramento
2. Dimensione del batch
3. Specifica della cartella
4. Estensione del file di didascalia
5. Numero di ripetizioni

### Passo 4: Addestramento

Fai riferimento ai rispettivi documenti per l'addestramento.

## Metodo di Fine Tuning

### Passo 1: Preparare i metadati

Chiamiamo metadati un file di gestione che raccoglie didascalie e tag. È in formato JSON e ha estensione `.json`. Poiché la creazione è dettagliata, l'ho inserita alla fine di questo documento.

### Passo 2: Descrivere il file di configurazione

Crea un file di testo con estensione `.toml`. Ad esempio, scrivi quanto segue:

```toml
[generale]
shuffle_caption = true
keep_tokens = 1

[[datasets]]
resolution = 512                                    # Risoluzione dell'addestramento
batch_size = 4                                      # Dimensione del batch

  [[datasets.sottoinsiemi]]
  image_dir = 'C:\piyo'                             # Specifica la cartella delle immagini di addestramento
  metadata_file = 'C:\piyo\piyo_md.json'            # Nome del file di metadati
```

Fondamentalmente, basta modificare i luoghi indicati per effettuare l'addestramento. Le parti non menzionate sono simili ai metodi DreamBooth e class+identifier.

1. Risoluzione dell'addestramento
2. Dimensione del batch
3. Specifica della cartella
4. Nome del file di metadati

### Passo 3: Addestramento

Fai riferimento ai rispettivi documenti per l'addestramento.
# Breve spiegazione dei termini utilizzati nell'apprendimento

Sto omettendo dettagli e non comprendo appieno il significato, quindi vi prego di fare ricerche più approfondite da soli.

## Fine tuning (ottimizzazione fine)

Si riferisce al processo di addestramento e aggiustamento di un modello. A seconda del contesto, il significato può variare, ma in senso stretto, il fine tuning in Stable Diffusion si riferisce all'addestramento di un modello su immagini e didascalie. DreamBooth è un metodo speciale di fine tuning in senso stretto. In senso lato, il fine tuning include LoRA, Textual Inversion, Hypernetworks, e comprende l'intero processo di addestramento del modello.

## Passo (step)

In breve, un passo corrisponde a un calcolo sui dati di addestramento. Un passo consiste nel "far passare le didascalie dei dati di addestramento attraverso il modello attuale, confrontare le immagini generate con le immagini dei dati di addestramento e apportare lievi modifiche al modello per avvicinarlo ai dati di addestramento".

## Dimensione del batch

La dimensione del batch indica quanti dati vengono calcolati insieme in un singolo passo. Calcolare i dati insieme migliora la velocità. Inoltre, generalmente si dice che aumentare la dimensione del batch migliora anche la precisione.

Il numero totale di dati utilizzati per l'addestramento è dato da `dimensione del batch x numero di passi`. Pertanto, aumentare la dimensione del batch e ridurre il numero di passi può essere vantaggioso.

(Tuttavia, ad esempio, "dimensione del batch 1 con 1600 passi" e "dimensione del batch 4 con 400 passi" non producono gli stessi risultati. Con lo stesso tasso di apprendimento, generalmente il secondo caso rischia di non apprendere a sufficienza. Si consiglia di regolare il tasso di apprendimento (ad es. `2e-6`) o ridurre il numero di passi a 500 per ottenere risultati migliori.)

Aumentare la dimensione del batch comporta un maggiore consumo di memoria GPU. Se la memoria è insufficiente, si verificheranno errori e, al limite, la velocità di addestramento diminuirà. Si consiglia di regolare la dimensione del batch monitorando la quantità di memoria utilizzata tramite Task Manager o il comando `nvidia-smi`.

Si noti che "batch" significa "un insieme di dati".

## Tasso di apprendimento

In breve, il tasso di apprendimento indica quanto cambiare ad ogni passo. Specificare un valore elevato accelera l'apprendimento, ma può portare a cambiamenti eccessivi nel modello o impedire di raggiungere uno stato ottimale. Specificare un valore basso rallenta l'apprendimento e potrebbe comunque non portare allo stato ottimale.

Il fine tuning, DreamBooth, LoRA e altri metodi possono avere impostazioni diverse, e il tasso di apprendimento può variare anche in base ai dati di addestramento, al modello desiderato, alla dimensione del batch e al numero di passi. Si consiglia di iniziare con valori comuni e regolare man mano in base allo stato di apprendimento.

Di default, il tasso di apprendimento rimane costante per tutto l'addestramento. È possibile modificare il tasso di apprendimento tramite gli scheduler, che influenzerà i risultati.

## Epoca (epoch)

Un'epoca corrisponde al completamento dell'addestramento di tutti i dati di addestramento (quando i dati completano un ciclo). Se si specifica un numero di iterazioni, un'epoca si completa quando i dati completano un ciclo dopo quelle iterazioni.

Il numero di passi in un'epoca è fondamentalmente `numero di dati ÷ dimensione del batch`, ma utilizzando Aspect Ratio Bucketing, questo numero può aumentare leggermente (poiché i dati di bucket diversi non possono essere inclusi nello stesso batch, il numero di passi aumenta).

## Aspect Ratio Bucketing

Stable Diffusion v1 viene addestrato a 512x512, ma viene addestrato anche a risoluzioni come 256x1024 o 384x640. Questo riduce le parti ritagliate e si prevede che migliori la relazione tra didascalie e immagini apprese.

Inoltre, poiché è possibile addestrare a risoluzioni arbitrarie, non è necessario uniformare i rapporti di aspetto delle immagini in anticipo.

È possibile abilitare o disabilitare questa funzione tramite le impostazioni, ma nell'esempio di file di configurazione fino a questo punto è abilitata (impostata su `true`).

La risoluzione di addestramento viene regolata e creata verticalmente e orizzontalmente su incrementi di 64 pixel (impostazione predefinita, modificabile) entro un'area di risoluzione data come parametro (cioè l'uso di memoria). 

Nell'apprendimento automatico, è comune uniformare le dimensioni di input, ma non ci sono restrizioni particolari e, in realtà, è sufficiente uniformare le dimensioni all'interno dello stesso batch. Il bucketing di cui parla NovelAI sembra riferirsi alla classificazione preventiva dei dati di addestramento in risoluzioni di apprendimento diverse in base al rapporto di aspetto. Quindi, creando i batch con le immagini di ciascun bucket, si uniformano le dimensioni delle immagini nei batch.

# Formato di specifica precedente (senza utilizzare un file di configurazione ma specificando da riga di comando)

Questo metodo consiste nel specificare le opzioni da riga di comando senza utilizzare un file `.toml`. Ci sono il metodo DreamBooth class+identifier, il metodo DreamBooth con didascalia e il metodo di fine tuning.

## DreamBooth, metodo class+identifier

Si specifica il numero di iterazioni nel nome della cartella. Si utilizzano le opzioni `train_data_dir` e `reg_data_dir`.

### Passo 1. Preparare le immagini di addestramento

Creare una cartella per le immagini di addestramento. __All'interno di questa cartella__, creare directory con il seguente formato:

```
<numero di iterazioni>_<identifier> <classe>
```

Non dimenticare il trattino basso tra i valori.

Ad esempio, se si desidera ripetere i dati 20 volte con il prompt "sls frog", la cartella sarà "20_sls frog". Ecco un esempio:

![immagine](https://user-images.githubusercontent.com/52813779/210770636-1c851377-5936-4c15-90b7-8ac8ad6c2074.png)

### Addestramento con più classi e obiettivi (identifier)

Il processo è semplice: all'interno della cartella delle immagini di addestramento, creare cartelle con il formato `numero di iterazioni_<identifier> <classe>` per più classi e obiettivi. Fare lo stesso anche per la cartella delle immagini di regolarizzazione con il formato `numero di iterazioni_<classe>`.

Ad esempio, se si desidera addestrare contemporaneamente "sls frog" e "cpc rabbit", il processo sarà il seguente.

![image](https://user-images.githubusercontent.com/52813779/210777933-a22229db-b219-4cd8-83ca-e87320fc4192.png)

Quando c'è una sola classe e più oggetti di interesse, è sufficiente una sola cartella per le immagini regolarizzate. Ad esempio, se ci sono i personaggi A e B nella classe "1girl", si procede come segue:

- train_girls
  - 10_sls 1girl
  - 10_cpc 1girl
- reg_girls
  - 1_1girl

### Passaggio 2. Preparazione delle immagini regolarizzate

Ecco i passaggi da seguire quando si utilizzano immagini regolarizzate.

Creare una cartella per memorizzare le immagini regolarizzate. __Inoltre, al suo interno__ creare una directory con il nome ``<numero di ripetizioni>_<classe>``.

Ad esempio, se si desidera regolarizzare i dati con il prompt "frog" senza ripetizioni (solo una volta), il procedimento sarà il seguente.

![immagine](https://user-images.githubusercontent.com/52813779/210770897-329758e5-3675-49f1-b345-c135f1725832.png)


### Passaggio 3. Esecuzione dell'addestramento

Eseguire ciascuno script di addestramento. Utilizzare l'opzione `--train_data_dir` per specificare la cartella dei dati di addestramento (__non la cartella contenente le immagini, ma la cartella genitore__) e l'opzione `--reg_data_dir` per specificare la cartella delle immagini regolarizzate (__non la cartella contenente le immagini, ma la cartella genitore__).

## DreamBooth, modalità di didascalia

Nelle cartelle dei dati di addestramento e delle immagini regolarizzate, è possibile inserire un file con lo stesso nome dell'immagine, ma con estensione .caption (può essere modificata come opzione), da cui verrà letta la didascalia per l'addestramento come prompt.

__Nota:__ Il nome della cartella (classe identificativa) non verrà più utilizzato per l'addestramento di tali immagini.

L'estensione predefinita del file di didascalia è .caption. È possibile modificarla utilizzando l'opzione `--caption_extension` nello script di addestramento. Utilizzando l'opzione `--shuffle_caption`, è possibile mescolare le varie parti della didascalia durante l'addestramento.

## Modalità di fine tuning

La creazione dei metadati avviene in modo simile a quando si utilizza un file di configurazione. Specificare il file di metadati con l'opzione `in_json`.

# Output di esempio durante l'addestramento

È possibile controllare l'avanzamento dell'addestramento generando immagini con il modello in fase di addestramento. Specificare le seguenti opzioni nello script di addestramento.

- `--sample_every_n_steps` / `--sample_every_n_epochs`
    
    Specificare il numero di passi o epoche per generare un output di esempio. Verrà generato un output di esempio ogni tot passi. Se entrambi sono specificati, verrà dato priorità al numero di epoche.

- `--sample_prompts`

    Specificare il file di prompt per l'output di esempio.

- `--sample_sampler`

    Specificare il campionatore da utilizzare per l'output di esempio. È possibile scegliere tra `'ddim', 'pndm', 'heun', 'dpmsolver', 'dpmsolver++', 'dpmsingle', 'k_lms', 'k_euler', 'k_euler_a', 'k_dpm_2', 'k_dpm_2_a'`.

Per generare un output di esempio, è necessario preparare in anticipo un file di testo contenente i prompt. Ogni prompt deve essere scritto su una riga separata.

Ad esempio:

```txt
# prompt 1
capolavoro, di ottima qualità, 1 ragazza, in camicie bianche, parte superiore del corpo, che guarda lo spettatore, sfondo semplice --n bassa qualità, pessima qualità, anatomia scadente, composizione scadente, povero, poco sforzo --w 768 --h 768 --d 1 --l 7.5 --s 28

# prompt 2
capolavoro, di ottima qualità, 1 ragazzo, in abito da lavoro, in piedi in strada, guardando indietro --n bassa qualità, pessima qualità, anatomia scadente, composizione scadente, povero, poco sforzo --w 576 --h 832 --d 2 --l 5.5 --s 40
```

Le righe che iniziano con `#` sono commenti. Utilizzando il formato `--` seguito da una lettera minuscola, è possibile specificare opzioni per le immagini generate. Le seguenti opzioni sono disponibili:

- `--n` Specifica che le opzioni seguenti sono negative.
- `--w` Specifica la larghezza dell'immagine generata.
- `--h` Specifica l'altezza dell'immagine generata.
- `--d` Specifica il seed dell'immagine generata.
- `--l` Specifica il CFG scale dell'immagine generata.
- `--s` Specifica il numero di passaggi durante la generazione.

# Opzioni comuni utilizzate in ciascuno script

Dopo l'aggiornamento dello script, potrebbe accadere che la documentazione non sia stata ancora aggiornata. In tal caso, controlla le opzioni disponibili utilizzando l'opzione `--help`.

## Specifica del modello da utilizzare per l'apprendimento

- `--v2` / `--v_parameterization`
    
    Se si desidera utilizzare il modello di apprendimento Hugging Face stable-diffusion-2-base o un modello di fine tuning da esso derivato (nel caso in cui il modello richieda l'uso di `v2-inference.yaml` durante l'infereza), specifica l'opzione `--v2`. Se si desidera utilizzare il modello stable-diffusion-2 o 768-v-ema.ckpt e i relativi modelli di fine tuning (nel caso in cui il modello richieda l'uso di `v2-inference-v.yaml` durante l'infereza), specifica entrambe le opzioni `--v2` e `--v_parameterization`.

    In Stable Diffusion 2.0 sono stati apportati i seguenti cambiamenti significativi:

    1. Tokenizer utilizzato
    2. Text Encoder utilizzato e il layer di output (2.0 utilizza il penultimo layer)
    3. Dimensione dell'output del Text Encoder (da 768 a 1024)
    4. Struttura di U-Net (numero di head di CrossAttention, ecc.)
    5. v-parameterization (sembra che il metodo di campionamento sia stato modificato)

    Per il modello base, vengono adottati i punti da 1 a 4, mentre per il modello senza base (768-v) vengono adottati i punti da 1 a 5. L'opzione v2 abilita i punti da 1 a 4, mentre l'opzione v_parameterization abilita il punto 5.

- `--pretrained_model_name_or_path` 
    
    Specifica il modello di partenza per l'apprendimento aggiuntivo. Puoi specificare il file di checkpoint di Stable Diffusion (.ckpt o .safetensors), la directory del modello presente sul disco locale di Diffusers, l'ID del modello di Diffusers ("stabilityai/stable-diffusion-2", ad esempio).

## Impostazioni relative all'apprendimento

- `--output_dir`

    Specifica la cartella in cui salvare il modello dopo l'apprendimento.

- `--output_name`

    Specifica il nome del file del modello senza estensione.

- `--dataset_config`

    Specifica il file `.toml` che contiene le impostazioni del dataset.

- `--max_train_steps` / `--max_train_epochs`

    Specifica il numero di passaggi di addestramento o epoche da eseguire. Se entrambi sono specificati, verrà dato priorità al numero di epoche.

- `--mixed_precision`

    Per risparmiare memoria, l'addestramento viene eseguito con precisione mista (mixed precision). Specificare come `--mixed_precision="fp16"`. Anche se la precisione mista potrebbe ridurre la precisione, consente di ridurre notevolmente la quantità di memoria GPU necessaria.

    (A partire dalla serie RTX30, è possibile specificare anche `bf16`. Assicurarsi di abbinare questa impostazione con quella eseguita con accelerate durante la configurazione dell'ambiente).

- `--gradient_checkpointing`

    Riduce la quantità di memoria GPU necessaria durante l'addestramento suddividendo il calcolo dei pesi in piccoli passaggi anziché farlo tutto insieme. L'attivazione o disattivazione non influisce sulla precisione, ma attivandola è possibile aumentare le dimensioni del batch, con conseguente impatto su questo aspetto.

    Di solito, attivando questa opzione si riduce la velocità, ma poiché consente di aumentare le dimensioni del batch, potrebbe addirittura accelerare complessivamente il tempo di addestramento.

- `--xformers` / `--mem_eff_attn`

    Specificando l'opzione xformers, si utilizza il CrossAttention di xformers. Se xformers non è installato o si verifica un errore (a seconda dell'ambiente, ad esempio con `mixed_precision="no"`), è possibile utilizzare l'opzione `mem_eff_attn` per utilizzare il CrossAttention a bassa memoria (più lento rispetto a xformers).

- `--clip_skip`

    Specificando `2`, si utilizza l'output del secondo strato dal fondo dell'Encoder di testo (CLIP). Se si specifica `1` o si omette l'opzione, viene utilizzato l'ultimo strato.

    *Nota: SD2.0 utilizza di default il secondo strato dal fondo, quindi non specificare questa opzione durante l'addestramento di SD2.0.*

    Se il modello in addestramento utilizza originariamente il secondo strato, specificare `2` potrebbe essere una buona scelta.

    Se invece il modello utilizzava l'ultimo strato, l'intero modello è stato addestrato su questa base. Pertanto, se si desidera addestrare nuovamente utilizzando il secondo strato, potrebbe essere necessario un numero significativo di dati di addestramento e un periodo di addestramento più lungo.

- `--max_token_length`

    Il valore predefinito è 75. Specificando `150` o `225`, è possibile estendere la lunghezza del token per l'addestramento. Si consiglia di specificare questo valore quando si addestra con didascalie lunghe.

    Tuttavia, è consigliabile addestrare con una lunghezza di token di 75 se non è necessario, poiché le specifiche di estensione del token durante l'addestramento potrebbero differire leggermente da quelle dell'interfaccia utente Web di Automatic1111 (ad esempio, per quanto riguarda la suddivisione), e potrebbe essere necessario un numero significativo di dati di addestramento e un periodo di addestramento più lungo se si addestra con una lunghezza diversa da quella dello stato di addestramento del modello.

- `--weighted_captions`

    Specificando questa opzione, si attivano didascalie pesate come nell'interfaccia Web di Automatic1111. Può essere utilizzato per l'addestramento non solo con "Textual Inversion e XTI", ma anche con il token string del metodo DreamBooth.

    La notazione delle didascalie pesate è simile a quella dell'interfaccia Web, con l'utilizzo di parentesi tonde `(abc)`, quadre `[abc]`, o con valori `(abc:1.23)`. È possibile annidare le parentesi e si consiglia di evitare di includere virgole all'interno delle parentesi per evitare problemi di corrispondenza durante la manipolazione di shuffle/dropout dei prompt.

- `--persistent_data_loader_workers`

    Specificando questa opzione in un ambiente Windows, si riduce notevolmente il tempo di attesa tra le epoche.

- `--max_data_loader_n_workers`

    Specifica il numero di processi di caricamento dati. Un numero maggiore di processi consente un caricamento più veloce dei dati e un utilizzo più efficiente della GPU, ma consuma memoria principale. Il valore predefinito è il minore tra `8` o `CPU_same_thread_number-1`, quindi se non c'è spazio sufficiente in memoria principale o l'utilizzo della GPU è superiore al 90%, è consigliabile ridurre questi valori a `2` o `1`.

- `--logging_dir` / `--log_prefix`

    Opzioni per il salvataggio dei log di addestramento. Specificare la directory di salvataggio dei log con l'opzione logging_dir. I log in formato TensorBoard verranno salvati in questa cartella.

    Ad esempio, specificando `--logging_dir=logs`, verrà creata una cartella logs nella cartella di lavoro e i log verranno salvati nella sottocartella con la data. Specificando anche l'opzione log_prefix, verrà aggiunto un prefisso al timestamp per identificare i log. Ad esempio, `--logging_dir=logs --log_prefix=db_style1_`.

    Per visualizzare i log con TensorBoard, aprire un'altra finestra della riga di comando nella cartella di lavoro e inserire il seguente comando:

    ```
    tensorboard --logdir=logs
    ```

    (TensorBoard dovrebbe essere installato durante la configurazione dell'ambiente, ma se non lo è, installalo con `pip install tensorboard`). Successivamente, aprire un browser e accedere a http://localhost:6006/ per visualizzare i log.

- `--log_with` / `--log_tracker_name`

    Opzioni per il salvataggio dei log di addestramento. È possibile salvare i log su `tensorboard` o `wandb`. Per ulteriori dettagli, consultare [PR#428](https://github.com/kohya-ss/sd-scripts/pull/428).

- `--noise_offset`

    Implementazione dell'articolo disponibile qui: https://www.crosslabs.org//blog/diffusion-with-offset-noise. Potrebbe migliorare i risultati della generazione di immagini scure o chiare. È efficace anche durante l'addestramento di LoRA. Si consiglia di specificare un valore di circa `0.1`.

- `--adaptive_noise_scale` (Opzione sperimentale)

    Regola automaticamente il valore di noise offset in base al valore assoluto medio dei canali latenti. Attivare questa opzione insieme a `--noise_offset`. Il valore di noise offset viene calcolato come `noise_offset + abs(mean(latents, dim=(2,3))) * adaptive_noise_scale`. Si consiglia di specificare un valore di circa 1/10 o simile a quello di noise offset, poiché i latenti sono distribuiti in modo simile a una distribuzione normale.

    È possibile specificare valori negativi, in tal caso il noise offset verrà limitato a zero o superiore.

- `--multires_noise_iterations` / `--multires_noise_discount`

    Impostazioni per il rumore a risoluzione multipla (rumore a piramide). Per ulteriori dettagli, consultare [PR#471](https://github.com/kohya-ss/sd-scripts/pull/471) e la pagina [Multi-Resolution Noise for Diffusion Model Training](https://wandb.ai/johnowhitaker/multires_noise/reports/Multi-Resolution-Noise-for-Diffusion-Model-Training--VmlldzozNjYyOTU2).

    Specificando un valore numerico con `--multires_noise_iterations`, si attiva questa funzionalità. Si consiglia un valore di circa 6-10. Con `--multires_noise_discount`, specificare un valore di circa 0.1-0.3 (raccomandato dall'autore del PR per dataset di dimensioni relativamente piccole come LoRA) o circa 0.8 (raccomandato nell'articolo originale) (il valore predefinito è 0.3).

- `--debug_dataset`

    Specificando questa opzione, è possibile controllare quali immagini e didascalie verranno utilizzate per l'addestramento prima di iniziare effettivamente l'addestramento. Premere Esc per interrompere e tornare alla riga di comando. Premere `S` per passare al passaggio successivo (batch) e `E` per passare alla prossima epoca.

    *Nota: In un ambiente Linux (compreso Colab), le immagini non verranno visualizzate.*

- `--vae`

    Specificando l'opzione vae con il checkpoint di Stable Diffusion, il checkpoint di VAE o il modello Diffusers o VAE (specificato come ID del modello locale o di Hugging Face), si utilizzerà quel VAE durante l'addestramento (per la cache dei latenti o per l'ottenimento dei latenti durante l'addestramento).

    Nei metodi DreamBooth e fine tuning, il modello salvato includerà questo VAE.

- `--cache_latents` / `--cache_latents_to_disk`

    Memorizza l'output del VAE nella memoria principale per ridurre l'utilizzo della VRAM. L'opzione di aumento `flip_aug` non sarà più disponibile. Inoltre, la velocità complessiva dell'addestramento potrebbe aumentare leggermente.

    Specificando `cache_latents_to_disk`, i dati memorizzati verranno salvati su disco. Anche se lo script viene interrotto e riavviato, la cache rimarrà attiva.

- `--min_snr_gamma`

    Specifica la strategia di pesatura Min-SNR. Per ulteriori dettagli, consultare [qui](https://github.com/kohya-ss/sd-scripts/pull/308). Il valore raccomandato è `5`.

## Impostazioni per il salvataggio del modello

- `--save_precision`

    Specifica la precisione dei dati durante il salvataggio. Specificare `float`, `fp16` o `bf16` per salvare il modello in quel formato (non valido per il salvataggio del modello in formato Diffusers durante DreamBooth o fine tuning). Utile per ridurre le dimensioni del modello.

- `--save_every_n_epochs` / `--save_state` / `--resume`

    Specificando un numero con `save_every_n_epochs`, il modello in fase di addestramento verrà salvato ogni tot epoche.

    Specificando anche `save_state`, verrà salvato lo stato dell'addestramento, compresi ottimizzatori e altro. Il modello salvato può essere utilizzato per riprendere l'addestramento (rispetto a riprendere da zero, si possono ottenere miglioramenti di precisione e riduzione del tempo di addestramento). I dati di addestramento verranno salvati nella cartella specificata.

    Lo stato dell'addestramento verrà salvato nella sottocartella `<output_name>-??????-state` (?????? è il numero di epoche) all'interno della cartella di salvataggio. Utile per addestramenti a lungo termine.

    Per riprendere l'addestramento da uno stato salvato, utilizzare l'opzione `resume`. Specificare la cartella dello stato dell'addestramento (non `output_dir`, ma la sottocartella state) come argomento.

    Si noti che a causa delle specifiche dell'Accelerator, il numero di epoche e i passaggi globali non vengono salvati e riprendendo l'addestramento si riparte da zero.

- `--save_every_n_steps`

    Specificando un numero con `save_every_n_steps`, il modello in fase di addestramento verrà salvato ogni tot passaggi.

- `--save_model_as` (Solo DreamBooth, fine tuning)

    Specifica il formato di salvataggio del modello tra `ckpt, safetensors, diffusers, diffusers_safetensors`.

    Specificare come `--save_model_as=safetensors`. Se si carica un modello in formato Stable Diffusion (ckpt o safetensors) e si desidera salvarlo in formato Diffusers, le informazioni mancanti verranno integrate con le informazioni di Hugging Face v1.5 o v2.1.

- `--huggingface_repo_id` e altri

    Se è specificato `huggingface_repo_id`, il modello verrà caricato contemporaneamente su HuggingFace durante il salvataggio. Fare attenzione alla gestione dell'accesso al token (consultare la documentazione di HuggingFace).

    Specificare altri argomenti come segue:

    -   `--huggingface_repo_id "your-hf-name/your-model" --huggingface_path_in_repo "path" --huggingface_repo_type model --huggingface_repo_visibility private --huggingface_token hf_YourAccessTokenHere`

    Specificando `public` per `huggingface_repo_visibility`, il repository sarà pubblico. Se non specificato o specificato come `private` (diverso da public), il repository sarà privato.

    Specificando `--save_state` insieme a `--save_state_to_huggingface`, lo stato verrà caricato anche su HuggingFace.

    Specificando `--resume` insieme a `--resume_from_huggingface`, lo stato verrà scaricato da HuggingFace per riprendere l'addestramento. In questo caso, l'opzione `--resume` diventerà `--resume {repo_id}/{path_in_repo}:{revision}:{repo_type}`.

    Esempio: `--resume_from_huggingface --resume your-hf-name/your-model/path/test-000002-state:main:model`.

    Specificando `--async_upload`, il caricamento verrà eseguito in modo asincrono.

## Ottimizzazioni relative all'ottimizzatore

- `--optimizer_type`

    Specifica il tipo di ottimizzatore. È possibile scegliere tra i seguenti:
    - AdamW: [torch.optim.AdamW](https://pytorch.org/docs/stable/generated/torch.optim.AdamW.html)
    - Impostazioni predefinite senza specificare l'opzione in versioni precedenti
    - AdamW8bit: stesse impostazioni di cui sopra
    - PagedAdamW8bit: stesse impostazioni di cui sopra
    - Impostazioni predefinite quando l'opzione --use_8bit_adam non era specificata in versioni precedenti
    - Lion: https://github.com/lucidrains/lion-pytorch
    - Impostazioni predefinite quando l'opzione --use_lion_optimizer non era specificata in versioni precedenti
    - Lion8bit: stesse impostazioni di cui sopra
    - PagedLion8bit: stesse impostazioni di cui sopra
    - SGDNesterov: [torch.optim.SGD](https://pytorch.org/docs/stable/generated/torch.optim.SGD.html), nesterov=True
    - SGDNesterov8bit: stesse impostazioni di cui sopra
    - DAdaptation(DAdaptAdamPreprint): https://github.com/facebookresearch/dadaptation
    - DAdaptAdam: stesse impostazioni di cui sopra
    - DAdaptAdaGrad: stesse impostazioni di cui sopra
    - DAdaptAdan: stesse impostazioni di cui sopra
    - DAdaptAdanIP: stesse impostazioni di cui sopra
    - DAdaptLion: stesse impostazioni di cui sopra
    - DAdaptSGD: stesse impostazioni di cui sopra
    - Prodigy: https://github.com/konstmish/prodigy
    - AdaFactor: [Transformers AdaFactor](https://huggingface.co/docs/transformers/main_classes/optimizer_schedules)
    - Qualsiasi altro ottimizzatore

- `--learning_rate`

    Specifica il tasso di apprendimento. Il tasso di apprendimento corretto dipende dallo script di addestramento specifico, quindi fare riferimento alle relative istruzioni.

- `--lr_scheduler` / `--lr_warmup_steps` / `--lr_scheduler_num_cycles` / `--lr_scheduler_power`

    Impostazioni relative allo scheduler del tasso di apprendimento.

    Con `lr_scheduler`, è possibile scegliere tra gli scheduler di apprendimento lineare, cosinusoidale, cosinusoidale con riavvii, polinomiale, costante, costante con warmup o qualsiasi altro scheduler. Il valore predefinito è costante.

    Con `lr_warmup_steps`, è possibile specificare il numero di passaggi di warmup dello scheduler (graduale variazione del tasso di apprendimento).
    

lr_scheduler_num_cycles è il numero di riavvii nel programma cosine with restarts, lr_scheduler_power è il polinomiale power nel programma polinomiale.

Per ulteriori dettagli, si prega di fare ricerche individuali.

Se si utilizza un qualsiasi programma di scheduling, si prega di specificare gli argomenti opzionali con `--scheduler_args`, come si farebbe con qualsiasi ottimizzatore.

### Specifiche sull'ottimizzatore

Si prega di specificare gli argomenti opzionali dell'ottimizzatore con l'opzione `--optimizer_args`. Si possono specificare più valori in formato key=value, con i valori separati da virgola. Ad esempio, per specificare gli argomenti per l'ottimizzatore AdamW, si utilizzerà ``--optimizer_args weight_decay=0.01 betas=.9,.999``.

Quando si specificano gli argomenti opzionali, si prega di consultare le specifiche di ciascun ottimizzatore.

Alcuni ottimizzatori richiedono argomenti obbligatori che verranno aggiunti automaticamente se omessi (come il momentum di SGDNesterov). Si prega di controllare l'output della console.

L'ottimizzatore D-Adaptation regola automaticamente il tasso di apprendimento. Il valore specificato per l'opzione del tasso di apprendimento non è il tasso di apprendimento effettivo, ma il tasso di applicazione del tasso di apprendimento determinato da D-Adaptation. Di solito si consiglia di specificare 1.0. Se si desidera impostare la metà del tasso di apprendimento per il Text Encoder rispetto a U-Net, si utilizzerà ``--text_encoder_lr=0.5 --unet_lr=1.0``.

L'ottimizzatore AdaFactor consente di regolare automaticamente il tasso di apprendimento specificando relative_step=True (aggiunto automaticamente se omesso). Quando si regola automaticamente, il programma di scheduling del tasso di apprendimento adafactor_scheduler viene utilizzato automaticamente. Inoltre, è consigliabile specificare scale_parameter e warmup_init.

Per specificare l'opzione per la regolazione automatica, si utilizzerà ad esempio ``--optimizer_args "relative_step=True" "scale_parameter=True" "warmup_init=True"``.

Se non si desidera regolare automaticamente il tasso di apprendimento, si prega di aggiungere l'opzione ``relative_step=False``. In questo caso, il programma di scheduling del tasso di apprendimento sarà constant_with_warmup e si consiglia di non effettuare il clipping del gradiente normale. Pertanto, gli argomenti saranno ``--optimizer_type=adafactor --optimizer_args "relative_step=False" --lr_scheduler="constant_with_warmup" --max_grad_norm=0.0``.

### Utilizzo di qualsiasi ottimizzatore

Quando si utilizza l'ottimizzatore della classe ``torch.optim``, si prega di specificare solo il nome della classe (come ``--optimizer_type=RMSprop``), mentre per utilizzare l'ottimizzatore di un altro modulo, si prega di specificare "nome_modulo.nome_classe" (come ``--optimizer_type=bitsandbytes.optim.lamb.LAMB``).

(Si sta solo importando il modulo e non è stata confermata la funzionalità. Si prega di installare il pacchetto se necessario.)

<!-- 
## Addestramento con immagini di dimensioni arbitrarie --resolution
È possibile addestrare con immagini non quadrate. Specificare la risoluzione come "larghezza,altezza" (ad esempio "448,640"). La larghezza e l'altezza devono essere divisibili per 64. Si prega di allineare le dimensioni delle immagini di addestramento e di regolarizzazione.

Personalmente, spesso genero immagini verticali, quindi potrei addestrare con "448,640" e simili.

## Aspect Ratio Bucketing --enable_bucket / --min_bucket_reso / --max_bucket_reso
Specificare l'opzione enable_bucket per abilitare. Stable Diffusion è addestrato con 512x512, ma verrà addestrato anche con risoluzioni come 256x768 o 384x640.

Con questa opzione, non è necessario uniformare le dimensioni delle immagini di addestramento e di regolarizzazione a una risoluzione specifica. Si sceglierà la migliore risoluzione (rapporto d'aspetto) da diverse risoluzioni e addestrerà con quella risoluzione.
Poiché la risoluzione è per unità di 64 pixel, potrebbe non corrispondere esattamente all'immagine originale se il rapporto d'aspetto non è perfettamente allineato, in tal caso, le parti in eccesso verranno ritagliate leggermente.

È possibile specificare la dimensione minima con l'opzione min_bucket_reso e la dimensione massima con max_bucket_reso. I valori predefiniti sono rispettivamente 256 e 1024.
Ad esempio, se si imposta 384 come dimensione minima, non verranno utilizzate risoluzioni come 256x1024 o 320x768.
Se si aumenta la risoluzione a 768x768, potrebbe essere utile specificare un valore come 1280 per la dimensione massima.

Inoltre, quando si abilita Aspect Ratio Bucketing, potrebbe essere utile preparare varie risoluzioni simili per le immagini di regolarizzazione come per le immagini di addestramento.

(Poiché le immagini all'interno di un batch non saranno più sbilanciate tra immagini di addestramento e di regolarizzazione. Non credo abbia un impatto significativo...)

## Augmentation --color_aug / --flip_aug
L'augmentation è una tecnica che aumenta le prestazioni del modello modificando dinamicamente i dati durante l'addestramento. Con color_aug si modificano leggermente le tonalità e con flip_aug si esegue una trasformazione flip orizzontale durante l'addestramento.

Poiché i dati vengono modificati dinamicamente, non è possibile specificare contemporaneamente l'opzione cache_latents.

## Addestramento con gradienti fp16 (funzionalità sperimentale) --full_fp16
Specificando l'opzione full_fp16, si addestrerà utilizzando gradienti in float16 (fp16) anziché float32 standard (non mixed precision, ma addestramento fp16 completo sembra essere il caso). Con dimensioni di 512x512 in SD1.x, sembra possibile addestrare con meno di 8GB di VRAM, mentre con dimensioni di 512x512 in SD2.x, sembra possibile addestrare con meno di 12GB di VRAM.

Prima di specificare full_fp16, si prega di impostare fp16 in accelerate config e specificare ``mixed_precision="fp16"`` come opzione (non funzionerà con bf16).

Per minimizzare l'uso della memoria, si prega di specificare le opzioni xformers, use_8bit_adam, cache_latents e gradient_checkpointing, e impostare train_batch_size a 1.

(Se c'è spazio, aumentare gradualmente train_batch_size dovrebbe portare a un leggero miglioramento delle prestazioni.)

È stato applicato un patch al codice sorgente di PyTorch per realizzare questa funzionalità (confermato con PyTorch 1.12.1 e 1.13.0). La precisione diminuirà notevolmente e la probabilità di fallimento durante l'addestramento aumenterà. Anche le impostazioni di tasso di apprendimento e numero di passaggi sembrano essere sensibili. Si prega di utilizzare a proprio rischio e di essere consapevoli di queste considerazioni.

-->

# Creazione del file di metadati

## Preparazione dei dati di addestramento

Preparare i dati delle immagini che si desidera addestrare come menzionato in precedenza e inserirli in una cartella a piacere.

Ad esempio, le immagini possono essere archiviate come segue.

![Screenshot della cartella dei dati di addestramento](https://user-images.githubusercontent.com/52813779/208907739-8e89d5fa-6ca8-4b60-8927-f484d2a9ae04.png)

## Generazione automatica delle didascalie

Se si desidera addestrare solo utilizzando i tag senza utilizzare le didascalie, è possibile saltare questa parte.

Inoltre, se si desidera preparare manualmente le didascalie, assicurarsi di creare le didascalie nella stessa cartella delle immagini di addestramento, con lo stesso nome file e l'estensione ".caption" o simile. Ogni file deve essere un file di testo con una sola riga.

### Generazione delle didascalie tramite BLIP

Nell'ultima versione, non è più necessario scaricare BLIP, i pesi o aggiungere un ambiente virtuale. Funzionerà direttamente.

Eseguire il file make_captions.py nella cartella finetune.

```
python finetune\make_captions.py --batch_size <dimensione_batch> <cartella_dati_di_addestramento>
```

Ad esempio, se si utilizza una dimensione batch di 8 e si posizionano i dati di addestramento nella cartella principale "train_data", l'esecuzione sarà la seguente.

```
python finetune\make_captions.py --batch_size 8 ..\train_data
```

I file di didascalia verranno creati nella stessa cartella delle immagini di addestramento con lo stesso nome file e l'estensione ".caption".

Si consiglia di regolare la dimensione del batch in base alla capacità della VRAM della GPU. Un valore più alto renderà il processo più veloce (anche con una VRAM da 12 GB si potrebbe aumentare leggermente).

È possibile specificare la lunghezza massima delle didascalie con l'opzione max_length. Il valore predefinito è 75. Potrebbe essere utile aumentarlo se si sta addestrando il modello con una lunghezza dei token di 225.

È possibile modificare l'estensione delle didascalie con l'opzione caption_extension. Il valore predefinito è ".caption" (cambiandolo in ".txt potrebbe causare conflitti con DeepDanbooru come descritto successivamente).

Se si dispone di più cartelle di dati di addestramento, eseguire il comando per ciascuna cartella.

Poiché l'inferenza è soggetta a casualità, i risultati varieranno ad ogni esecuzione. Per ottenere risultati ripetibili, è possibile specificare un seed casuale con l'opzione --seed come ad esempio `--seed 42`.

Per ulteriori opzioni, consultare `--help` (sembra che non ci sia una documentazione completa sui significati dei parametri, quindi potrebbe essere necessario consultare direttamente il codice sorgente).

Di default, i file di didascalia vengono generati con l'estensione ".caption".

![Cartella con didascalie generate](https://user-images.githubusercontent.com/52813779/208908845-48a9d36c-f6ee-4dae-af71-9ab462d1459e.png)

Ad esempio, le didascalie possono essere visualizzate come segue.

![Didascalia e immagine](https://user-images.githubusercontent.com/52813779/208908947-af936957-5d73-4339-b6c8-945a52857373.png)

## Etichettatura tramite DeepDanbooru

Se non si desidera etichettare le immagini con i tag di Danbooru, procedere con la sezione "Preelaborazione delle informazioni sulle didascalie e i tag".

L'etichettatura può essere eseguita con DeepDanbooru o WD14Tagger. WD14Tagger sembra offrire una maggiore precisione. Se si desidera utilizzare WD14Tagger per l'etichettatura, procedere alla sezione successiva.

### Preparazione dell'ambiente

Clonare il repository di DeepDanbooru https://github.com/KichangKim/DeepDanbooru nella cartella di lavoro o scaricare e decomprimere il file zip. Personalmente ho usato il metodo del file zip.

Inoltre, dal sito delle versioni di DeepDanbooru https://github.com/KichangKim/DeepDanbooru/releases, scaricare il file deepdanbooru-v3-20211112-sgd-e28.zip dalla sezione "DeepDanbooru Pretrained Model v3-20211112-sgd-e28" e decomprimerlo nella cartella di DeepDanbooru.

Scaricare il file dalla sezione "Assets" cliccando su "Assets".

![Pagina di download di DeepDanbooru](https://user-images.githubusercontent.com/52813779/208909417-10e597df-7085-41ee-bd06-3e856a1339df.png)

Assicurarsi di avere la seguente struttura delle cartelle.

![Struttura delle cartelle di DeepDanbooru](https://user-images.githubusercontent.com/52813779/208909486-38935d8b-8dc6-43f1-84d3-fef99bc471aa.png)

Installare le librerie necessarie per l'ambiente di Diffusers. Passare alla cartella di DeepDanbooru e installare le librerie (aggiungerà principalmente tensorflow-io).

```
pip install -r requirements.txt
```

Successivamente, installare DeepDanbooru stesso.

```
pip install .
```

A questo punto, l'ambiente per l'etichettatura è pronto.

### Esecuzione dell'etichettatura
Spostarsi nella cartella di DeepDanbooru, eseguire il comando deepdanbooru per avviare l'etichettatura.

```
deepdanbooru evaluate <cartella_dati_di_addestramento> --project-path deepdanbooru-v3-20211112-sgd-e28 --allow-folder --save-txt
```

Se i dati di addestramento sono nella cartella principale "train_data", il comando sarà simile al seguente.

```
deepdanbooru evaluate ../train_data --project-path deepdanbooru-v3-20211112-sgd-e28 --allow-folder --save-txt
```

I file di tag verranno creati nella stessa cartella delle immagini di addestramento con lo stesso nome file e l'estensione ".txt". Poiché il processo è eseguito uno alla volta, potrebbe richiedere del tempo.

Se si dispone di più cartelle di dati di addestramento, eseguire il comando per ciascuna cartella.

I risultati saranno simili a quanto mostrato di seguito.

![File generati da DeepDanbooru](https://user-images.githubusercontent.com/52813779/208909855-d21b9c98-f2d3-4283-8238-5b0e5aad6691.png)

I tag verranno aggiunti alle immagini come mostrato di seguito.

![Tag di DeepDanbooru e immagine](https://user-images.githubusercontent.com/52813779/208909908-a7920174-266e-48d5-aaef-940aba709519.png)

## Tagging con WD14Tagger

Ecco la procedura per utilizzare WD14Tagger al posto di DeepDanbooru.

Utilizzeremo il tagger utilizzato da Automatic1111 nell'interfaccia WebUI. Abbiamo preso spunto da questa pagina GitHub (https://github.com/toriato/stable-diffusion-webui-wd14-tagger#mrsmilingwolfs-model-aka-waifu-diffusion-14-tagger).

### Esecuzione del Tagging

Esegui lo script per effettuare il tagging.
```
python tag_images_by_wd14_tagger.py --batch_size <dimensione_batch> <cartella_dati_di_addestramento>
```

Se hai posizionato i dati di addestramento nella cartella padre train_data, l'esecuzione sarà la seguente.
```
python tag_images_by_wd14_tagger.py --batch_size 4 ..\train_data
```

Al primo avvio, il file del modello verrà scaricato automaticamente nella cartella wd14_tagger_model (è possibile modificare la cartella). L'operazione sarà simile a questa.

![File scaricato](https://user-images.githubusercontent.com/52813779/208910447-f7eb0582-90d6-49d3-a666-2b508c7d1842.png)

Il file dei tag verrà creato nella stessa cartella delle immagini di addestramento, con lo stesso nome file e l'estensione .txt.

![File dei tag generato](https://user-images.githubusercontent.com/52813779/208910534-ea514373-1185-4b7d-9ae3-61eb50bc294e.png)

![Tag e immagine](https://user-images.githubusercontent.com/52813779/208910599-29070c15-7639-474f-b3e4-06bd5a3df29e.png)

Con l'opzione thresh, puoi specificare a quale livello di confidenza dei tag applicare il tagging. Il valore predefinito è 0.35, come nel campione di WD14Tagger. Riducendo il valore, verranno applicati più tag ma la precisione diminuirà.

Modifica la dimensione_batch in base alla capacità della VRAM della GPU. Un valore più alto renderà l'operazione più veloce (anche con una VRAM da 12GB, potresti aumentare leggermente il valore). Con l'opzione caption_extension, puoi modificare l'estensione del file dei tag. Il valore predefinito è .txt.

Con l'opzione model_dir, puoi specificare la cartella di salvataggio del modello.

Se specifici l'opzione force_download, il modello verrà scaricato nuovamente anche se la cartella di destinazione esiste.

Se hai più cartelle di dati di addestramento, esegui lo script per ciascuna di esse.

## Pre-elaborazione delle informazioni di caption e tag

Unisci le informazioni di caption e tag in un unico file di metadati per renderle più facili da elaborare con lo script.

### Pre-elaborazione del caption

Per inserire il caption nei metadati, esegui il seguente comando nella cartella di lavoro (non necessario se non utilizzi il caption per l'addestramento) (in realtà, verrà eseguito in una sola riga, come segue). Specifica l'opzione `--full_path` per memorizzare il percorso completo del file immagine nei metadati. Se ometti questa opzione, verrà registrato il percorso relativo, ma sarà necessario specificare la cartella nel file .toml separatamente.

```
python merge_captions_to_metadata.py --full_path <cartella_dati_di_addestramento>
　  --in_json <nome_file_metadati_da_caricare> <nome_file_metadati>
```

Il nome del file dei metadati è arbitrario.
Se i dati di addestramento sono nella cartella train_data, non hai un file di metadati da caricare e il file di metadati è meta_cap.json, l'esecuzione sarà la seguente.

```
python merge_captions_to_metadata.py --full_path train_data meta_cap.json
```

Con l'opzione caption_extension, puoi specificare l'estensione del caption.

Se hai più cartelle di dati di addestramento, esegui lo script per ciascuna di esse specificando l'argomento full_path.

```
python merge_captions_to_metadata.py --full_path 
    train_data1 meta_cap1.json
python merge_captions_to_metadata.py --full_path --in_json meta_cap1.json 
    train_data2 meta_cap2.json
```

Se ometti in_json, il file di metadati di destinazione verrà sovrascritto con quello letto.

__※È sicuro specificare l'opzione in_json e modificare il file di destinazione per ogni esecuzione, in modo da scrivere su un altro file di metadati.__

### Pre-elaborazione dei tag

Anche i tag vengono raccolti insieme ai metadati (non è necessario eseguire se non si utilizzano i tag per l'apprendimento).
```
python merge_dd_tags_to_metadata.py --full_path <cartella dei dati di addestramento> 
    --in_json <nome del file dei metadati da leggere> <nome del file dei metadati da scrivere>
```

Nello stesso layout della cartella precedente, se si desidera leggere da meta_cap.json e scrivere in meta_cap_dd.json, l'istruzione sarà la seguente.
```
python merge_dd_tags_to_metadata.py --full_path train_data --in_json meta_cap.json meta_cap_dd.json
```

Se si dispone di più cartelle di dati di addestramento, si prega di specificare l'argomento full_path e di eseguire l'istruzione per ciascuna cartella.

```
python merge_dd_tags_to_metadata.py --full_path --in_json meta_cap2.json
    train_data1 meta_cap_dd1.json
python merge_dd_tags_to_metadata.py --full_path --in_json meta_cap_dd1.json 
    train_data2 meta_cap_dd2.json
```

Se si omette in_json, verrà sovrascritto il file dei metadati di destinazione se presente e verrà letto da lì.

__※ Modificare l'opzione in_json e il file di destinazione ogni volta per scrivere su un altro file di metadati è più sicuro.__

### Pulizia delle didascalie e dei tag

Finora le didascalie e i tag di DeepDanbooru sono stati raccolti nel file dei metadati. Tuttavia, le didascalie generate automaticamente possono essere sottoposte a variazioni nella scrittura (※) e i tag possono contenere underscore o rating (nel caso di DeepDanbooru), quindi è consigliabile pulire le didascalie e i tag utilizzando la funzione di sostituzione dell'editor.

È disponibile uno script per la pulizia, si prega di modificarne il contenuto in base alla situazione.

(Non è più necessario specificare la cartella dei dati di addestramento. Verranno puliti tutti i dati presenti nei metadati.)

```
python clean_captions_and_tags.py <nome del file dei metadati da leggere> <nome del file dei metadati da scrivere>
```

--in_json non è incluso, quindi fare attenzione. Ad esempio:

```
python clean_captions_and_tags.py meta_cap_dd.json meta_clean.json
```

Con questo si conclude la pre-elaborazione delle didascalie e dei tag.

## Prelievo preliminare dei latenti

※ Questo passaggio non è obbligatorio. È possibile ometterlo e acquisire i latenti durante l'addestramento.
Inoltre, se si eseguono operazioni come `random_crop` o `color_aug` durante l'addestramento, non è possibile effettuare il prelievo preliminare dei latenti (poiché l'immagine viene modificata ad ogni iterazione). Senza il prelievo preliminare, è possibile addestrare utilizzando i metadati finora.

È possibile acquisire in anticipo la rappresentazione latente delle immagini e salvarle su disco. Ciò consente di accelerare il processo di addestramento. Inoltre, verrà eseguito il bucketing (classificazione dei dati di addestramento in base all'aspect ratio).

Nella cartella di lavoro, inserire il seguente comando:
```
python prepare_buckets_latents.py --full_path <cartella dei dati di addestramento>  
    <nome del file dei metadati da leggere> <nome del file dei metadati da scrivere> 
    <nome del modello o del checkpoint per il fine-tuning> 
    --batch_size <dimensione del batch> 
    --max_resolution <risoluzione massima larghezza,altezza> 
    --mixed_precision <precisione>
```

Se il modello è model.ckpt, il batch size è 4, la risoluzione di addestramento è 512\*512, la precisione è no (float32), e si desidera leggere da meta_clean.json e scrivere in meta_lat.json, l'istruzione sarà la seguente.

```
python prepare_buckets_latents.py --full_path 
    train_data meta_clean.json meta_lat.json model.ckpt 
    --batch_size 4 --max_resolution 512,512 --mixed_precision no
```

I latenti verranno salvati nella cartella dei dati di addestramento in formato npz di numpy.

È possibile specificare la dimensione minima del bucket con l'opzione --min_bucket_reso e la dimensione massima con --max_bucket_reso. I valori predefiniti sono rispettivamente 256 e 1024. Ad esempio, specificando 384 come dimensione minima, non verranno utilizzate risoluzioni come 256\*1024 o 320\*768.
Se si aumenta la risoluzione a 768\*768, è consigliabile specificare 1280 come dimensione massima.

Specificando l'opzione --flip_aug, verrà eseguita l'aumentazione tramite flip orizzontale. Questo consente di raddoppiare virtualmente la quantità di dati, ma se i dati non sono simmetrici rispetto all'asse verticale (ad esempio l'aspetto esteriore di un personaggio, il taglio di capelli, ecc.), l'addestramento potrebbe non funzionare correttamente se specificato. 

(Il salvataggio dei latenti per le immagini flip è un'implementazione semplice che salva i file con il suffisso \_flip.npz. Non è necessario specificare opzioni particolari in fline_tune.py. Se sono presenti file con il suffisso \_flip, il programma caricherà casualmente i file con e senza flip.)

La dimensione del batch potrebbe essere aumentata leggermente anche con 12GB di VRAM.
La risoluzione deve essere un numero divisibile per 64, specificato come "larghezza,altezza". La risoluzione è direttamente correlata alla memoria richiesta durante il fine-tuning. Con 12GB di VRAM, 512\*512 sembra essere il limite (※). Con 16GB, potresti essere in grado di aumentare fino a 512\*704 o 512\*768. Anche se imposti 256\*256, sembra essere difficile con 8GB di VRAM (poiché alcuni parametri come l'ottimizzatore richiedono una certa quantità di memoria indipendentemente dalla risoluzione).

※ C'è stato un report di un funzionamento a 640\*640 con 12GB di VRAM durante l'addestramento con batch size 1.

Di seguito è riportato un esempio di visualizzazione dei risultati del bucketing.

![Risultati del bucketing](https://user-images.githubusercontent.com/52813779/208911419-71c00fbb-2ce6-49d5-89b5-b78d7715e441.png)

Se si dispone di più cartelle di dati di addestramento, si prega di specificare l'argomento full_path e di eseguire l'istruzione per ciascuna cartella.
```
python prepare_buckets_latents.py --full_path  
    train_data1 meta_clean.json meta_lat1.json model.ckpt 
    --batch_size 4 --max_resolution 512,512 --mixed_precision no

python prepare_buckets_latents.py --full_path 
    train_data2 meta_lat1.json meta_lat2.json model.ckpt 
    --batch_size 4 --max_resolution 512,512 --mixed_precision no

```
È possibile specificare la stessa origine e destinazione per la lettura e la scrittura, ma è più sicuro specificare due file separati.

__※ Modificare gli argomenti ogni volta per scrivere su un altro file di metadati è più sicuro.__