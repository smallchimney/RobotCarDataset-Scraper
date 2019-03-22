# os
FROM ubuntu:16.04

# apt
RUN apt-get -y update \
	&& apt-get install -y software-properties-common \
	&& apt-get -y update \
	&& apt-get install -y git python-pip

# pip
RUN git clone -b master https://github.com/matthewgadd/RobotCarDataset-Scraper.git \
    && cd RobotCarDataset-Scraper \
    && pip install -r requirements.txt

# entry point at a working dir
ENTRYPOINT ["/bin/bash"]