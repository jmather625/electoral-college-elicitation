# FILE?=*_test.py

# VENV_NAME?=./.dp3t_server
# PYTHON_VERSION?=python3.7
# PYTHONPATH=${VENV_NAME}/bin/python

DOCKER_USERNAME?=jmather
CONTAINER_NAME?=electoral-college-elicit-mvp
IMAGE_VERSION?=1.0

NAMESPACE?=ece
DEPLOYMENT_NAME?=ece-mvp

PURPLE_COLOR='\033[1;34m'
NO_COLOR='\033[0m'

.PHONY: local
local:
	docker-compose build
	docker-compose up

# makes docker image and pushes to public registry
.PHONY: docker-image
docker-image:
	docker build -t ${CONTAINER_NAME} -f ./prod.Dockerfile .
	docker tag ${CONTAINER_NAME} ${DOCKER_USERNAME}/${CONTAINER_NAME}:${IMAGE_VERSION}
	docker push ${DOCKER_USERNAME}/${CONTAINER_NAME}:${IMAGE_VERSION}

.PHONY: deploy
deploy:
	@echo "${PURPLE_COLOR} If you have made changes to the server code, run:"
	@echo "${PURPLE_COLOR} make docker-image${NO_COLOR}"
	# deploy
	kubectl apply -f k8s-deploy
	# expose with load balancer
	kubectl -n ${NAMESPACE} expose deployment ${DEPLOYMENT_NAME} --name=${DEPLOYMENT_NAME}-lb --type=LoadBalancer --port 80 --target-port 80
	# autoscaling
	kubectl -n ${NAMESPACE} autoscale deployment ${DEPLOYMENT_NAME} --cpu-percent=80 --min=1 --max=5

.PHONY: deploy-teardown
deploy-teardown:
	kubectl -n ${NAMESPACE} delete -f k8s-deploy
	kubectl -n ${NAMESPACE} delete service ${DEPLOYMENT_NAME}-lb
	kubectl -n ${NAMESPACE} delete hpa ${DEPLOYMENT_NAME}


