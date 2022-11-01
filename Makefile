
serve:
	env PYTHONPATH=`pwd`/api IMAGE_FOLDER=`pwd`/images flask --app api/main --debug run

run: serve