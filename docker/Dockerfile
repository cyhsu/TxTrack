###
# TxTrack: Particle Trajectory Using High Frequency Radar along the Texas Coast.
###


FROM python:3.6.4-slim

#  AuthorWHO
MAINTAINER frankehsu "chsu1@tamu.edu"

ENV APP_USER TxTrack

ENV HOME /home/TxTrack

RUN useradd -d $HOME $APP_USER

#  Optimization
RUN apt-get update && apt-get -y install cron

###  User TxTrack does not exist yet. 
##RUN mkdir -p /home/TxTrack

#  Install Required Packages
COPY ./requirements.txt $HOME/requirements.txt

WORKDIR $HOME

RUN pip3 install -r requirements.txt

# Copy  everything into app directory 
COPY . $HOME/

# Set up Crontab
#COPY cron/TxTrack /var/spool/cron/TxTrack
RUN crontab $HOME/cron/TxTrack

# Set communication port.
EXPOSE 8012

#CMD ["./runTxTrack.sh"]

ENTRYPOINT ["python3"]
CMD ["run.py"]
