#!/usr/bin/python
# coding: utf-8
from django.test import TestCase
from .models import Recensione
from .utility import latestOfficial
import unittest
import math

# Testing della classe recensione
class testRecensione(unittest.TestCase):

	def setUp(self):
		self.rec = Recensione(titolo="RecensioneTest")

	#consistenza architetturale
	def testObj(self):
		self.assertTrue(
			isinstance(self.rec, Recensione), 
			"Errore: rec non è una Recensione"
		)

	#coerenza funzionale: metodi invocabili
	def testMeth(self):
		self.assertTrue(
			callable(self.rec.__str__),
			"rec non ha il metodo __str__"
		)
		self.assertTrue(
			callable(self.rec.__rankUpdate__),
			"rec non ha il metodo __rankUpdate__"
		)
		self.assertTrue(
			callable(self.rec.campi),
			"rec non ha il metodo campi"
		)
		self.assertTrue(
			callable(self.rec.campi_segreti),
			"rec non ha il metodo campi_segreti"
		)
		self.assertTrue(
			callable(self.rec.num_voti),
			"rec non ha il metodo num_voti"
		)
		self.assertTrue(
			callable(self.rec.breve),
			"rec non ha il metodo breve"
		)
		self.assertTrue(
			callable(self.rec.getAutore),
			"rec non ha il metodo getAutore"
		)
		self.assertTrue(
			callable(self.rec.__allRec__),
			"rec non ha il metodo __allRec__"
		)

	#robustezza: input non validi
	# I metodi sono quasi tutti get o comunque in input hanno solo self quindi..
	def testRobustezza(self):
		self.assertRaises(
			TypeError,
			self.rec.breve,
			None
		)
		self.assertRaises(
			TypeError,
			self.rec.breve,
			self.rec,
		)
		self.assertRaises(
			TypeError,
			self.rec.__rankUpdate__,
			None
		)
		self.assertRaises(
			TypeError,
			self.rec.__rankUpdate__,
			self.rec
		)
		self.assertRaises(
			TypeError,
			self.rec.num_voti,
			self.rec
		)
		self.assertRaises(
			TypeError,
			self.rec.num_voti,
			None
		)
		
	#coerenza funzionale: risultati attesi dei metodi
	def testRank(self):
		self.rec.__rankUpdate__()
		self.assertEqual(
			self.rec.rank,
			50,
			"Il rank di rec non è calcolato correttamente"
		)
		
	#coerenza funzionale: risultati attesi dei metodi
	def testvoti(self):
		self.assertEqual(
			self.rec.num_voti(),
			0,
			"Numero dei voti non calcolato correttamente"
		)

	def tearDown(self):
		del self.rec

#class TestUtility:
	
	#def setUp(self):
		#profile
		#found = False
		#found, voto = commentsAnalyzer(profile, recensione, found)
	
	#def tearDown(self):
		#del self.rec

if __name__ == '__main__':
	unittest.main()
