#### Make a model directory and put all model there

#### To build docker
```
docker build -t awstissue .
docker run awstissue  
docker tag awstissue:latest <>.dkr.ecr.ap-south-1.amazonaws.com/awstissue:latest
docker push <>.dkr.ecr.ap-south-1.amazonaws.com/awstissue:latest
```