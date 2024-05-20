install:
	pip install -r requirements.txt

clean:
	cd package && rm -rf __pycache__

run:
	python main.py
