# Introduction

This script can be used to perform sequenced downloads of various sensors logs for the robotcar-dataset <https://robotcar-dataset.robots.ox.ac.uk/>.

The code is tested for Python3 on Ubuntu 16.04.

# Getting started

```bash
git clone https://github.com/smallchimney/RobotCarDataset-Scraper.git && cd RobotCarDataset-Scraper
```

In case your python environment is not suitable, maybe docker environment is better:

```bash
docker build -t robotcar-dataset-scraper .
```

# Example usage

If your python environment is suitable, simply execute the script to download the whole dataset:

```bash
python scrape_mrgdatashare.py --downloads_dir PATH_TO_SAVE --datasets_file datasets.csv --username USERNAME --password PASSWORD
```

In docker case, you should mount your downloads dir through the docker image:

```bash
docker run --rm -it -w /RobotCarDataset-Scraper -v $HOME/Downloads:/Downloads robotcar-dataset-scraper:latest
```

In case you don't require all kinds of sensor data, or all the sequences, the script `get_datasets.py` can reproduce the resource file `datasets.csv`:

```bash
python get_datasets.py --sensors SENSOR1 SENSOR2 ... --sequences SEQUENCE_FILE
```

Note that the SEQUENCE_FILE will be find relative with DIR `/Downloads`, which is equals with the DIR `~/Downloads` in your host device.
