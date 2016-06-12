import Const
import random
import requests
import json
import re

class Type:
	"""Stores individual type data"""
	def __init__(self,name):
		typedata = requests.get(Const.API_BASE+Const.TYPE_END+name)
		typedata = typedata.json()
		self.name = name
		self.damage_relations = typedata['damage_relations']


def fetch_type(name):
	if not(name in Const.TYPE_CATCHE.keys()):
		if Const.CACHE_DEBUG:
			print "Type not cached - " + name
		Const.TYPE_CATCHE[name] = Type(name)
	return Const.TYPE_CATCHE[name]
