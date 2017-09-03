Preparazione ambiente:
>	Seguire le istruzioni presenti al <a href="https://weblab.ing.unimore.it/people/canali/teaching/ld_1617/Risoluzione_Problemi_installazione.txt"> link </a>
>	pip install distance


Scaricare da github il progetto:
>	cd cartella-dove-scaricare
>	git init
>	git remote add origin https://github.com/ifritzord/octo-movies.git
>	git pull origin master
	
	
Visualizzare il progetto:
>	python manage.py runserver
>	browse 127.0.0.1:8000
>	Enjoy!


I dati sono già pronti dopo il git pull. Per ripristinare il database originale, per un qualsiasi motivo:
>	python manage.py loaddata db.json


Ulteriore documentazione presente nella cartella doc (progetto_LD.odt).
