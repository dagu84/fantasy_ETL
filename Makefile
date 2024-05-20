install:
	@pip install -r requirements.txt

clean:
	@cd packages && rm -rf __pycache__

pull_trigger:
	@python trigger.py

api_check:
	@cd packages && python sleeper_api.py
