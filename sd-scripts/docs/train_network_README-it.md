#LoRA
LoRA: Adattamento a basso rango dei grandi modelli linguistici (LoRA) è un metodo descritto nel paper [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685), che è stato applicato a Stable Diffusion. Può essere esteso all'utilizzo con Conv2d di dimensione 3x3.

Il contributo di [cloneofsimo](https://github.com/cloneofsimo) ha fornito un punto di partenza significativo, e KohakuBlueleaf ha dimostrato l'efficacia di questa estensione in [LoCon](https://github.com/KohakuBlueleaf/LoCon).

È possibile utilizzare LoRA in due varianti: LoRA-LierLa e LoRA-C3Lier.

1. **LoRA-LierLa**: Applicato a livelli lineari e Conv2d di dimensione 1x1.
2. **LoRA-C3Lier**: Oltre a quanto sopra, esteso anche a Conv2d di dimensione 3x3.

Rispetto a LoRA-LierLa, LoRA-C3Lier offre una maggiore precisione a causa dell'applicazione su più strati.

Per quanto riguarda la formazione, si consiglia di fare riferimento al documento [README per l'addestramento](./train_README-ja.md).

## Procedura di addestramento

### Preparazione dei dati

Per la preparazione dei dati, consulta il documento [Preparazione dei dati di addestramento](./train_README-ja.md).

### Esecuzione dell'addestramento

Utilizza lo script `train_network.py`, specificando l'opzione `--network_module` come `network.lora` per addestrare utilizzando LoRA.

Ecco un esempio di linea di comando:
```
accelerate launch --num_cpu_threads_per_process 1 train_network.py
--pretrained_model_name_or_path=<percorso del modello .ckpt o .safetensor o della directory del modello Diffusers>
--dataset_config=<file .toml creato per la preparazione dei dati>
--output_dir=<directory di output per il modello addestrato>
--output_name=<nome del file per il modello addestrato>
--save_model_as=safetensors
--prior_loss_weight=1.0
--max_train_steps=400
--learning_rate=1e-4
--optimizer_type="AdamW8bit"
--xformers
--mixed_precision="fp16"
--cache_latents
--gradient_checkpointing
--save_every_n_epochs=1
--network_module=networks.lora
```


Questa riga di comando addestrerà LoRA-LierLa.


Il modello LoRA sarà salvato nella cartella specificata dall'opzione `--output_dir`. Per ulteriori opzioni, ottimizzatori, ecc., si prega di fare riferimento alla sezione "Opzioni comuni per l'addestramento" nel [documento di formazione](./train_README-ja.md).

Altre opzioni disponibili includono:

- `--network_dim`: specifica il RANK di LoRA (ad esempio, `--networkdim=4`). Il default è 4. Un numero maggiore aumenta la capacità espressiva ma richiede più memoria e tempo di addestramento. Non è consigliabile aumentare il valore in modo indiscriminato.
- `--network_alpha`: specifica il valore `alpha` per prevenire l'underflow e garantire un addestramento stabile. Il default è 1. Specificare lo stesso valore di `network_dim` comporterà un comportamento simile alle versioni precedenti.
- `--persistent_data_loader_workers`: riduce significativamente il tempo di attesa tra le epoche in ambienti Windows.
- `--max_data_loader_n_workers`: specifica il numero di processi per il caricamento dei dati. Un numero maggiore accelera il caricamento dei dati e utilizza efficientemente la GPU, ma consuma più memoria. Il default è il minimo tra `8` o `CPU simultaneous threads - 1`, quindi, se c'è poco spazio nella memoria principale o l'utilizzo della GPU è superiore al 90%, è consigliabile ridurre questi valori a `2` o `1`.
- `--network_weights`: carica i pesi preaddestrati di LoRA prima dell'addestramento e continua l'addestramento da lì.
- `--network_train_unet_only`: attiva solo i moduli LoRA relativi a U-Net. È utile per l'addestramento fine-tuning.
- `--network_train_text_encoder_only`: attiva solo i moduli LoRA relativi all'encoder di testo. Può produrre effetti simili all'inversione testuale.
- `--unet_lr`: specifica il tasso di apprendimento diverso per i moduli LoRA relativi a U-Net.
- `--text_encoder_lr`: specifica il tasso di apprendimento diverso per i moduli LoRA relativi all'encoder di testo.
- `--network_args`: permette di specificare più argomenti. Vedere di seguito.

Se `--network_train_unet_only` e `--network_train_text_encoder_only` non sono specificati (valore predefinito), entrambi i moduli LoRA relativi all'encoder di testo e a U-Net sono attivi.

## Altri Metodi di Addestramento

### Addestramento di LoRA-C3Lier

Specificare `--network_args` come segue per l'addestramento. Usare `conv_dim` per specificare il RANK di Conv2d (3x3) e `conv_alpha` per specificare alpha.

```
--network_args "conv_dim=4" "conv_alpha=1"
```

Se `alpha` è omesso, verrà utilizzato il valore predefinito di 1.

```
--network_args "conv_dim=4"
```

### DyLoRA

DyLoRA è stato proposto in questo articolo: [DyLoRA: Parameter Efficient Tuning of Pre-trained Models using Dynamic Search-Free Low-Rank Adaptation](https://arxiv.org/abs/2210.07558). L'implementazione ufficiale è disponibile [qui](https://github.com/huawei-noah/KD-NLP/tree/main/DyLoRA).

Secondo l'articolo, un RANK elevato per LoRA non è sempre il migliore; è necessario trovare il RANK appropriato per il modello, il set di dati e il compito specifici. Con DyLoRA, è possibile addestrare contemporaneamente LoRA con vari RANK inferiori a quello specificato. Ciò consente di risparmiare tempo nel trovare il RANK ottimale per ciascuno.

L'implementazione in questo repository estende l'implementazione ufficiale (quindi potrebbero esserci bug).

#### Caratteristiche dell'implementazione DyLoRA in questo repository

I modelli DyLoRA addestrati possono essere compatibili con LoRA e possono estrarre modelli LoRA con diversi RANK dal file del modello DyLoRA.

È possibile addestrare DyLoRA-LierLa e DyLoRA-C3Lier.

#### Addestramento con DyLoRA

Specificare `--network_module=networks.dylora` per utilizzare DyLoRA. Usare `--network_args` per specificare `unit`, ad esempio `--network_args "unit=4"`. `unit` è l'unità di suddivisione del RANK. Ad esempio, `--network_dim=16 --network_args "unit=4"`. Se `unit` non è specificato, viene considerato come `unit=1`.

Esempi di specifica:

```
--network_module=networks.dylora --network_dim=16 --network_args "unit=4"

--network_module=networks.dylora --network_dim=32 --network_alpha=16 --network_args "unit=4"
```

Per DyLoRA-C3Lier, specificare `--network_args` come `"conv_dim=4"`. A differenza di LoRA standard, `conv_dim` deve avere lo stesso valore di `network_dim`.

Esempi di specifica:

```
--network_module=networks.dylora --network_dim=16 --network_args "conv_dim=16" "unit=4"

--network_module=networks.dylora --network_dim=32 --network_alpha=16 --network_args "conv_dim=32" "conv_alpha=16" "unit=8"
```

Con dim=16 e unit=4 (come specificato), è possibile addestrare e estrarre quattro LoRA con RANK di 4, 8, 12 e 16. È possibile confrontare questi modelli per trovare il RANK ottimale.

Le altre opzioni sono simili a LoRA standard.

**Nota:** `unit` è un'estensione personalizzata in questo repository. Per DyLoRA, addestrare con `unit` può richiedere più tempo rispetto a un normale LoRA con lo stesso RANK, quindi `unit` è stato introdotto per ridurre il tempo di addestramento.



### Estrarre un modello LoRA da un modello DyLoRA

Utilizzare lo script `extract_lora_from_dylora.py` nella cartella `networks`. Questo script estrae un modello LoRA da un modello DyLoRA con una certa unità specificata.

Il comando da utilizzare è il seguente:

```powershell
python networks\extract_lora_from_dylora.py --model "percorso_cartella/nome_modello_dylora.safetensors" --save_to "percorso_cartella/nome_modello_dylora-split.safetensors" --unit 4
```

- `--model`: Specifica il percorso del file del modello DyLoRA.
- `--save_to`: Specifica il nome del file in cui salvare il modello estratto (il numero di rank viene aggiunto al nome del file). 
- `--unit`: Specifica l'unità utilizzata durante l'addestramento del modello DyLoRA.

## Tassi di apprendimento a livelli

Per ulteriori dettagli, vedere [PR #355](https://github.com/kohya-ss/sd-scripts/pull/355).

Attualmente, SDXL non è supportato.

È possibile specificare i pesi per i 25 blocchi del modello completo. Anche se il primo blocco corrispondente a LoRA non esiste, viene comunque considerato il 25° blocco per compatibilità con l'applicazione di LoRA a livelli. Inoltre, anche se non si estende a conv2d3x3, specificare sempre 25 valori per uniformità.

Utilizzare `--network_args` per specificare i seguenti argomenti:

- `down_lr_weight`: Specifica i pesi dei tassi di apprendimento per i blocchi down di U-Net. È possibile specificare quanto segue:
  - Pesi per blocco: Specificare 12 valori numerici come `"down_lr_weight=0,0,0,0,0,0,1,1,1,1,1,1"`.
  - Specificare da un preset: Specificare come `"down_lr_weight=sine"`. I valori possibili includono sine, cosine, linear, reverse_linear, zeros. Inoltre, aggiungere `+numero` per aggiungere il numero specificato (ad es. `"down_lr_weight=cosine+.25"`).
- `mid_lr_weight`: Specifica il peso del tasso di apprendimento per i blocchi mid di U-Net. Specificare un solo valore numerico come `"mid_lr_weight=0.5"`.
- `up_lr_weight`: Specifica i pesi dei tassi di apprendimento per i blocchi up di U-Net. Simile a down_lr_weight.
- Le parti non specificate vengono trattate come 1.0. Se il peso è impostato su 0, non viene creato un modulo LoRA per quel blocco.
- `block_lr_zero_threshold`: Se il peso è inferiore o uguale a questo valore, non viene creato un modulo LoRA. Il valore predefinito è 0.

### Esempio di specifica dei tassi di apprendimento a livelli tramite riga di comando:

```powershell
--network_args "down_lr_weight=0.5,0.5,0.5,0.5,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5" "mid_lr_weight=2.0" "up_lr_weight=1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,0.5,0.5,0.5,0.5"

--network_args "block_lr_zero_threshold=0.1" "down_lr_weight=sine+.5" "mid_lr_weight=1.5" "up_lr_weight=cosine+.5"
```

### Esempio di specifica dei tassi di apprendimento a livelli tramite file toml:

```toml
network_args = [ "down_lr_weight=0.5,0.5,0.5,0.5,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5", "mid_lr_weight=2.0", "up_lr_weight=1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,0.5,0.5,0.5,0.5",]

network_args = [ "block_lr_zero_threshold=0.1", "down_lr_weight=sine+.5", "mid_lr_weight=1.5", "up_lr_weight=cosine+.5", ]
```

## Dimensioni (rank) a livelli

È possibile specificare le dimensioni (rank) per i 25 blocchi del modello completo. Anche se alcuni blocchi non hanno LoRA, specificare sempre 25 valori per uniformità.

Utilizzare `--network_args` per specificare i seguenti argomenti:

- `block_dims`: Specifica le dimensioni (rank) per ciascun blocco. Specificare 25 valori come `"block_dims=2,2,2,2,4,4,4,4,6,6,6,6,8,6,6,6,6,4,4,4,4,2,2,2,2"`.
- `block_alphas`: Specifica alpha per ciascun blocco. Specificare 25 valori come block_dims. Se omesso, viene utilizzato il valore di network_alpha.
- `conv_block_dims`: Estende LoRA a conv2d 3x3 e specifica le dimensioni (rank) per ciascun blocco.
- `conv_block_alphas`: Estende LoRA a conv2d 3x3 e specifica alpha per ciascun blocco. Se omesso, viene utilizzato il valore di conv_alpha.

### Esempio di specifica delle dimensioni (rank) a livelli tramite riga di comando:

```powershell
--network_args "block_dims=2,4,4,4,8,8,8,8,12,12,12,12,16,12,12,12,12,8,8,8,8,4,4,4,2"

--network_args "block_dims=2,4,4,4,8,8,8,8,12,12,12,12,16,12,12,12,12,8,8,8,8,4,4,4,2" "conv_block_dims=2,2,2,2,4,4,4,4,6,6,6,6,8,6,6,6,6,4,4,4,4,2,2,2,2"

--network_args "block_dims=2,4,4,4,8,8,8,8,12,12,12,12,16,12,12,12,12,8,8,8,8,4,4,4,2" "block_alphas=2,2,2,2,4,4,4,4,6,6,6,6,8,6,6,6,6,4,4,4,4,2,2,2,2"
```

### Esempio di specifica delle dimensioni (rank) a livelli tramite file toml:

```toml
network_args = [ "block_dims=2,4,4,4,8,8,8,8,12,12,12,12,16,12,12,12,12,8,8,8,8,4,4,4,2",]
  
network_args = [ "block_dims=2,4,4,4,8,8,8,8,12,12,12,12,16,12,12,12,12,8,8,8,8,4,4,4,2", "block_alphas=2,2,2,2,4,4,4,4,6,6,6,6,8,6,6,6,6,4,4,4,4,2,2,2,2",]
```

# Altri script

Script correlati a LoRA come la fusione.

## Script di fusione

Con merge_lora.py, è possibile fondere i risultati di apprendimento di LoRA su un modello Stable Diffusion o fondere più modelli LoRA insieme.

Per SDXL, è disponibile sdxl_merge_lora.py. Le opzioni sono le stesse, quindi sostituire merge_lora.py con sdxl_merge_lora.py.


### Unire un modello LoRA a un modello Stable Diffusion

Dopo la fusione, il modello risultante può essere gestito come un normale ckpt di Stable Diffusion. Ecco un esempio di comando:

```
python networks\merge_lora.py --sd_model ..\model\model.ckpt 
    --save_to ..\lora_train1\model-char1-merged.safetensors 
    --models ..\lora_train1\last.safetensors --ratios 0.8
```

Se si sta addestrando un modello Stable Diffusion v2.x e si desidera unire un modello LoRA, specificare l'opzione --v2.

- `--sd_model`: Specifica il percorso del file del modello Stable Diffusion di partenza (supporta solo .ckpt o .safetensors, non supporta ancora i Diffusers).
- `--save_to`: Specifica il percorso in cui salvare il modello unito (il formato del file viene determinato dall'estensione automaticamente).
- `--models`: Specifica i file dei modelli LoRA addestrati da unire. È possibile specificare più file.
- `--ratios`: Specifica i rapporti di applicazione per ciascun modello. Assicurarsi di specificare un rapporto per ogni modello. 

Quando si specificano più modelli, l'uso è il seguente:

```
python networks\merge_lora.py --sd_model ..\model\model.ckpt 
    --save_to ..\lora_train1\model-char1-merged.safetensors 
    --models ..\lora_train1\last.safetensors ..\lora_train2\last.safetensors --ratios 0.8 0.5
```

### Unire più modelli LoRA

Con l'opzione --concat, è possibile semplicemente concatenare più modelli LoRA per creare un nuovo modello LoRA. Il formato dei file (e quindi le dimensioni/dimensioni) sarà la somma dei modelli LoRA specificati. Per evitare il reverse engineering, si consiglia di utilizzare l'opzione --shuffle per mescolare i pesi.

Ecco un esempio di comando:

```
python networks\merge_lora.py --save_precision bf16 
    --save_to ..\lora_train1\model-char1-style1-merged.safetensors 
    --models ..\lora_train1\last.safetensors ..\lora_train2\last.safetensors 
    --ratios 1.0 -1.0 --concat --shuffle
```

- `--concat`: Specifica l'unione concatenando i modelli LoRA invece di unire i pesi. Assicurarsi di specificare --concat quando si desidera concatenare i modelli LoRA.
- `--shuffle`: Mescola i pesi dei modelli per evitare il reverse engineering.
- Gli altri argomenti sono simili a quelli dell'esempio precedente.

### Fusione di modelli LoRA con dimensioni (rank) diverse

Per unire più modelli LoRA con dimensioni (rank) diverse, utilizzare lo script `svd_merge_lora.py`. Questo script approssima i modelli LoRA multipli in un unico modello LoRA. Ecco un esempio di comando:

```
python networks\svd_merge_lora.py 
    --save_to ..\lora_train1\model-char1-style1-merged.safetensors 
    --models ..\lora_train1\last.safetensors ..\lora_train2\last.safetensors 
    --ratios 0.6 0.4 --new_rank 32 --device cuda
```

- `--new_rank`: Specifica il rank del nuovo modello LoRA creato.
- `--device`: Specifica il dispositivo su cui eseguire i calcoli (ad esempio, cuda per l'utilizzo della GPU).

Assicurarsi di specificare tutti gli argomenti necessari per l'unione dei modelli LoRA con dimensioni (rank) diverse.

## Generazione delle immagini nello script di generazione dell'immagine all'interno del repository

Aggiungi le opzioni --network_module e --network_weights allo script gen_img_diffusers.py. Il significato è lo stesso di quando si esegue il training.

Con l'opzione --network_mul, è possibile specificare un valore compreso tra 0 e 1.0 per regolare il tasso di applicazione di LoRA.

## Generazione nel pipeline di Diffusers

Si prega di fare riferimento all'esempio seguente. L'unico file necessario è networks/lora.py. Si noti che Diffusers potrebbe non funzionare con versioni diverse da 0.10.2.

```python
import torch
from diffusers import StableDiffusionPipeline
from networks.lora import LoRAModule, create_network_from_weights
from safetensors.torch import load_file

# if the ckpt is CompVis based, convert it to Diffusers beforehand with tools/convert_diffusers20_original_sd.py. See --help for more details.

model_id_or_dir = r"model_id_on_hugging_face_or_dir"
device = "cuda"

# create pipe
print(f"creating pipe from {model_id_or_dir}...")
pipe = StableDiffusionPipeline.from_pretrained(model_id_or_dir, revision="fp16", torch_dtype=torch.float16)
pipe = pipe.to(device)
vae = pipe.vae
text_encoder = pipe.text_encoder
unet = pipe.unet

# load lora networks
print(f"loading lora networks...")

lora_path1 = r"lora1.safetensors"
sd = load_file(lora_path1)   # If the file is .ckpt, use torch.load instead.
network1, sd = create_network_from_weights(0.5, None, vae, text_encoder,unet, sd)
network1.apply_to(text_encoder, unet)
network1.load_state_dict(sd)
network1.to(device, dtype=torch.float16)

# # You can merge weights instead of apply_to+load_state_dict. network.set_multiplier does not work
# network.merge_to(text_encoder, unet, sd)

lora_path2 = r"lora2.safetensors"
sd = load_file(lora_path2) 
network2, sd = create_network_from_weights(0.7, None, vae, text_encoder,unet, sd)
network2.apply_to(text_encoder, unet)
network2.load_state_dict(sd)
network2.to(device, dtype=torch.float16)

lora_path3 = r"lora3.safetensors"
sd = load_file(lora_path3)
network3, sd = create_network_from_weights(0.5, None, vae, text_encoder,unet, sd)
network3.apply_to(text_encoder, unet)
network3.load_state_dict(sd)
network3.to(device, dtype=torch.float16)

# prompts
prompt = "masterpiece, best quality, 1girl, in white shirt, looking at viewer"
negative_prompt = "bad quality, worst quality, bad anatomy, bad hands"

# exec pipe
print("generating image...")
with torch.autocast("cuda"):
    image = pipe(prompt, guidance_scale=7.5, negative_prompt=negative_prompt).images[0]

# if not merged, you can use set_multiplier
# network1.set_multiplier(0.8)
# and generate image again...

# save image
image.save(r"by_diffusers..png")
```
## Creazione del modello LoRA dalla differenza di due modelli

Questo è un'implementazione basata su [questa discussione](https://github.com/cloneofsimo/lora/discussions/56). Ho utilizzato le formule direttamente (anche se non le comprendo bene, sembra che facciano uso della decomposizione ai valori singolari).

LoRA approssima la differenza tra due modelli (ad esempio, il modello originale e il modello fine-tuning).

### Modalità di esecuzione dello script

Si prega di specificare come segue:
```
python networks\extract_lora_from_models.py --model_org base-model.ckpt
    --model_tuned fine-tuned-model.ckpt 
    --save_to lora-weights.safetensors --dim 4
```

Con l'opzione --model_org si specifica il modello Stable Diffusion originale. Questo modello verrà utilizzato quando si applica il modello LoRA creato. Può essere specificato come .ckpt o .safetensors.

Con l'opzione --model_tuned si specifica il modello Stable Diffusion da cui estrarre la differenza. Ad esempio, il modello fine-tuning o il modello dopo DreamBooth. Può essere specificato come .ckpt o .safetensors.

Con l'opzione --save_to si specifica il percorso di salvataggio del modello LoRA creato. Con l'opzione --dim si specifica la dimensione di LoRA.

Il modello LoRA generato può essere utilizzato come un modello LoRA addestrato.

Se l'encoder di testo è lo stesso per entrambi i modelli, LoRA sarà solo U-Net LoRA.

### Altre opzioni

- `--v2`
  - Specificare quando si utilizza un modello Stable Diffusion v2.x.
- `--device`
  - Specificare `--device cuda` per eseguire i calcoli sulla GPU, il che aumenterà la velocità di elaborazione (anche se la differenza di velocità tra CPU e GPU potrebbe non essere significativa).
- `--save_precision`
  - Specificare il formato di salvataggio di LoRA tra "float", "fp16", "bf16". Per default è "float".
- `--conv_dim`
  - Specificare per espandere l'area di applicazione di LoRA a Conv2d 3x3. Specificare il rank di Conv2d 3x3.

## Script di ridimensionamento delle immagini

(Documentazione in fase di organizzazione, ma fornisco una breve spiegazione qui.)

Con l'estensione delle funzionalità di Aspect Ratio Bucketing, è ora possibile utilizzare direttamente le immagini più piccole come dati di insegnamento senza ingrandirle. Ho ricevuto uno script di pre-elaborazione insieme a un rapporto che diceva che aggiungere le immagini ridimensionate migliora l'accuratezza. Pertanto, ho integrato e ordinato lo script. Grazie a bmaltais.

### Modalità di esecuzione dello script

Specificare come segue. Le immagini originali e le immagini ridimensionate verranno salvate nella cartella di destinazione. Per le immagini ridimensionate, le dimensioni di destinazione saranno aggiunte al nome del file come ``+512x512`` (diverso dalle dimensioni effettive). Le immagini più piccole della dimensione di destinazione non verranno ingrandite.

```
python tools\resize_images_to_resolution.py --max_resolution 512x512,384x384,256x256 --save_as_png 
    --copy_associated_files cartella_immagini_origine cartella_destinazione
```

Le immagini nella cartella di origine verranno ridimensionate in modo che abbiano la stessa area delle dimensioni specificate (più dimensioni specificate sono possibili). Le immagini saranno salvate nella cartella di destinazione. I file non immagine verranno copiati così come sono.

Con l'opzione ``--max_resolution`` specificare le dimensioni di destinazione come nell'esempio. Le immagini saranno ridimensionate in modo che abbiano quell'area. Se specificate più dimensioni, le immagini saranno ridimensionate in ciascuna dimensione. Ad esempio, con ``512x512,384x384,256x256``, nella cartella di destinazione ci saranno 4 immagini per ogni immagine nell'originale: l'originale e tre ridimensionate.

Con l'opzione ``--save_as_png`` le immagini verranno salvate come file PNG. Se omesso, verranno salvate come file JPEG con qualità 100.

Con l'opzione ``--copy_associated_files`` i file associati (ad es. didascalie) con lo stesso nome dei file immagine verranno copiati nella cartella di destinazione con lo stesso nome dei file immagine.

### Altre opzioni

- divisible_by
  - Le immagini ridimensionate saranno tagliate al centro in modo che le dimensioni risultanti siano divisibili per questo valore.
- interpolation
  - Specificare il metodo di interpolazione durante il ridimensionamento. È possibile scegliere tra "area", "cubic", "lanczos4", con il valore predefinito di "area".

# Informazioni aggiuntive

## Differenze con il repository di cloneofsimo

Alla data del 25/12/2022, questo repository ha ampliato l'applicazione di LoRA a Text Encoder's MLP, U-Net's FFN e Transformer's in/out projection, aumentando così la capacità espressiva. Tuttavia, ciò ha comportato un aumento del consumo di memoria, avvicinandosi al limite di 8 GB.

Inoltre, il meccanismo di scambio dei moduli è completamente diverso.

## Futura espansione

Sarà possibile supportare non solo LoRA ma anche altre estensioni, e queste saranno aggiunte in futuro.
