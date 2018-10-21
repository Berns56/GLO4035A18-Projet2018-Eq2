docker stop MyApp
docker stop AppProf
docker container prune -f
docker build -t applicationglo4035 . 
docker create -i -p 80:80 --network="MonReaseauApp" --name MyApp applicationglo4035
docker create -i -p 5000:5000 --network "MonReaseauApp" --name AppProf jtbai/glo4035-data-server
docker start AppProf
docker start -i MyApp