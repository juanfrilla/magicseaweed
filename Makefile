install:
	#install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:
	#format code
	black *.py tests/*.py
lint:
	#flake6 or pylint
	pylint --disable=R,C *.py *.py tests/*.py
test:
	python -m pytest -vv --cov=utils tests
build:
	#build container
	docker build -t magicseaweed .
run:
	#run docker
	docker run -p 127.0.0.1:8501:8501 065d9f2d32a70b
deploy:
	#deploy
all: install lint test deploy