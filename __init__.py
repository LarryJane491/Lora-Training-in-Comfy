from .train import LoraTraininginComfy, LoraTraininginComfyAdvanced, TensorboardAccess
NODE_CLASS_MAPPINGS = {"Lora Training in ComfyUI": LoraTraininginComfy, "Lora Training in Comfy (Advanced)": LoraTraininginComfyAdvanced, "Tensorboard Access": TensorboardAccess}
NODE_DISPLAY_NAME_MAPPINGS = {}
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']