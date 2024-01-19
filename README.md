
# UPDATE! (19-01-2024)
Introducing an Advanced node and Access Tensorboard node!
Access Tensorboard is a very simple node that launches a URL to see data about the logs created during training. Click the node once (after, during, or even before training!), then copy-paste the URL that it wrote in the command prompt. The logs folder related to Tensorboard is in the same folder as your launcher file.

The Advanced node is full of many recommended features. Some are still missing, but they are here in the code, you just have to change their values manually! Not everything was tested, I personally don't even know what most of these do. Let me know if a certain feature doesn't work like it should!

This node is now confirmed to work with LCMs, SD2.0 and SD Turbo models. I am not able to test for SDXL though.





# Lora-Training-in-Comfy

DISCLAIMER: This is my first "big" custom node. More specifically, it's the first I publish that has a lot of requirements. Therefore, it could conflict with other custom nodes. If it happens, please let me know so I update it accordingly!

This custom node lets you train LoRA directly in ComfyUI! By default, it saves directly in your ComfyUI lora folder. That means you just have to refresh after training (...and select the LoRA) to test it!


Making LoRA has never been easier!

I'll link my tutorial. Download it from here, then follow the guide:

https://www.reddit.com/r/StableDiffusion/comments/193hqkz/lora_training_directly_in_comfyui/

In short, you have to put it in custom_nodes and install the requirements (from requirements_win.txt if you're on Windows). Pretty standard for custom nodes!
![LoRATrainingNode](https://github.com/LarryJane491/Lora-Training-in-Comfy/assets/156431112/ff9453a7-498e-4e26-a2b9-003f9667cbb2)

After installing, you can find it in the LJRE/LORA category or by double-clicking and searching for Training or LoRA.
Make sure you have a folder containing multiple images with captions.
Then, rename that folder into something like [number]_[whatever].
Copy the path of the folder ABOVE the one containing images and paste it in data_path. For example, if it's in C:/database/5_images, data_path MUST be C:/database.
Finally, just choose a name for the LoRA, and change the other values if you want. Then just click Queue Prompt and training starts!

I recommend using it alongside my other custom nodes, LoRA Caption Load and LoRA Caption Save:
![LoraCaption and Training](https://github.com/LarryJane491/Lora-Training-in-Comfy/assets/156431112/bd53593b-88f9-4a69-b4ff-5cad1b40294f)

That way you just have to gather images, then you can do the captioning AND training, all inside Comfy! And since it saves LoRAs in the loras folder of Comfy by default, you just need to refresh and you can test it right away!

Results from the first LoRA I got with my method:

![w62yekl73obc1](https://github.com/LarryJane491/Lora-Training-in-Comfy/assets/156431112/480b5b7b-d6af-4472-a476-8f2fb94dfe0e)
![am585t5h3obc1](https://github.com/LarryJane491/Lora-Training-in-Comfy/assets/156431112/0acad9ef-23c0-490b-a2c0-f65fdfc4f1ad)
![1wacnvrv5obc1](https://github.com/LarryJane491/Lora-Training-in-Comfy/assets/156431112/9fbe23da-fee1-4107-be00-d726bcf9bd07)


You can compare with real images:
https://www.google.com/search?client=opera&hs=eLO&sca_esv=597261711&sxsrf=ACQVn0-1AWaw7YbryEzXe0aIpP_FVzMifw:1704916367322&q=Pokemon+Dawn+Grand+Festival&tbm=isch&source=lnms&sa=X&ved=2ahUKEwiIr8izzNODAxU2RaQEHVtJBrQQ0pQJegQIDRAB&biw=1534&bih=706&dpr=1.25



IMPORTANT NOTES:
This node is confirmed to work for SD 1.5, SD2.0, SDTurbo and LCM.
But I have no idea about SDXL. If someone could test it and confirm or infirm, I’d appreciate ^^. I know the LoRA project included custom scripts for SDXL, so maybe it’s more complicated.

----

TROUBLESHOOT:
The very first version I published online had very strict requirements, which made conflicts likely. I've reduced requirements to the bare minimum, but conflicts can still arise. If that happens to you, please let me know!

"No module X found" : This error happens when Python can't find the required modules for the running program. For ComfyUI, it often happens if you forgot to install requirements for the custom node.
But it can also happen if you installed the requirements in the wrong folder! If your ComfyUI folder has a virtual environment (venv), make sure to enable it before installing requirements.


"Something about cuda.dll missing" : there's a lot of variants of this error, but they're all the same problem (hopefully): it happens if you haven't installed CUDA properly (or, again, if it's not installed in the right folder). Here is what to do in this case:
1) Open a command prompt and make absolutely sure that it's the right environment.
2) Go there: https://pytorch.org and scroll down. Follow the instructions to get a line of code, something like pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121. Copy-paste the line the website gives you into the command prompt you opened and press Enter. This will install CUDA.



I own a Windows 10 machine with a RTX 3060. I can't test for Linux, for MAC, for AMD GPUs and other weird situations x).




----

TO GO FURTHER
Even the Advanced node doens't include all inputs available for LoRA training, but you can find them all in the script train.py! All of that can be modified by the user directly within the script.


----
SHOUTOUT
This is based off an existing project, lora-scripts, available on github. Thanks to the author for making a project that launches training with a single script!

I took that project, got rid of the UI, translated this “launcher script” into Python, and adapted it to ComfyUI. Still took a few hours, but I was seeing the light all the way, it was a breeze thanks to the original project ^^.
