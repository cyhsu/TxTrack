###
# TxTrack: Particle Trajectory Using High Frequency Radar along the Texas Coast.
###


FROM ubuntu:18.04

#  AuthorWHO
MAINTAINER cyhsu

# PORT
EXPOSE 8012

# Optimization
RUN apt-get update && apt-get -y install cron python3-pip


# User TxTrack does not exist yet. 
RUN mkdir -p /home/TxTrack

ENV HOME /home/TxTrack

WORKDIR $HOME

ADD . $HOME/

WORKDIR $HOME/download

###
# Install Requirements.
###
RUN pip3 install requirements.txt


###
# Crontab
###
COPY cron/TxTrack /var/spool/cron/crontabs/TxTrack

##
# Execute Script.
##
CMD ["runTxTrack.sh"]

