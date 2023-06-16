install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

#lint:
#	pylint --disable=R,C hello.py

#format:
#	black *.py

#test:
#	python3 -m pytest -vv test_hello.py