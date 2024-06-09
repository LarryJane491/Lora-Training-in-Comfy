# Original LoRA train script by @Akegarasu ; rewritten in Python by LJRE.
import subprocess
import os
import folder_paths
import random
from comfy import model_management
import torch

#Train data path | 设置训练用模型、图片
#pretrained_model = "E:\AI-Image\ComfyUI_windows_portable_nvidia_cu121_or_cpu\ComfyUI_windows_portable\ComfyUI\models\checkpoints\MyAnimeModel.ckpt"
is_v2_model = 0 # SD2.0 model | SD2.0模型 2.0模型下 clip_skip 默认无效
parameterization = 0 # parameterization | 参数化 本参数需要和 V2 参数同步使用 实验性功能
#train_data_dir = "" # train dataset path | 训练数据集路径
reg_data_dir = "" # directory for regularization images | 正则化数据集路径，默认不使用正则化图像。

# Network settings | 网络设置
network_module = "networks.lora" # 在这里将会设置训练的网络种类，默认为 networks.lora 也就是 LoRA 训练。如果你想训练 LyCORIS（LoCon、LoHa） 等，则修改这个值为 lycoris.kohya
network_weights = "" # pretrained weights for LoRA network | 若需要从已有的 LoRA 模型上继续训练，请填写 LoRA 模型路径。
network_dim = 32 # network dim | 常用 4~128，不是越大越好
network_alpha = 32 # network alpha | 常用与 network_dim 相同的值或者采用较小的值，如 network_dim的一半 防止下溢。默认值为 1，使用较小的 alpha 需要提升学习率。

# Train related params | 训练相关参数
resolution = "512,512" # image resolution w,h. 图片分辨率，宽,高。支持非正方形，但必须是 64 倍数。
#batch_size = 1 # batch size | batch 大小
#max_train_epoches = 10 # max train epoches | 最大训练 epoch
#save_every_n_epochs = 10 # save every n epochs | 每 N 个 epoch 保存一次

train_unet_only = 0 # train U-Net only | 仅训练 U-Net，开启这个会牺牲效果大幅减少显存使用。6G显存可以开启
train_text_encoder_only = 0 # train Text Encoder only | 仅训练 文本编码器
stop_text_encoder_training = 0 # stop text encoder training | 在第 N 步时停止训练文本编码器

noise_offset = 0 # noise offset | 在训练中添加噪声偏移来改良生成非常暗或者非常亮的图像，如果启用，推荐参数为 0.1
keep_tokens = 0 # keep heading N tokens when shuffling caption tokens | 在随机打乱 tokens 时，保留前 N 个不变。
min_snr_gamma = 0 # minimum signal-to-noise ratio (SNR) value for gamma-ray | 伽马射线事件的最小信噪比（SNR）值  默认为 0

# Learning rate | 学习率
lr = "1e-4" # learning rate | 学习率，在分别设置下方 U-Net 和 文本编码器 的学习率时，该参数失效
unet_lr = "1e-4" # U-Net learning rate | U-Net 学习率
text_encoder_lr = "1e-5" # Text Encoder learning rate | 文本编码器 学习率
lr_scheduler = "cosine_with_restarts" # "linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"
lr_warmup_steps = 0 # warmup steps | 学习率预热步数，lr_scheduler 为 constant 或 adafactor 时该值需要设为0。
lr_restart_cycles = 1 # cosine_with_restarts restart cycles | 余弦退火重启次数，仅在 lr_scheduler 为 cosine_with_restarts 时起效。

# 优化器设置
optimizer_type = "AdamW8bit" # Optimizer type | 优化器类型 默认为 AdamW8bit，可选：AdamW AdamW8bit Lion Lion8bit SGDNesterov SGDNesterov8bit DAdaptation AdaFactor prodigy

# Output settings | 输出设置
#output_name = "Pkmn3GTest" # output model name | 模型保存名称
save_model_as = "safetensors" # model save ext | 模型保存格式 ckpt, pt, safetensors

# Resume training state | 恢复训练设置
save_state = 0 # save training state | 保存训练状态 名称类似于 <output_name>-??????-state ?????? 表示 epoch 数
resume = "" # resume from state | 从某个状态文件夹中恢复训练 需配合上方参数同时使用 由于规范文件限制 epoch 数和全局步数不会保存 即使恢复时它们也从 1 开始 与 network_weights 的具体实现操作并不一致

