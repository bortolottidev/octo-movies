from django.core.exceptions import ObjectDoesNotExist

# Funzione di test:
# testa un istanza e/o un metodo passato su di essa
def objectExist(istance, methodStr):
	try:
		if istance and methodStr:
			getattr(istance, methodStr)
		if istance:
			istance
	except ObjectDoesNotExist:
		return False
	except:
		return False
	return True

def errore (str_errore):
	print(str_errore)
