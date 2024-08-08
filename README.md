# Reproduce comyco results

Using [comyco-lin](https://github.com/godka/comyco-lin) repo to generate results. 

Use the commands below to easily set up virtual envs and requirements without worrying about version issues.

## Setup

Set up conda:

```bash
conda create -n venv_tf2 python=3.7
conda activate venv_tf2
conda init
```

Install dependencies:

```bash
conda install tqdm
conda install tensorflow
pip install tflearn
conda install matplotlib
```

Set up libcore:

```bash
conda install pybind11
cd core
bash build.sh
```

## Run

```bash
conda activate venv_tf2
python train.py
```

```bash
python test.py path_to_your_model
```

```bash
python plot.py
```
