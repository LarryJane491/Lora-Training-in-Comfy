# README - Traduzione in Italiano

**Per chi non parla giapponese**: Attualmente questo README è disponibile solo in giapponese. Ci scusiamo per l'inconveniente. Forniremo presto una versione in inglese.

Questa è una spiegazione sui file di configurazione che possono essere passati con `--dataset_config`.

## Panoramica

Passando un file di configurazione, è possibile consentire all'utente di effettuare configurazioni dettagliate.

* È possibile configurare più dataset
    * Ad esempio, è possibile configurare `resolution` per ogni dataset e poi mescolarli per l'addestramento.
    * Con entrambi i metodi di addestramento, sia quello di DreamBooth che quello di fine tuning, è possibile mescolare i dataset dei metodi di DreamBooth e di fine tuning.
* È possibile modificare le impostazioni per ciascun sottoinsieme
    * Un sottoinsieme è costituito da dataset divisi per directory delle immagini o metadati. Alcuni sottoinsiemi costituiscono un dataset.
    * Le opzioni come `keep_tokens` o `flip_aug` possono essere configurate per ogni sottoinsieme. Al contrario, opzioni come `resolution` o `batch_size` possono essere configurate per ogni dataset e avranno lo stesso valore per tutti i sottoinsiemi appartenenti allo stesso dataset. Verrà spiegato più dettagliatamente in seguito.

