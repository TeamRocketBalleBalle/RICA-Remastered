release: cd backend && flask delete-db && flask create-db && flask fill-testdata
web: gunicorn --bind 0.0.0.0:$PORT --workers=4 "backend:create_app()"
