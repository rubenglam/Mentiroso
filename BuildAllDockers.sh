docker build -t your_dockerhub_username/nodejs-image-demo .

docker images

docker run --name nodejs-image-demo -p 80:8080 -d your_dockerhub_username/nodejs-image-demo

docker ps