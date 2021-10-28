# ML Case Study - Predicting Default

# Problem Description

The task is to predict the `probability of default` for the data points in the attached `data/dataset.csv` where
that variable is missing. The solution should contain predictions in a .csv file with two
columns, `uuid` and `pd (probability of default==1)`. Once done, the model should be exposed
with an API endpoint on a cloud provider of your choice.

# Model

A brief overview of the model and solution can be found in this [doc](https://docs.google.com/document/d/17ER3koNmlLpO4ojl0oZ3bNmZaJ5N_i5KHkADelzqn9w/edit?usp=sharing). An overview of how the model was built and evaluated can be found in the `notebooks` directory. 

# Prerequisites

* Docker 
* Docker Compose
* Terraform

# Deployment (AWS)

1. Create ECR repository on AWS

 ```{r, engine='bash', count_lines}
 aws ecr create-repository --repository-name klarna-solution
 ```

2. Set environment variable that points to the ECR registry

 ```{r, engine='bash', count_lines}
 export DOCKER_REGISTRY=xyz.dkr.ecr.eu-central-1.amazonaws.com
 ```

3. Push dockerized project to ECR
 
```{r, engine='bash', count_lines}
$(aws ecr get-login --no-include-email --region eu-central-1)

docker-compose build
docker-compose push
```

4. Set-up the AWS infrastructure with Terraform
 ```{r, engine='bash', count_lines}
terraform init
terraform apply
```

5. Deploy the project on the infrastructure

First, export a variable to which the script will ssh 

```{r, engine='bash', count_lines}
export EC2_MACHINE=xxx.yyy.zzz.qqq
```
Then run the deploy script

 ```{r, engine='bash', count_lines}
bash deploy.sh
```

# Querying the endpoint

To query the endpoint with a randomly selected feature set, simply run:

```{r, engine='bash', count_lines}
python experiments/send_request_for_random_user.py
```