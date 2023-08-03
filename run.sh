mlflow models serve -m $ARTIFACT_STORE -h $SERVER_HOST -p $SERVER_PORT --no-conda
exec gunicorn --timeout=60 -b 0.0.0.0:8000 -w 1 ${GUNICORN_CMD_ARGS} -- mlflow.pyfunc.scoring_server.wsgi:app
