# Seq2Seq Spelling Corrector
A simple seq2seq spelling corrector which uses seq2seq based neural network to predict the correct spelling of an incorrect word.The inspiration behind this project was to see the powers of seq2seq.Below is the Neural Net graph for the same.

![graph](/img/graph_raw.png)

Amplified Graph:
![graph](/img/graph_amplified.png)

# Dataset 
The dataset is taken from [here](http://ota.ox.ac.uk/headers/0643.xml) and [here](http://www.dcs.bbk.ac.uk/~ROGER/corpora.html) then self  preprocessed to convert all the files in one format and is present by the name `final_dataset.csv`.

# Usage
```
1. Run main.py to train the model.
2. tensorboard --logdir=/tmp/SpellCorrector
```
