serve:
	env PYTHONPATH=api IMAGE_FOLDER=`pwd`/images python3 api/main.py

debug:
	env PYTHONPATH=api IMAGE_FOLDER=`pwd`/images uvicorn --host 127.0.0.1 --port 5000 --interface asgi3 --debug --reload --workers 4 api.main:app
