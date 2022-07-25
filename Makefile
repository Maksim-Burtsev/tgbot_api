run:
	python manage.py runserver

mm:
	python manage.py makemigrations && python manage.py migrate 

test:
	python manage.py test