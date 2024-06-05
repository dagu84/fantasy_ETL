install:
	@pip install -r requirements.txt

clean:
	@cd api_application/packages && rm -rf __pycache__

trigger_api:
	@python manual_trigger_api.py

trigger_scrape:
	@python manual_trigger_scrape.py

api_check:
	@cd api_application/packages && python sleeper_api.py
