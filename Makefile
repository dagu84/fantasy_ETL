install:
	@pip install -r requirements.txt

clean:
	@cd application/packages && rm -rf __pycache__

pull_trigger:
	@cd application && python trigger.py

api_check:
	@cd application/packages && python sleeper_api.py
