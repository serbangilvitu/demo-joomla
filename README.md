# Dockerfile

## Reference
The Dockerfile is based on https://github.com/joomla/docker-joomla/tree/master/php7.3/fpm-alpine

## What changed from the "official" Dockerfile?

### Base Image
The base image has been changed to php:7.3.5-fpm-alpine3.9 as the tag is more specific and it will offer repeatable builds than php:7.3-fpm-alpine (which is the tag in the original code).

### New Argument
Added a new argument JOOMLA_VERSION
```
ARG JOOMLA_VERSION
```
in order to parametrize the build

## Building a new image
The following command will build the Docker image and push it to Dockerhub.
Note: this assumes you have already successfully authenticated using `docker login`
```
./build.sh <version>
```
Example:
```
./build.sh 3.9.6
```

# Helm configuration

In case Helm/Tiller are already configured, skip this section.
If Tiller is not deployed, it can be started locally (which is in line with the proposal for Helm 3, which aims to remove Tiller)
https://github.com/helm/helm/blob/master/docs/securing_installation.md#running-tiller-locally
```
tiller --storage=configmap
```

In another terminal, export the HELM_HOST variable (can be included in .bashrc to avoid repeating this step)
```
export HELM_HOST=:44134
```


# Database
The database is deployed independently from Joomla
https://github.com/helm/charts/blob/master/stable/mariadb

```
read -s MARIADB_PASSWORD && \
kubectl create secret generic joomla-db --from-literal=mariadb-root-password=${MARIADB_PASSWORD}
```

To verify the content of the secret
```
kubectl get secret --namespace default joomla-db -o jsonpath="{.data.mariadb-root-password}"| base64 --decode
```

Deploy MariaDB using a custom value file
```
helm install stable/mariadb --name joomla-db --version 6.0.1 -f helm/maria-db/values.yaml
```


# Deploying demo-joomla using Helm

Assuming the CD pipeline will inject the environment variable
```
helm install helm/demo-joomla/ --name demo-joomla-$(date +%Y%m%d%H%M%S) --set mariadb.password=${MARIADB_PASSWORD}
```

If the deployment must be triggered manually
```
read -s MARIADB_PASSWORD && \
helm install helm/demo-joomla/ --name demo-joomla-$(date +%Y%m%d%H%M%S) --set mariadb.password=${MARIADB_PASSWORD}
```


# demo-joomla service

Create the service using
```
kubectl apply -f k8s/service.yaml
```

This service is outside of the chart in order to allow blue/green deployments by modifying its selector.

Expose the service locally using port-forward
```
kubectl port-forward svc/demo-joomla  8080:8080
```

# Initial Configuration
When you initially access the application using `localhost:8080` you will be prompted to configure the database connection.
Use `joomla-db-mariadb` for the 'Host Name' (which is the name of the k8s service), and `joomla` as the 'Database Name' field
