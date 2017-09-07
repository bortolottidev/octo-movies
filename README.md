##	Preparazione ambiente
1.	Seguire le istruzioni presenti al [link](https://weblab.ing.unimore.it/people/canali/teaching/ld_1617/Risoluzione_Problemi_installazione.txt) 
2.	pip install distance


##	Scaricare da github il progetto
1.	cd cartella-dove-scaricare
1.	git clone https://github.com/ifritzord/octo-movies.git LD_Proj

	
##	Visualizzare il progetto
1.	python manage.py runserver
2.	browse 127.0.0.1:8000
3.	Enjoy!


I dati sono già pronti dopo il git pull/clone. 
Se dovete ripristinare il database originale, per un qualsiasi motivo:
1.	python manage.py loaddata db.json


_Ulteriore documentazione presente in doc/progetto_LD.odt._
