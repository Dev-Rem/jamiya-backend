#!/bin/zsh

docker tag jamiya-backend-web devrem/jamiya:backend-v3

docker login

docker push devrem/jamiya:backend-v3      

docker tag jamiya-frontend devrem/jamiya:frontend-v3

docker login

docker push devrem/jamiya:frontend-v3      

kubectl apply -f jamiyafx-backend-service.yaml  

kubectl apply -f jamiyafx-backend.yaml     

kubectl apply -f jamiyafx-frontend-service.yaml    

kubectl apply -f jamiyafx-frontend.yaml