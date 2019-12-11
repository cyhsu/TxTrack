###
# TxTrack: Particle Trajectory Using High Frequency Radar along the Texas Coast.
###


FROM python:3.6.4-slim

#  AuthorWHO
MAINTAINER frankehsu "chsu1@tamu.edu"

#  User TxTrack does not exist yet. 
RUN mkdir -p /home/TxTrack

ENV HOME /home/TxTrack

#  Install Required Packages
COPY ./requirements.txt $HOME/requirements.txt

WORKDIR $HOME

RUN pip3 install -r requirements.txt

# Set up Crontab
COPY cron/TxTrack /var/spool/cron/crontabs/TxTrack

# Copy  everything into app directory 
COPY . $HOME/


# Set communication port.
EXPOSE 8012

ENTRYPOINT ["python3"]

CMD ["run.py"]
