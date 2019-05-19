#! /bin/bash
set -euo pipefail

pushd ./docker

export JOOMLA_VERSION=$1 && \
  docker build . -t serbangilvitu/demo-joomla:${JOOMLA_VERSION} --build-arg JOOMLA_VERSION=${JOOMLA_VERSION} && \
  docker push serbangilvitu/demo-joomla:${JOOMLA_VERSION}