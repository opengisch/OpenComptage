FROM ubuntu:18.04
MAINTAINER Mario Baranzini <mario@opengis.ch>

# install add-apt-repository command
RUN apt-get update
RUN apt-get -y install software-properties-common wget

# Add public key
RUN wget -O - https://qgis.org/downloads/qgis-2017.gpg.key | gpg --import
RUN gpg --fingerprint CAEB3DC3BDF7FB45
RUN gpg --export --armor CAEB3DC3BDF7FB45 | apt-key add -

# Add qgis repostory
RUN add-apt-repository "deb     https://qgis.org/debian bionic main"

# Install tzdata noninteractively
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN ln -fs /usr/share/zoneinfo/Europe/Zurich /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

# Install QGIS, xvfb and imagemagick
RUN apt-get update && apt-get -y install qgis python-qgis qgis-plugin-grass xvfb imagemagick

# Copy script to run the test
ADD .docker/run_test.sh /run_test.sh
RUN chmod +x /run_test.sh

RUN mkdir /tests
RUN chmod 777 /tests