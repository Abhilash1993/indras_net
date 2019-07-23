from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.space import Space
from indra.env import Env
from models.bigbox import create_consumer, create_bb, create_mp, set_up
from models.bigbox import calc_util, transaction, town_action, pay_fixed_expenses
from models.bigbox import bb_store, consumer_action, mp_action, bb_action
from models.bigbox import MP_PREF, RADIUS, CONSUMER_INDX
from models.bigbox import BB_INDX, MP_INDX, mp_stores
import models.bigbox as bb

def print_sep():
    print("________________________", flush=True)

class BigBoxTestCase(TestCase):
	def setup(self):
		(bb.town, bb.groups) = set_up()
		pass


	def test_calc_util(self):
		a= create_bb("Big box"+str(0))
		util = bb.calc_util(a)
		self.assertLess(util, 1.0)
		self.assertGreater(util, 0.0)
	

	def test_transaction(self):
		a = create_bb("Big box"+str(0))
		b = create_consumer("Consumer"+str(0))
		spending_power = b.attrs["spending power"]
		bb.transaction(a,b)
		self.assertEqual(a.attrs["capital"],480+spending_power)
		self.assertEqual(a.attrs["inventory"][1], 89)
		a.attrs["inventory"][1]-=87
		bb.transaction(a,b)
		self.assertEqual(a.attrs["inventory"][1], 91)
		self.assertEqual(a.attrs["capital"], 480+2*spending_power-25)
		while a.attrs["capital"] > -1*spending_power:
			bb.pay_fixed_expenses(a)
		bb.transaction(a,b)
		self.assertEqual(a.active, False)


	def test_create_consumer(self):
		bob= create_consumer("Consumer"+str(0))
		self.assertEqual(len(bob.attrs), 3)


	def test_create_mp(self):
		mp= create_mp("books", 0)
		self.assertEqual(len(mp.attrs), 4)


	def test_create_bb(self):
		bigBox = create_bb("Big Box"+str(0))
		self.assertEqual(len(bigBox.attrs), 4)

	
	def test_pay_fixed_expenses(self):
		a = create_bb("Big box"+str(0))
		bb.pay_fixed_expenses(a)
		self.assertEqual(a.attrs["capital"], 420)

	
	def test_mp_action(self):
		mp= create_mp("books", 0)
		self.assertEqual(True, bb.mp_action(mp))


	def test_bb_action(self):
		bigBox= create_bb("Big Box"+str(0))
		self.assertEqual(True, bb.bb_action(bigBox))


	def test_consumer_action(self):
		bob= create_consumer("Consumer"+str(0))
		self.assertEqual(False, bb.consumer_action(bob))





			

