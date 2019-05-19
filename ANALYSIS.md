# Docker Image

## Build base php image from alpine image
Instead of using images from

https://hub.docker.com/_/php

create a new Dockerfile for php-fpm, and build it from

https://hub.docker.com/_/alpine

This will increase your control over the docker image build process, and reduce the risk of image tampering on Dockerhub.

It also allows following some security best practices which might not have been applied for the official image.

# Run process with non-root user
A new user should be created, instead of using the root user (which is the default option).
This would reduce the surface of attack in case an application is compromised.

# Database
The database is not production ready.
Replication, automatic failover, and regular backups need to be configured.
A dedicated user should be created for the application instead of using the root user.

# Joomla
The solution was created with the assumption that the application is able to run multiple instances in parallel (i.e. locking resources before modifying them).
If that's not the case, the number of replicas needs to be reduced to 1.

# Kubernetes

## Dynamic Volume Provisioning

Use [dynamic volume provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/) and define one or more [storage classes](https://kubernetes.io/docs/concepts/storage/storage-classes/).

## Monitoring and Logging
Monitor the cluster and the application using Prometheus exporters, and store the data in a Prometheus server.
Collect, filter and strore logs using an ELK stack, or an equivalent solution.

## Autoscaling
Achieve autoscaling by using the [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), or by using a combination of Kubernetes node autoscaling (e.g. AWS autoscaling groups) and [Horizontal Pod Autoscalers](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

## Service Mesh
Using a service mesh such as [Istio](https://istio.io/) will increase the the level of control over the traffic between services, allow encryption out of the box (without modifying existing applications), and offer better observability.