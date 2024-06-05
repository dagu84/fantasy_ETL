install:
	@pip install -r requirements.txt

clean:
	@cd api_application/packages && rm -rf __pycache__

trigger:
	@python manual_trigger.py

api_check:
	@cd api_application/packages && python sleeper_api.py