Il formato del file di configurazione può essere JSON o TOML. Per facilità di scrittura, si consiglia di utilizzare [TOML](https://toml.io/ja/v1.0.0-rc.2). Di seguito, verranno fornite spiegazioni basate su TOML.

Esempio di file di configurazione scritto in TOML:

```toml
[general]
shuffle_caption = true
caption_extension = '.txt'
keep_tokens = 1

# Questo è un dataset di tipo DreamBooth
[[datasets]]
resolution = 512
batch_size = 4
keep_tokens = 2

  [[datasets.subsets]]
  image_dir = 'C:\hoge'
  class_tokens = 'hoge ragazza'
  # Questo sottoinsieme ha keep_tokens = 2 (utilizza il valore del dataset a cui appartiene)

  [[datasets.subsets]]
  image_dir = 'C:\fuga'
  class_tokens = 'fuga ragazzo'
  keep_tokens = 3

  [[datasets.subsets]]
  is_reg = true
  image_dir = 'C:\reg'
  class_tokens = 'umano'
  keep_tokens = 1

# Questo è un dataset di tipo fine tuning
[[datasets]]
resolution = [768, 768]
batch_size = 2

  [[datasets.subsets]]
  image_dir = 'C:\piyo'
  metadata_file = 'C:\piyo\piyo_md.json'
  # Questo sottoinsieme ha keep_tokens = 1 (utilizza il valore di default)
```

In questo esempio, si addestrano tre directory come dataset di DreamBooth a 512x512 (batch size 4) e una directory come dataset di fine tuning a 768x768 (batch size 2).

## Impostazioni del dataset e del sottoinsieme

Le impostazioni del dataset e del sottoinsieme sono divise in diverse sezioni.

* `[general]`
    * Specifica le opzioni applicate a tutti i dataset o a tutti i sottoinsiemi.
    * Se ci sono opzioni con lo stesso nome specificate per il dataset e per il sottoinsieme, le impostazioni del dataset o del sottoinsieme avranno la precedenza.
* `[[datasets]]`
    * Questa è la sezione per specificare le impostazioni del dataset, che si applicano a ciascun dataset.
    * Se ci sono impostazioni specificate per il sottoinsieme, avranno la precedenza.
* `[[datasets.subsets]]`
    * Questa è la sezione per specificare le impostazioni del sottoinsieme, che si applicano a ciascun sottoinsieme.

Ecco un diagramma dell'associazione tra directory delle immagini e registrazioni:

```
C:\
├─ hoge  ->  [[datasets.subsets]] No.1  ┐                        ┐
├─ fuga  ->  [[datasets.subsets]] No.2  |->  [[datasets]] No.1   |->  [general]
├─ reg   ->  [[datasets.subsets]] No.3  ┘                        |
└─ piyo  ->  [[datasets.subsets]] No.4  -->  [[datasets]] No.2   ┘
```

Ogni directory delle immagini corrisponde a un `[[datasets.subsets]]`. Più `[[datasets.subsets]]` formano un singolo `[[datasets]]`. `[general]` include tutte le registrazioni.

Anche se è possibile specificare opzioni diverse per registrazioni diverse, se ci sono opzioni con lo stesso nome, verrà utilizzato il valore dalla registrazione più bassa. Ti consiglio di controllare come l'opzione `keep_tokens` viene gestita nell'esempio di cui sopra per una migliore comprensione.

Inoltre, le opzioni che possono essere specificate dipendono dal metodo di addestramento utilizzato.

* Opzioni esclusive per il metodo DreamBooth
* Opzioni esclusive per il metodo di fine tuning
* Opzioni disponibili quando si utilizza il metodo di dropout delle didascalie

Quando si utilizzano entrambi i metodi di addestramento di DreamBooth e fine tuning, è possibile utilizzare entrambi. Tuttavia, poiché il tipo di metodo (DreamBooth o fine tuning) è determinato per ciascun dataset, non è possibile mescolare sottoinsiemi di entrambi i tipi nello stesso dataset. In altre parole, per utilizzarli entrambi, è necessario assegnare sottoinsiemi di diversi tipi a dataset diversi.

Il programma determina se un sottoinsieme è di tipo fine tuning controllando se esiste l'opzione `metadata_file`. Pertanto, per lo stesso dataset, tutti i sottoinsiemi devono essere dotati di `metadata_file` oppure nessuno di essi.


# Opzioni disponibili

Di seguito sono spiegate le opzioni disponibili. Per le opzioni con lo stesso nome degli argomenti della riga di comando, verrà principalmente omessa la spiegazione. Consultare altri README per ulteriori informazioni.

## Opzioni comuni a tutti i metodi di apprendimento

Opzioni che possono essere specificate indipendentemente dal metodo di apprendimento.

### Opzioni per il dataset

Opzioni relative alla configurazione del dataset. Non possono essere specificate in `datasets.subsets`.

| Nome dell'opzione | Esempio di configurazione | `[general]` | `[[datasets]]` |
| ---- | ---- | ---- | ---- |
| `batch_size` | `1` | o | o |
| `bucket_no_upscale` | `true` | o | o |
| `bucket_reso_steps` | `64` | o | o |
| `enable_bucket` | `true` | o | o |
| `max_bucket_reso` | `1024` | o | o |
| `min_bucket_reso` | `128` | o | o |
| `resolution` | `256`, `[512, 512]` | o | o |

* `batch_size`
    * Equivalente all'argomento della riga di comando `--train_batch_size`.

Queste impostazioni sono fisse per ogni dataset.
In altre parole, i subset del dataset condivideranno queste impostazioni.
Ad esempio, se si desidera preparare dataset con risoluzioni diverse, è possibile definire dataset separati come mostrato negli esempi sopra.

### Opzioni per i subset

Opzioni relative alla configurazione dei subset.

| Nome dell'opzione | Esempio di configurazione | `[general]` | `[[datasets]]` | `[[dataset.subsets]]` |
| ---- | ---- | ---- | ---- | ---- |
| `color_aug` | `false` | o | o | o |
| `face_crop_aug_range` | `[1.0, 3.0]` | o | o | o |
| `flip_aug` | `true` | o | o | o |
| `keep_tokens` | `2` | o | o | o |
| `num_repeats` | `10` | o | o | o |
| `random_crop` | `false` | o | o | o |
| `shuffle_caption` | `true` | o | o | o |
| `caption_prefix` | `“capolavoro, di alta qualità, ”` | o | o | o |
| `caption_suffix` | `“, da parte”` | o | o | o |

* `num_repeats`
    * Specifica il numero di ripetizioni delle immagini nel subset. Corrisponde a `--dataset_repeats` nell'addestramento fine, ma `num_repeats` può essere specificato per qualsiasi metodo di apprendimento.
* `caption_prefix`, `caption_suffix`
    * Specifica i prefissi e i suffissi da aggiungere alle didascalie. La mescolanza avviene con queste stringhe incluse. Fare attenzione quando si specifica `keep_tokens`.

## Opzioni esclusive per il metodo DreamBooth

Le opzioni per il metodo DreamBooth sono presenti solo per i subset.

### Opzioni per i subset

Opzioni relative alla configurazione dei subset del metodo DreamBooth.

| Nome dell'opzione | Esempio di configurazione | `[general]` | `[[datasets]]` | `[[dataset.subsets]]` |
| ---- | ---- | ---- | ---- | ---- |
| `image_dir` | `‘C:\hoge’` | - | - | o (obbligatorio) |
| `caption_extension` | `".txt"` | o | o | o |
| `class_tokens` | `“ragazza sks”` | - | - | o |
| `is_reg` | `false` | - | - | o |

Prima di tutto, si noti che `image_dir` deve contenere il percorso delle immagini direttamente. Nel metodo DreamBooth tradizionale, era necessario inserire le immagini in sottodirectory, ma questo non è compatibile. Inoltre, anche se si usa un nome di cartella come `5_cat`, il numero di ripetizioni delle immagini e il nome della classe non verranno riflessi. Se si desidera configurare questi parametri separatamente, è necessario specificarli esplicitamente con `num_repeats` e `class_tokens`.

* `image_dir`
    * Specifica il percorso della directory delle immagini. Opzione obbligatoria.
    * Le immagini devono essere direttamente nella directory.
* `class_tokens`
    * Imposta i token di classe.
    * Viene utilizzato durante l'addestramento solo se non viene trovato il file di didascalia corrispondente all'immagine. Se non viene specificato `class_tokens` e non viene trovato il file di didascalia, verrà generato un errore.
* `is_reg`
    * Specifica se le immagini nel subset sono per la normalizzazione. Se non specificato, viene trattato come `false`, ovvero immagini non normalizzate.


### Opzioni esclusive per il fine tuning

Le opzioni per il fine tuning sono presenti solo per i subset.

#### Opzioni per i subset

Opzioni relative alla configurazione dei subset del fine tuning.

| Nome dell'opzione | Esempio di configurazione | `[general]` | `[[datasets]]` | `[[dataset.subsets]]` |
| ---- | ---- | ---- | ---- | ---- |
| `image_dir` | `‘C:\hoge’` | - | - | o |
| `metadata_file` | `'C:\piyo\piyo_md.json'` | - | - | o (obbligatorio) |

* `image_dir`
    * Specifica il percorso della directory delle immagini. A differenza del metodo DreamBooth, non è obbligatorio specificarlo, ma è consigliato farlo.
        * Non è necessario specificare in situazioni in cui si esegue la generazione del file metadata con `--full_path`.
    * Le immagini devono essere direttamente nella directory.
* `metadata_file`
    * Specifica il percorso del file metadata utilizzato nel subset. Opzione obbligatoria.
        * Equivalente all'argomento della riga di comando `--in_json`.
    * Poiché è necessario specificare un file metadata separato per ogni subset, è consigliabile evitare di creare un unico file metadata che attraversi le directory. Si consiglia vivamente di preparare un file metadata per ogni directory delle immagini e registrarli come subset separati.

### Opzioni disponibili quando è possibile utilizzare il caption dropout

Le opzioni disponibili quando è possibile utilizzare il caption dropout sono presenti solo per i subset. Queste opzioni sono disponibili per qualsiasi metodo di apprendimento che supporta il caption dropout, indipendentemente dal metodo DreamBooth o dal fine tuning.

#### Opzioni per i subset

Opzioni relative alla configurazione dei subset che supportano il caption dropout.

| Nome dell'opzione | `[general]` | `[[datasets]]` | `[[dataset.subsets]]` |
| ---- | ---- | ---- | ---- |
| `caption_dropout_every_n_epochs` | o | o | o |
| `caption_dropout_rate` | o | o | o |
| `caption_tag_dropout_rate` | o | o | o |

## Comportamento in caso di subset duplicati

Nel caso di dataset DreamBooth, i subset con lo stesso `image_dir` sono considerati duplicati.
Nel caso di dataset fine tuning, i subset con lo stesso `metadata_file` sono considerati duplicati.
Se ci sono subset duplicati all'interno di un dataset, quelli a partire dal secondo vengono ignorati.

Tuttavia, se i subset appartengono a dataset diversi, non sono considerati duplicati.
Ad esempio, se si inseriscono subset con lo stesso `image_dir` in dataset diversi, non sono considerati duplicati.
Questo è utile quando si desidera addestrare con la stessa immagine a risoluzioni diverse.

```toml
# Se si trovano in dataset diversi, non vengono considerati duplicati e vengono entrambi utilizzati per l'addestramento


[[datasets]]
resolution = 512

  [[datasets.subsets]]
  image_dir = 'C:\hoge'

[[datasets]]
resolution = 768

  [[datasets.subsets]]
  image_dir = 'C:\hoge'
```
## Uso con argomenti della riga di comando

Alcuni degli argomenti della riga di comando hanno lo stesso ruolo delle opzioni nel file di configurazione.

I seguenti argomenti della riga di comando verranno ignorati se viene fornito un file di configurazione:

* `--train_data_dir`
* `--reg_data_dir`
* `--in_json`

I seguenti argomenti della riga di comando verranno sovrascritti dalle opzioni nel file di configurazione. Di norma, le opzioni nel file di configurazione avranno la precedenza se non specificato diversamente.

| Argomento della riga di comando | Opzione nel file di configurazione prioritaria |
| ---------------------------------- | ---------------------------------- |
| `--bucket_no_upscale`              |                                    |
| `--bucket_reso_steps`              |                                    |
| `--caption_dropout_every_n_epochs` |                                    |
| `--caption_dropout_rate`           |                                    |
| `--caption_extension`              |                                    |
| `--caption_tag_dropout_rate`       |                                    |
| `--color_aug`                      |                                    |
| `--dataset_repeats`                | `num_repeats`                      |
| `--enable_bucket`                  |                                    |
| `--face_crop_aug_range`            |                                    |
| `--flip_aug`                       |                                    |
| `--keep_tokens`                    |                                    |
| `--min_bucket_reso`                |                                    |
| `--random_crop`                    |                                    |
| `--resolution`                     |                                    |
| `--shuffle_caption`                |                                    |
| `--train_batch_size`               | `batch_size`                       |

## Guida agli errori

Attualmente, stiamo utilizzando una libreria esterna per controllare la correttezza della sintassi del file di configurazione, ma la manutenzione è carente e ci sono problemi con i messaggi di errore poco chiari.

Come soluzione temporanea, forniremo una guida per gli errori più comuni e le relative soluzioni.
Se ricevi un errore anche se pensi che il file di configurazione sia corretto, potrebbe essere un bug. Ti preghiamo di contattarci.

* `voluptuous.error.MultipleInvalid: required key not provided @ ...`: Questo errore indica che una chiave richiesta non è stata fornita. Potresti aver dimenticato di specificare un'opzione o potresti aver scritto il nome dell'opzione in modo errato.
  * Il percorso `...` indicherà dove si trova il problema. Ad esempio, se ricevi un errore come `voluptuous.error.MultipleInvalid: required key not provided @ data['datasets'][0]['subsets'][0]['image_dir']`, significa che `image_dir` non è stato fornito nella posizione 0 di `subsets` del primo elemento di `datasets`.
* `voluptuous.error.MultipleInvalid: expected int for dictionary value @ ...`: Questo errore indica che il formato del valore specificato non è corretto. Potrebbe essere dovuto a un formato errato. Il tipo di dato (`int`) varia a seconda dell'opzione. Gli esempi di configurazione forniti in questo README potrebbero essere utili.
* `voluptuous.error.MultipleInvalid: extra keys not allowed @ ...`: Questo errore si verifica quando vengono fornite opzioni non supportate. Potrebbe essere dovuto a un errore di digitazione o a opzioni errate incluse per errore.
