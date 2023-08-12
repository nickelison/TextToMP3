SHELL := /usr/bin/env bash
PROJECT_DIR := $(shell dirname "$(shell pwd)")
AWS_PROFILE := texttomp3
APP_NAME := texttomp3
STATIC_S3_BUCKET := texttomp3-django-static
EC2_KEY_NAME := texttomp3
ECR_REPO_URI := 431608762876.dkr.ecr.us-east-1.amazonaws.com
CLUSTER_NAME := $(APP_NAME)-ecs-cluster
SERVICE_NAME := $(APP_NAME)-django-service
ECR_REPO_NAME := $(APP_NAME)-ecr-repo
DB_MIGRATION_TASK_DEF := $(APP_NAME)-django-service-db-upgrade
ENV_FILE := ../.env

include .env.mk

.env.mk: $(ENV_FILE)
	@sed 's/#.*//' $(ENV_FILE) > .env.mk

# COLORS
RED=$(shell echo -e "\033[0;31m")
GRE=$(shell echo -e "\033[0;32m")
NC=$(shell echo -e "\033[0m")

# TERRAFORM INSTALL
version  ?= "1.0.10"
os       ?= $(shell uname|tr A-Z a-z)
ifeq ($(shell uname -m),x86_64)
    arch   ?= "amd64"
endif
ifeq ($(shell uname -m),i686)
    arch   ?= "386"
endif
ifeq ($(shell uname -m),aarch64)
    arch   ?= "arm"
endif

# CHECK TERRAFORM VERSION
TERRAFORM := $(shell command -v terraform 2> /dev/null)
AWS_ACCOUNT_ID := $(shell aws --profile $(AWS_PROFILE) sts get-caller-identity --query "Account" --output text)
REGION := $(shell aws --profile $(AWS_PROFILE) configure get region)

aws-info:
	@echo "$(AWS_ACCOUNT_ID)"
	@echo "$(AWS_ACCESS_KEY_ID)"

deploy-infra:
	@terraform init
	@echo "$(GRE)INFO: Deploying Terraform resources.$(NC)"
	@terraform fmt -recursive && \
	 terraform validate && \
	 terraform apply -auto-approve
	@aws --profile $(AWS_PROFILE) ec2 describe-instances --filters "Name=tag:$(APP_NAME)-ASG,Values=$(APP_NAME)-instance" "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].{PublicDnsName: PublicDnsName, Region: Placement.AvailabilityZone}' --output table

update-infra:
	@echo "$(GRE)INFO: Updating Terraform resources.$(NC)"
	@terraform init -reconfigure && \
     terraform validate && \
     terraform apply -auto-approve

destroy-infra:
	@echo "$(RED)INFO: Removing all Terraform created resources$(NC)"
	@terraform init -reconfigure && \
	 terraform validate && \
	 terraform destroy -auto-approve
	@echo "$(RED)INFO: Removing local build artifacts.$(NC)"
	@rm -rf .terraform* terraform.tfs*

ecr-deploy:
	aws --profile $(AWS_PROFILE) ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(ECR_REPO_URI)
	cd "$(PROJECT_DIR)" && \
	docker buildx build --platform=linux/amd64 --file Dockerfile -t $(ECR_REPO_NAME) --build-arg AWS_ACCESS_KEY_ID="$(AWS_ACCESS_KEY_ID)" --build-arg AWS_SECRET_ACCESS_KEY="$(AWS_SECRET_ACCESS_KEY)" --build-arg AWS_DEFAULT_REGION="$(AWS_DEFAULT_REGION)" . && \
	docker tag $(ECR_REPO_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com/$(ECR_REPO_NAME):latest && \
	docker push $(ECR_REPO_URI)/$(ECR_REPO_NAME):latest

ecr-update:
	aws --profile $(AWS_PROFILE) ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(ECR_REPO_URI)
	cd "$(PROJECT_DIR)" && \
	docker buildx build --platform=linux/amd64 --file Dockerfile -t $(ECR_REPO_NAME) --build-arg AWS_ACCESS_KEY_ID="$(AWS_ACCESS_KEY_ID)" --build-arg AWS_SECRET_ACCESS_KEY="$(AWS_SECRET_ACCESS_KEY)" --build-arg AWS_DEFAULT_REGION="$(AWS_DEFAULT_REGION)" . && \
	docker tag $(ECR_REPO_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com/$(ECR_REPO_NAME):latest && \
	docker push $(ECR_REPO_URI)/$(ECR_REPO_NAME):latest
	@aws --profile $(AWS_PROFILE) ecs update-service --cluster $(CLUSTER_NAME) --service $(SERVICE_NAME) --force-new-deployment --region $(REGION)

update-ssh-config:
	$(eval BASTION_PUBLIC_DNS := $(shell aws --profile $(AWS_PROFILE) ec2 describe-instances --filters 'Name=instance-type,Values=t2.micro' 'Name=key-name,Values=$(EC2_KEY_NAME)' 'Name=availability-zone,Values=us-east-1a' --query 'Reservations[].Instances[].[PublicDnsName]' --output text))
	$(eval INSTANCE_A_PUBLIC_DNS := $(shell aws --profile $(AWS_PROFILE) ec2 describe-instances --filters 'Name=instance-type,Values=t2.small' 'Name=key-name,Values=$(EC2_KEY_NAME)' 'Name=availability-zone,Values=us-east-1a' --query 'Reservations[].Instances[].[PublicDnsName]' --output text))
	$(eval INSTANCE_B_PUBLIC_DNS := $(shell aws --profile $(AWS_PROFILE) ec2 describe-instances --filters 'Name=instance-type,Values=t2.small' 'Name=key-name,Values=$(EC2_KEY_NAME)' 'Name=availability-zone,Values=us-east-1e' --query 'Reservations[].Instances[].[PublicDnsName]' --output text))
	@echo "Updating ~/.ssh/config"
	@sed -i.bak '/^Host $(APP_NAME)-bastion-instance/,+1s/HostName.*/HostName $(BASTION_PUBLIC_DNS)/' ~/.ssh/config
	@sed -i.bak '/^Host $(APP_NAME)-instance-a/,+1s/HostName.*/HostName $(INSTANCE_A_PUBLIC_DNS)/' ~/.ssh/config
	@sed -i.bak '/^Host $(APP_NAME)-instance-b/,+1s/HostName.*/HostName $(INSTANCE_A_PUBLIC_DNS)/' ~/.ssh/config
	@rm -f ~/.ssh/config.bak

apply-db-migration:
	aws --profile $(AWS_PROFILE) ecs run-task --cluster $(CLUSTER_NAME) --task-definition $(DB_MIGRATION_TASK_DEF) --count 1 --launch-type EC2 --placement-constraints "type=memberOf,expression=attribute:ecs.availability-zone == us-east-1a"

upload-static:
	@echo "$(GRE)INFO: Uploading static files to S3.$(NC)"
	@aws s3 sync "$(PROJECT_DIR)/static/" "s3://$(STATIC_S3_BUCKET)/" --exclude "*.DS_Store" --profile $(AWS_PROFILE)