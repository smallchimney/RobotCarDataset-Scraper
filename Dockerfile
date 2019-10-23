# os
FROM ubuntu:18.04

# apt
RUN apt-get -y update \
	&& apt-get install -y software-properties-common \
	&& apt-get -y update \
	&& apt-get install -y git python-pip python3-pip

# pip
COPY requirements.txt /RobotCarDataset-Scraper/
WORKDIR /RobotCarDataset-Scraper
RUN pip3 install -r requirements.txt

# add sources
COPY * /RobotCarDataset-Scraper/

# alias
RUN echo 'alias python=python3' >> /root/.bashrc \
	&& echo 'alias pip=pip3' >> /root/.bashrc

# entry point at a working dir
ENTRYPOINT ["/bin/bash"]
