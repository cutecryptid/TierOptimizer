import requests
import re
import os 

API_BASE = 'http://pokeapi.co/api/v2/'
POKE_END = 'pokemon/'

def fetch_name(number):
	pokedata = requests.get(API_BASE+POKE_END+number)
	if pokedata.status_code == 200:
		pokedata = pokedata.json()
		return pokedata['name']
	else:
		return None

for fn in os.listdir('.'):
	if os.path.isfile(fn):
		if re.match('.*\.png', fn):
			pname_form = re.search('([0-9]+)([\-a-z]*)\.png', fn)
			print "Fecth " + pname_form.group(1)
			pname = fetch_name(pname_form.group(1))
			print fn + " >> " + (pname+pname_form.group(2)+'.png')
			os.rename(fn, (pname+pname_form.group(2)+'.png'))