# 其他设置
min_bucket_reso = 256 # arb min resolution | arb 最小分辨率
max_bucket_reso = 1584 # arb max resolution | arb 最大分辨率
persistent_data_loader_workers = 1 # persistent dataloader workers | 保留加载训练集的worker，减少每个 epoch 之间的停顿
#clip_skip = 2 # clip skip | 玄学 一般用 2
multi_gpu = 0 # multi gpu | 多显卡训练 该参数仅限在显卡数 >= 2 使用
lowram = 0 # lowram mode | 低内存模式 该模式下会将 U-net 文本编码器 VAE 转移到 GPU 显存中 启用该模式可能会对显存有一定影响

# LyCORIS 训练设置
algo = "lora" # LyCORIS network algo | LyCORIS 网络算法 可选 lora、loha、lokr、ia3、dylora。lora即为locon
conv_dim = 4 # conv dim | 类似于 network_dim，推荐为 4
conv_alpha = 4 # conv alpha | 类似于 network_alpha，可以采用与 conv_dim 一致或者更小的值
dropout = "0"  # dropout | dropout 概率, 0 为不使用 dropout, 越大则 dropout 越多，推荐 0~0.5， LoHa/LoKr/(IA)^3 暂时不支持

# 远程记录设置
use_wandb = 0 # enable wandb logging | 启用wandb远程记录功能
wandb_api_key = "" # wandb api key | API，通过 https://wandb.ai/authorize 获取
log_tracker_name = "" # wandb log tracker name | wandb项目名称,留空则为"network_train"


#output_dir = ''
logging_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
log_prefix = ''
mixed_precision = 'fp16'
caption_extension = '.txt'


os.environ['HF_HOME'] = "huggingface"
os.environ['XFORMERS_FORCE_DISABLE_TRITON'] = "1"
ext_args = []
launch_args = []

def GetTrainScript(script_name:str):
    # Current file directory from __file__
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    sd_script_dir = os.path.join(current_file_dir, "sd-scripts")
    train_script_path = os.path.join(sd_script_dir, f"{script_name}.py")
    return train_script_path, sd_script_dir

