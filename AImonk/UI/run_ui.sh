container="ui"
docker stop $container
docker rm $container
docker run -t --name $container -p 5000:5000 -v /home/poo/AImonk/files:/home/files -e ai_ip=$ai_ip aimonk/ui