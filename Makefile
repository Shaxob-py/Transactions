mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	python3 manage.py createsuperuser

update:
	python manage.py makemessages -l uz
	python manage.py makemessages -l en

compile:
	python manage.py compilemessages