class LoraTraininginComfy:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            "ckpt_name": (folder_paths.get_filename_list("checkpoints"), ),
            "model_type": (["sd1.5", "sd2.0", "sdxl"], ),
            "resolution_width": ("INT", {"default":512, "step":64}),
            "resolution_height": ("INT", {"default":512, "step":64}),
            #"theseed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            "data_path": ("STRING", {"default": "Insert path of image folders"}),
			"batch_size": ("INT", {"default": 1, "min":1}),
            "max_train_epoches": ("INT", {"default":10, "min":1}),
            "save_every_n_epochs": ("INT", {"default":10, "min":1}),
            #"lr": ("INT": {"default":"1e-4"}),
            #"optimizer_type": ("STRING", {["AdamW8bit", "Lion8bit", "SGDNesterov8bit", "AdaFactor", "prodigy"]}),
            "output_name": ("STRING", {"default":'Desired name for LoRA.'}),
            "clip_skip": ("INT", {"default":2, "min":1}),
            "output_dir": ("STRING", {"default":'models/loras'}),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "loratraining"

    OUTPUT_NODE = True

    CATEGORY = "LJRE/LORA"

    
    def loratraining(self, ckpt_name, resolution_width, resolution_height, model_type, data_path, batch_size, max_train_epoches, save_every_n_epochs, output_name, clip_skip, output_dir):
        #free memory first of all
        loadedmodels=model_management.current_loaded_models
        unloaded_model = False
        for i in range(len(loadedmodels) -1, -1, -1):
            m = loadedmodels.pop(i)
            m.model_unload()
            del m
            unloaded_model = True
        if unloaded_model:
            model_management.soft_empty_cache()
            
        print(model_management.current_loaded_models)
        #loadedmodel = model_management.LoadedModel()
        #loadedmodel.model_unload(self, current_loaded_models)
        #transform backslashes into slashes for user convenience.
        train_data_dir = data_path.replace( "\\", "/")
        if data_path == "Insert path of image folders":
            raise ValueError("Please insert the path of the image folders.")
        if output_name == 'Desired name for LoRA.': 
            raise ValueError("Please insert the desired name for LoRA.")
        #print(train_data_dir)
        train_script_name = "train_network"

        #generates a random seed
        theseed = random.randint(0, 2^32-1)
        
        if multi_gpu:
            launch_args.append("--multi_gpu")

        if lowram:
            ext_args.append("--lowram")

        if model_type == "sd2.0":
            ext_args.append("--v2")
        elif model_type == "sd1.5":
            ext_args.append(f"--clip_skip={clip_skip}")
        elif model_type == "sdxl":
            train_script_name = "sdxl_train_network"
        
        resolution = f"{resolution_width},{resolution_height}"

        if parameterization:
            ext_args.append("--v_parameterization")

        if train_unet_only:
            ext_args.append("--network_train_unet_only")

        if train_text_encoder_only:
            ext_args.append("--network_train_text_encoder_only")

        if network_weights:
            ext_args.append(f"--network_weights={network_weights}")

        if reg_data_dir:
            ext_args.append(f"--reg_data_dir={reg_data_dir}")

        if optimizer_type:
            ext_args.append(f"--optimizer_type={optimizer_type}")

        if optimizer_type == "DAdaptation":
            ext_args.append("--optimizer_args")
            ext_args.append("decouple=True")

        if network_module == "lycoris.kohya":
            ext_args.extend([
                f"--network_args",
                f"conv_dim={conv_dim}",
                f"conv_alpha={conv_alpha}",
                f"algo={algo}",
                f"dropout={dropout}"
            ])

        if noise_offset != 0:
            ext_args.append(f"--noise_offset={noise_offset}")

        if stop_text_encoder_training != 0:
            ext_args.append(f"--stop_text_encoder_training={stop_text_encoder_training}")

        if save_state == 1:
            ext_args.append("--save_state")

        if resume:
            ext_args.append(f"--resume={resume}")

        if min_snr_gamma != 0:
            ext_args.append(f"--min_snr_gamma={min_snr_gamma}")

        if persistent_data_loader_workers:
            ext_args.append("--persistent_data_loader_workers")

        if use_wandb == 1:
            ext_args.append("--log_with=all")
            if wandb_api_key:
                ext_args.append(f"--wandb_api_key={wandb_api_key}")
            if log_tracker_name:
                ext_args.append(f"--log_tracker_name={log_tracker_name}")
        else:
            ext_args.append("--log_with=tensorboard")

        launchargs=' '.join(launch_args)
        extargs=' '.join(ext_args)

        pretrained_model = folder_paths.get_full_path("checkpoints", ckpt_name)
        
        #Looking for the training script.
        progpath = os.getcwd()
        nodespath=''
        sd_script_dir=''
        for dirpath, dirnames, filenames in os.walk(progpath):
             if 'sd-scripts' in dirnames:
               nodespath = dirpath + f'/sd-scripts/{train_script_name}.py'
               sd_script_dir = dirpath + '/sd-scripts'
               print(nodespath)

        nodespath = nodespath.replace( "\\", "/")
        command = "python -m accelerate.commands.launch " + launchargs + f'--num_cpu_threads_per_process=8 "{nodespath}" --enable_bucket --pretrained_model_name_or_path={pretrained_model} --train_data_dir="{train_data_dir}" --output_dir="{output_dir}" --logging_dir="{logging_dir}" --log_prefix={output_name} --resolution={resolution} --network_module={network_module} --max_train_epochs={max_train_epoches} --learning_rate={lr} --unet_lr={unet_lr} --text_encoder_lr={text_encoder_lr} --lr_scheduler={lr_scheduler} --lr_warmup_steps={lr_warmup_steps} --lr_scheduler_num_cycles={lr_restart_cycles} --network_dim={network_dim} --network_alpha={network_alpha} --output_name={output_name} --train_batch_size={batch_size} --save_every_n_epochs={save_every_n_epochs} --mixed_precision="fp16" --save_precision="fp16" --seed={theseed} --cache_latents --prior_loss_weight=1 --max_token_length=225 --caption_extension=".txt" --save_model_as={save_model_as} --min_bucket_reso={min_bucket_reso} --max_bucket_reso={max_bucket_reso} --keep_tokens={keep_tokens} --xformers --shuffle_caption ' + extargs
        #print(command)
        subprocess.run(command, cwd=sd_script_dir)
        print("Train finished")
        #input()
        return ()

