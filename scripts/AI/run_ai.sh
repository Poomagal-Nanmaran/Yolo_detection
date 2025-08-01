container="ai"
docker stop $container
docker rm $container
docker run -it --name $container -v /home/poo/AImonk/files/:/home/files/ -p 8000:8000 aimonk/ai
