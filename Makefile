#SETUP
install:
	@pip install -r requirements.txt


#CLEANING
clean:
	@cd api_application/packages && rm -rf __pycache__


#CONNECTION
api_check:
	@cd api_application/packages && python sleeper_api.py

scrape_check:
	@cd scrape_application/packages && python scraper.py


#MAIN FILE
trigger_api:
	@python manual_trigger_api.py

trigger_scrape:
	@python manual_trigger_scrape.py


#DOCKER
api_docker:
	@docker buildx build --platform linux/amd64 -f $(DOCKER_FILE) -t $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):0.1 . && docker push $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):0.1

scrape_docker:
	@docker buildx build --platform linux/amd64 -f $(DOCKER_FILE_2) -t $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME_2):0.1 . && docker push $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME_2):0.1
