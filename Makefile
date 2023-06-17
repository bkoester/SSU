install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C make_data.py

#format:
#	black *.py

test:
	python -m pytest -s test_create.py 