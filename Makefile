PYTHON = python3

install:
	${PYTHON} -m pip install -r req.txt

serve:
	env PYTHONPATH=`pwd`/api IMAGE_FOLDER=`pwd`/images ${PYTHON} -m flask --app api/main --debug run

run: serve

no run:
	env PYTHONPATH=`pwd`/api IMAGE_FOLDER=`pwd`/images ${PYTHON} -m flask --app api/main run

tester:
	env PYTHONPATH=`pwd`/api ${PYTHON} api/tester.py