#!/bin/bash

set -e

cmds=$(cat <<-END
sudo apt update
sudo apt install -y docker.io awscli
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo $(aws ecr get-login --no-include-email --region eu-central-1)
sudo docker pull ${DOCKER_REGISTRY}
sudo DOCKER_REGISTRY=${DOCKER_REGISTRY} docker-compose up -d train-model
sudo DOCKER_REGISTRY=${DOCKER_REGISTRY} docker-compose up -d klarna-api-production
END
)

ssh $EC2_MACHINE "$cmds"