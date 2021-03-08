# Nvidia Monitor

In space-constrained GPUs, such as those designed to fit within a server rack, the heat dissipation components (e.g. heatsinks, coolant, fans, etc.) are often suboptimal with respect to the thermal qualities of the GPU chip. Consequently, it is quite easy to physically burn a GPU by letting it run above and beyond its upper thermal limits for extended periods of time. By parsing the output of `nvidia-smi`, an Nvidia-specific GPU status-check tool, we can actively monitor the status of GPU components and automatically warn the user when the GPU exceeds the limitations that we prescribe for it.


## Usage

1. First, ensure that your GPU is recognized by your system and that the target GPU is shown in the output of `nvidia-smi` (note 1).
2. Clone this repository or otherwise download a zip file of the current `main` branch.
3. From within the installed directory, open the `execute.py` script and adjust the `limitations` variable to your ideal trigger settings (note 2). Change the `recipient` variable to your intended notification recipient.
4. Within your cron setup, add the `execute.py` script to run at the interval that you desire.


**Notes**:
1. This version only supports single-GPU systems. However, future updates may extend its ability to parse `nvidia-smi` to more than one GPU.
2. Currently, only the `temperature` limitation is supported. We have no use for notifying the users of fan speed, power usages, etc. at this time.

*Written by Austin Dial. Maintained by Alice Seaborn.*