class LoraTraininginComfyAdvanced:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
         return {
            "required": {
            "ckpt_name": (folder_paths.get_filename_list("checkpoints"), ),
            "model_type": (["sd1.5", "sd2.0", "sdxl"], ),
            "networkmodule": (["networks.lora", "lycoris.kohya"], ),
            "networkdimension": ("INT", {"default": 32, "min":0}),
            "networkalpha": ("INT", {"default":32, "min":0}),
            "resolution_width": ("INT", {"default":512, "step":64}),
            "resolution_height": ("INT", {"default":512, "step":64}),
            "data_path": ("STRING", {"default": "Insert path of image folders"}),
			"batch_size": ("INT", {"default": 1, "min":1}),
            "max_train_epoches": ("INT", {"default":10, "min":1}),
            "save_every_n_epochs": ("INT", {"default":10, "min":1}),
            "keeptokens": ("INT", {"default":0, "min":0}),
            "minSNRgamma": ("FLOAT", {"default":0, "min":0, "step":0.1}),
            "learningrateText": ("FLOAT", {"default":0.0001, "min":0, "step":0.00001}),
            "learningrateUnet": ("FLOAT", {"default":0.0001, "min":0, "step":0.00001}),
            "learningRateScheduler": (["cosine_with_restarts", "linear", "cosine", "polynomial", "constant", "constant_with_warmup"], ),
            "lrRestartCycles": ("INT", {"default":1, "min":1}),
            "optimizerType": (["AdamW8bit", "Lion8bit", "SGDNesterov8bit", "AdaFactor", "prodigy"], ),
            "output_name": ("STRING", {"default":'Desired name for LoRA.'}),
            "algorithm": (["lora","loha","lokr","ia3","dylora", "locon"], ),
            "networkDropout": ("FLOAT", {"default": 0, "step":0.1}),
            "clip_skip": ("INT", {"default":2, "min":1}),
            "output_dir": ("STRING", {"default":'models/loras'}),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "loratraining"

    OUTPUT_NODE = True

    CATEGORY = "LJRE/LORA"

    def loratraining(self, ckpt_name, model_type, networkmodule, networkdimension, networkalpha, resolution_width, resolution_height, data_path, batch_size, max_train_epoches, save_every_n_epochs, keeptokens, minSNRgamma, learningrateText, learningrateUnet, learningRateScheduler, lrRestartCycles, optimizerType, output_name, algorithm, networkDropout, clip_skip, output_dir):
        #free memory first of all
        loadedmodels=model_management.current_loaded_models
        unloaded_model = False
        for i in range(len(loadedmodels) -1, -1, -1):
            m = loadedmodels.pop(i)
            m.model_unload()
            del m
            unloaded_model = True
        if unloaded_model:
            model_management.soft_empty_cache()
            
        #print(model_management.current_loaded_models)
        #loadedmodel = model_management.LoadedModel()
        #loadedmodel.model_unload(self, current_loaded_models)
        
        #transform backslashes into slashes for user convenience.
        train_data_dir = data_path.replace( "\\", "/")
        if data_path == "Insert path of image folders":
            raise ValueError("Please insert the path of the image folders.")

        if output_name == 'Desired name for LoRA.': 
            raise ValueError("Please insert the desired name for LoRA.")
        
        #ADVANCED parameters initialization
        network_moduke="networks.lora"
        network_dim=32
        network_alpha=32
        resolution = "512,512"
        keep_tokens = 0
        min_snr_gamma = 0
        unet_lr = "1e-4"
        text_encoder_lr = "1e-5"
        lr_scheduler = "cosine_with_restarts"
        lr_restart_cycles = 0
        optimizer_type = "AdamW8bit"
        algo= "lora"
        dropout = 0.0
        train_script_name = "train_network"
        
        if model_type == "sd1.5":
            ext_args.append(f"--clip_skip={clip_skip}")
        elif model_type == "sd2.0":
            ext_args.append("--v2")
        elif model_type == "sdxl":
            train_script_name = "sdxl_train_network"
        
        network_module = networkmodule
        network_dim = networkdimension
        network_alpha = networkalpha
        resolution = f"{resolution_width},{resolution_height}"
        
        formatted_value = str(format(learningrateText, "e")).rstrip('0').rstrip()
        text_encoder_lr = ''.join(c for c in formatted_value if not (c == '0'))
        
        formatted_value2 = str(format(learningrateUnet, "e")).rstrip('0').rstrip()
        unet_lr = ''.join(c for c in formatted_value2 if not (c == '0'))
        
        keep_tokens = keeptokens
        min_snr_gamma = minSNRgamma
        lr_scheduler = learningRateScheduler
        lr_restart_cycles = lrRestartCycles
        optimizer_type = optimizerType
        algo = algorithm
        dropout = f"{networkDropout}"

        #generates a random seed
        theseed = random.randint(0, 2^32-1)
        
        if multi_gpu:
            launch_args.append("--multi_gpu")
        
        if network_module == "lycoris.kohya":
            ext_args.extend([
                f"--network_args",
                f"conv_dim={conv_dim}",
                f"conv_alpha={conv_alpha}",
                f"algo={algo}",
                f"dropout={dropout}"
            ])

        if lowram:
            ext_args.append("--lowram")

        if parameterization:
            ext_args.append("--v_parameterization")

        if train_unet_only:
            ext_args.append("--network_train_unet_only")

        if train_text_encoder_only:
            ext_args.append("--network_train_text_encoder_only")

        if network_weights:
            ext_args.append(f"--network_weights={network_weights}")

        # if reg_data_dir:
        #     ext_args.append(f"--reg_data_dir={reg_data_dir}")

        if optimizer_type:
            ext_args.append(f"--optimizer_type={optimizer_type}")

        if optimizer_type == "DAdaptation":
            ext_args.append("--optimizer_args")
            ext_args.append("decouple=True")

        if network_module == "lycoris.kohya":
            ext_args.extend([
                f"--network_args",
                f"conv_dim={conv_dim}",
                f"conv_alpha={conv_alpha}",
                f"algo={algo}",
                f"dropout={dropout}"
            ])

        if noise_offset != 0:
            ext_args.append(f"--noise_offset={noise_offset}")

        if stop_text_encoder_training != 0:
            ext_args.append(f"--stop_text_encoder_training={stop_text_encoder_training}")

        if save_state == 1:
            ext_args.append("--save_state")

        if resume:
            ext_args.append(f"--resume={resume}")

        if min_snr_gamma != 0:
            ext_args.append(f"--min_snr_gamma={min_snr_gamma}")

        if persistent_data_loader_workers:
            ext_args.append("--persistent_data_loader_workers")

        if use_wandb == 1:
            ext_args.append("--log_with=all")
            if wandb_api_key:
                ext_args.append(f"--wandb_api_key={wandb_api_key}")
            if log_tracker_name:
                ext_args.append(f"--log_tracker_name={log_tracker_name}")
        else:
            ext_args.append("--log_with=tensorboard")

        launchargs=' '.join(launch_args)
        extargs=' '.join(ext_args)

        pretrained_model = folder_paths.get_full_path("checkpoints", ckpt_name)
        
        #Looking for the training script.
        nodespath, sd_script_dir = GetTrainScript(script_name=train_script_name)
        print(nodespath)
        print(sd_script_dir)

        command = f"python -m accelerate.commands.launch " + launchargs + f'--num_cpu_threads_per_process=8 "{nodespath}" --enable_bucket --pretrained_model_name_or_path={pretrained_model} --train_data_dir="{train_data_dir}" --output_dir="{output_dir}" --logging_dir="{logging_dir}" --log_prefix={output_name} --resolution={resolution} --network_module={network_module} --max_train_epochs={max_train_epoches} --learning_rate={lr} --unet_lr={unet_lr} --text_encoder_lr={text_encoder_lr} --lr_scheduler={lr_scheduler} --lr_warmup_steps={lr_warmup_steps} --lr_scheduler_num_cycles={lr_restart_cycles} --network_dim={network_dim} --network_alpha={network_alpha} --output_name={output_name} --train_batch_size={batch_size} --save_every_n_epochs={save_every_n_epochs} --mixed_precision="fp16" --save_precision="fp16" --seed={theseed} --cache_latents --prior_loss_weight=1 --max_token_length=225 --caption_extension=".txt" --save_model_as={save_model_as} --min_bucket_reso={min_bucket_reso} --max_bucket_reso={max_bucket_reso} --keep_tokens={keep_tokens} --xformers --shuffle_caption ' + extargs
        print(command)
        subprocess.run(command, cwd=sd_script_dir)
        print("Train finished")
        #input()
        return ()
        
class TensorboardAccess:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
         return {
            "required": {
           
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "opentensorboard"

    OUTPUT_NODE = True

    CATEGORY = "LJRE/LORA"

    def opentensorboard(self):
        command = f'tensorboard --logdir="{logging_dir}"'
        subprocess.Popen(command, shell=True)
        return()