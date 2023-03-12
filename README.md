# Dining savages problem
This repo is my implementation of fourth assignment for PPDS course at FEI STU.

## What is Feasting savages problem
Community of savages meets every night for a dinner. Savages are eating in companion so everyone has to wait for all savages to arrive first. The last savage to arrive gives a signal and all savages can eat. There is a large pot that can hold M servings of food. When a member of the community wants to eat, they serve themselves from the pot, unless it is empty. If the pot is empty, they wake up the cook and wait until the pot is refilled. Then they can go ahead and take a portion of a meal. Every savage takes one serving. This happens every night, so program has to run indefinitely.

## How to use this project
This project consists of single python script `main.py`. To run this program, you need some prerequisites: 
1. Python 3.10 installed on your system
2. Library `fei.ppds` installed on your system (easiest way is to install globally with `pip install fei.ppds`)

After fulfilling these requirements, you should be able to run this script with command `python main.py` (assuming your shell's working directory is the directory where script is located).
After running the command, the output should be in this format: 
```
SAVAGE: 0 waiting on barrier
SAVAGE: 1 waiting on barrier
SAVAGE: 2 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 4 arrived, barrier unlocking
SAVAGE: 4 waiting on barrier
SAVAGE: 4 took a portion
SAVAGE: 2 took a portion
SAVAGE: 0 took a portion
SAVAGE: 3 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 3 took a portion
SAVAGE: 1 took a portion
SAVAGE: 1 waiting on barrier
SAVAGE: 4 waiting on barrier
SAVAGE: 0 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 2 arrived, barrier unlocking
SAVAGE: 2 waiting on barrier
SAVAGE: 2 took a portion
SAVAGE: 4 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 4 took a portion
SAVAGE: 0 took a portion
SAVAGE: 3 took a portion
SAVAGE: 1 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 1 took a portion
SAVAGE: 1 waiting on barrier
SAVAGE: 4 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 2 waiting on barrier
SAVAGE: 0 arrived, barrier unlocking
SAVAGE: 0 waiting on barrier
SAVAGE: 0 took a portion
SAVAGE: 1 took a portion
SAVAGE: 3 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 3 took a portion
SAVAGE: 4 took a portion
SAVAGE: 2 took a portion
SAVAGE: 2 waiting on barrier
SAVAGE: 0 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 1 waiting on barrier
SAVAGE: 4 arrived, barrier unlocking
SAVAGE: 4 waiting on barrier
SAVAGE: 4 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 4 took a portion
SAVAGE: 3 took a portion
SAVAGE: 0 took a portion
SAVAGE: 2 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 2 took a portion
SAVAGE: 1 took a portion
SAVAGE: 1 waiting on barrier
SAVAGE: 0 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 4 waiting on barrier
SAVAGE: 2 arrived, barrier unlocking
SAVAGE: 2 waiting on barrier
SAVAGE: 2 took a portion
SAVAGE: 4 went to take a portion, but pot is empty, waiting for refill
```

The script runs indefinitely. The number of servings in the pot is equals `SIZE_OF_COOKING_POT` (default is 3). 
The script spawns 5 processes by default, but you can play around with this variable by changing the value of `NUM_OF_SAVAGES`.

## How does this program work