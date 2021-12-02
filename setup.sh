#!/usr/bin/env bash

# instal python
apt-get install -y python3 python3-pip python3-dev

# instal needed dependencies
pip3 install -r /autograder/source/requirements.txt

# Get Java17
# install the necessary dependencies
apt-get -q update
apt-get -yq install gnupg curl 

# add Azul's public key
apt-key adv \
  --keyserver hkp://keyserver.ubuntu.com:80 \
  --recv-keys 0xB1998361219BD9C9

# download and install the package that adds 
# the Azul APT repository to the list of sources 
curl -O https://cdn.azul.com/zulu/bin/zulu-repo_1.0.0-3_all.deb

# install the package
apt-get install ./zulu-repo_1.0.0-3_all.deb

# update the package sources
apt-get update

# install Azul Zulu JDK 17, push through any yes/no prompts
echo Y | apt-get install zulu17-jdk

# Make sure java installed correctly
java -version

# Make run_autograder an executable file
chmod u+x /autograder/source/run_autograder
