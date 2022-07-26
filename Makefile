run:
	python manage.py runserver

migrate:
	python manage.py makemigrations && python manage.py migrate 

test:
	python manage.py test

req:
	pip freeze > requirements.txt

shell: 
	python manage.py shell