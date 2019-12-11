# Particle Trajectories using High Frequency Radar

#### Project Structure

	> {'Project short name': 'ParTHdar',
	>  'Funding Source': 'Texas General Land Office', 
	>  'Project PI': 'Steve DiMarco',
	> 	'Project co-PI': 'Kerri Whilden',
	>  'Web Creator': 'Chuan-Yuan Hsu',
	>	'Institute': 'Geochemical and Environmental Research Group - Texas A&M University; Gulf of Mexico Ocean Observing System'}

Docker Folder.  

docker image  
-- Build Docker Images: build_docker.sh  
-- Run Docker Images: run_docker.sh  

ex:
docker run -p 5000:8012 --volume=/dockerized:/home/TxTrack txtrack-flask
