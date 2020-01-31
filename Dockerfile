###
# TxTrack: Particle Trajectory Using High Frequency Radar along the Texas Coast.
###
FROM python:3.6.4-slim

#  AuthorWHO
MAINTAINER frankehsu "chsu1@tamu.edu"

ENV HOME /TxTrack

#  Optimization
RUN apt-get update && apt-get -y install cron vim

#  Install Required Packages
COPY ./requirements.txt $HOME/requirements.txt

WORKDIR $HOME

RUN pip3 install -r requirements.txt

# Copy  everything into app directory 
COPY . $HOME/

# Set script permission to execute 
RUN chmod +x $HOME/runTxTrack.sh

# Set communication port.
EXPOSE 8012

#ENTRYPOINT ./runTxTrack.sh
CMD ["./runTxTrack.sh"]
