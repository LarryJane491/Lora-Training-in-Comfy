# Fine-tuning
#### Metodo di addestramento proposto da NovelAI, che supporta il fine-tuning per il metodo di apprendimento, la sottotitolazione automatica, l'etichettatura e l'ambiente con Windows + VRAM da 12 GB (nel caso di SD v1.x). Qui, il fine-tuning si riferisce all'addestramento del modello su immagini e didascalie (non include LoRA, Textual Inversion, Hypernetworks).

Si prega di consultare anche il [documento comune sull'addestramento](./train_README-ja.md).

# Panoramica

Si esegue il fine-tuning della Stable Diffusion U-Net utilizzando i Diffusers. Questo è compatibile con i miglioramenti segnalati nell'articolo di NovelAI, inclusi:

- Utilizzo dell'output del penultimo strato di CLIP (Text Encoder) anziché dell'ultimo strato.
- Addestramento a risoluzioni non quadrate (Bucketing del rapporto d'aspetto).
- Estensione della lunghezza del token da 75 a 225.
- Sottotitolazione tramite BLIP, etichettatura automatica tramite DeepDanbooru o WD14Tagger.
- Supporto per l'addestramento dell'Hypernetwork.
- Compatibilità con Stable Diffusion v2.0 (base e 768/v).
- Prelievo dell'output del VAE in anticipo e salvataggio su disco per una maggiore efficienza e velocità nell'addestramento.

Di default, non si addestra il Text Encoder. È comune addestrare solo la U-Net nell'intero modello (come sembra fare anche NovelAI). È possibile specificare l'addestramento del Text Encoder tramite opzioni.

# Funzionalità aggiuntive

## Modifica dell'output di CLIP

Per riflettere il prompt sull'immagine, si utilizza CLIP (Text Encoder) per convertire le caratteristiche del testo. Mentre Stable Diffusion utilizza l'output dell'ultimo strato di CLIP, è possibile modificare ciò per utilizzare l'output del penultimo strato. Secondo NovelAI, questo migliorerebbe la riflessione più accurata del prompt.

## Addestramento a risoluzioni non quadrate

Sebbene Stable Diffusion sia addestrato a 512x512, viene addestrato anche a risoluzioni come 256x1024 o 384x640. Ciò riduce le parti ritagliate e ci si aspetta una migliore comprensione della relazione tra prompt e immagine. La risoluzione di addestramento è regolata per non superare l'area specificata come parametro, regolando la dimensione verticalmente e orizzontalmente in incrementi di 64 pixel.

## Estensione della lunghezza del token a 225

Mentre Stable Diffusion è limitato a 75 token (77 contando l'inizio e la fine), viene esteso fino a 225 token. Tuttavia, poiché CLIP accetta un massimo di 75 token, per 225 token i risultati sono concatenati dopo la chiamata a CLIP.

# Procedura di addestramento

Si prega di fare riferimento alla README di questo repository per la preparazione dell'ambiente.

## Preparazione dei dati

Si prega di fare riferimento a [Preparazione dei dati di addestramento](./train_README-ja.md). Solo il metodo di fine tuning che utilizza i metadati è supportato.

## Esecuzione dell'addestramento

Ad esempio, l'addestramento può essere avviato come segue. Le seguenti righe sono impostate per la minimizzazione della memoria. Si prega di modificare di conseguenza ogni riga se necessario.
```
accelerate launch --num_cpu_threads_per_process 1 fine_tune.py
--pretrained_model_name_or_path=<.ckpt o .safetensor o directory del modello Diffusers>
--output_dir=<cartella di output del modello addestrato>
--output_name=<nome del file di output del modello addestrato>
--dataset_config=<file .toml creato durante la preparazione dei dati>
--save_model_as=safetensors
--learning_rate=5e-6 --max_train_steps=10000
--use_8bit_adam --xformers --gradient_checkpointing
--mixed_precision=fp16
```


Si consiglia di impostare `num_cpu_threads_per_process` su 1.

Impostare `pretrained_model_name_or_path` sul modello di partenza per l'addestramento aggiuntivo. Possono essere specificati file di checkpoint di Stable Diffusion (.ckpt o .safetensors), una directory del modello locale di Diffusers o l'ID del modello di Diffusers ("stabilityai/stable-diffusion-2" ecc.).

Impostare `output_dir` sulla cartella in cui salvare il modello addestrato. Impostare `output_name` sul nome del file del modello senza estensione. Impostare `save_model_as` per salvare il modello in formato safetensors.

Impostare `dataset_config` su un file .toml. Inizialmente, impostare la dimensione del batch a `1` per ridurre il consumo di memoria.

Il numero di passaggi di addestramento `max_train_steps` è impostato su 10000. Il tasso di apprendimento `learning_rate` è impostato su 5e-6.

Per la minimizzazione della memoria, impostare `mixed_precision="fp16"` (per RTX30 Serie o successiva, è possibile impostare anche `bf16`). Impostare anche `gradient_checkpointing`.

Per ottimizzare l'uso della memoria utilizzando 8bit AdamW come ottimizzatore per adattare il modello ai dati di addestramento, specifica `optimizer_type="AdamW8bit"`.

Se hai installato `xformers`, puoi utilizzare l'opzione `xformers` e utilizzare CrossAttention da xformers. Se non hai installato xformers o incontri un errore (ad esempio, con `mixed_precision="no"`), puoi specificare l'opzione `mem_eff_attn` per utilizzare una versione a basso consumo di memoria di CrossAttention (anche se più lenta).

Se hai abbastanza memoria a disposizione, considera di aumentare le dimensioni del batch a, ad esempio, `4` modificando il file `.toml` (potenzialmente migliorando la velocità e la precisione).

### Opzioni Comuni

Per informazioni dettagliate sulle opzioni, consulta la documentazione nei seguenti casi:

- Se stai addestrando un modello Stable Diffusion 2.x o derivato.
- Se stai addestrando un modello che richiede un clip skip superiore a 2.
- Se stai addestrando con didascalie di più di 75 token.

### Dimensioni del Batch

Il consumo di memoria è maggiore rispetto all'addestramento di modelli come LoRA, quindi è necessario prestare attenzione alle dimensioni del batch (simile a DreamBooth).

### Tasso di Apprendimento

Un tasso di apprendimento compreso tra 1e-6 e 5e-6 sembra essere comune. Puoi anche fare riferimento ad altri esempi di fine-tuning.

### Comandi per Dati di Formato Precedente

Se stai utilizzando specifiche di dataset in formato precedente, specifica le dimensioni della batch e altre opzioni tramite la riga di comando, ad esempio:

```
accelerate launch --num_cpu_threads_per_process 1 fine_tune.py
--pretrained_model_name_or_path=model.ckpt
--in_json meta_lat.json
--train_data_dir=train_data
--output_dir=fine_tuned
--shuffle_caption
--train_batch_size=1 --learning_rate=5e-6 --max_train_steps=10000
--use_8bit_adam --xformers --gradient_checkpointing
--mixed_precision=bf16
--save_every_n_epochs=4
```

## Altre Opzioni Specifiche per il Fine-Tuning

Per ulteriori dettagli su tutte le opzioni, consulta la documentazione specifica.

### `train_text_encoder`
Specifica se addestrare anche il Text Encoder. Questo può aumentare leggermente il consumo di memoria.

Di solito il Text Encoder non viene addestrato durante il fine-tuning, ma in alcuni casi, come con DreamBooth, può essere utile addestrare anche il Text Encoder per migliorare le prestazioni.

### `diffusers_xformers`
Specifica se utilizzare le funzionalità xformers di Diffusers anziché le funzionalità xformers native dello script. Tuttavia, non sarà possibile addestrare l'hypernetwork con questa opzione.


