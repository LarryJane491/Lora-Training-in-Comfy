from .train import LoraTraininginComfy, LoraTraininginComfyAdvanced, TensorboardAccess
from .utils import check_and_install

check_and_install('toml',reboot=True)
check_and_install('voluptuous')
check_and_install('transformers',"transformers","4.30.2")
check_and_install('bitsandbytes',"bitsandbytes",extra="--index-url https://jihulab.com/api/v4/projects/140618/packages/pypi/simple")
check_and_install("opencv-python","cv2") 

NODE_CLASS_MAPPINGS = {"Lora Training in ComfyUI": LoraTraininginComfy, "Lora Training in Comfy (Advanced)": LoraTraininginComfyAdvanced, "Tensorboard Access": TensorboardAccess}
NODE_DISPLAY_NAME_MAPPINGS = {}
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']