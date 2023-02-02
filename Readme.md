## Run in docker container

```
docker pull deadman2099/video_ocr
docker run -d --restart always --env SERVER=https://deadman.sknt.ru --env PREFIX=test deadman2099/video_ocr

# With volume
docker run -d --restart always --env SERVER=https://deadman.sknt.ru --env PREFIX=test -v $(pwd)/download:/usr/src/app/download deadman2099/video_ocr
```


## Run in kubernetes

```
kubectl create namespace video
kubectl apply --namespace=video -f https://raw.githubusercontent.com/deadman2000/video_text/master/Deployment.yaml
```