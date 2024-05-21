from .train import LoraTraininginComfy, LoraTraininginComfyAdvanced, TensorboardAccess
from .utils import check_and_install,get_os,read_config, color


#the following dependencies are required in the windows portable version of ComfyUI
check_and_install('toml',reboot=True)
check_and_install('voluptuous')
check_and_install('transformers',"transformers","4.36.2")
if get_os() == "windows":
    check_and_install('bitsandbytes',"bitsandbytes",extra="--index-url https://jihulab.com/api/v4/projects/140618/packages/pypi/simple")
else:
    check_and_install('bitsandbytes')
check_and_install("opencv-python","cv2")
check_and_install("accelerate")

check_and_install("tensorboardX","tensorboardX",reboot=True)
check_and_install("tensorboard","tensorboard",reboot=True)
#check_and_install("wandb")
check_and_install("xformers", extra="--no-deps")
#build diffusers from source
check_and_install('git+https://github.com/huggingface/diffusers.git@ec953047bc0f4a3542e673f3d463543c02505ca5','diffusers')


#check_and_install('torch',desired_version="2.2.1",extra="--index-url https://download.pytorch.org/whl/cu121")
#check_and_install('torchvision',extra="--index-url https://download.pytorch.org/whl/cu121")
#check_and_install('torchaudio',extra="--index-url https://download.pytorch.org/whl/cu121")


print(f"{color.BLUE}{read_config('name')}:{color.END} {color.GREEN}Loaded{color.END}")

NODE_CLASS_MAPPINGS = {"Lora Training in ComfyUI": LoraTraininginComfy, 
                       "Lora Training in Comfy (Advanced)": LoraTraininginComfyAdvanced, 
                       "Tensorboard Access": TensorboardAccess}
NODE_DISPLAY_NAME_MAPPINGS = {}
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']