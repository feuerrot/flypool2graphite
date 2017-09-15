#!/usr/bin/env python
import graphitesend
import requests

config = {
	'graphite_server': 'localhost',
	'graphite_prefix': 'mining.stats.{}.',
	'miner': [
		'',
	]
}

def get_stats(worker):
	r = requests.get(worker)
	j = r.json()
	return j

def add_worker_data(worker, graphite):
	data = get_stats(worker)
	if data['status'] != 'OK':
		print('[!] Error: status for worker {} not OK:\n    {}'.format(worker, data))
	for elem in data['data']:
		if data['data'][elem] == None:
			data['data'][elem] = 0
		else:
			data['data'][elem] = float(data['data'][elem])
	graphite.send_dict(data['data'])

if __name__ == '__main__':
	for worker in config['miner']:
		graphite = graphitesend.init(
			graphite_server = config['graphite_server'],
			prefix = config['graphite_prefix'].format(
				worker.split('/')[4]
			),
			system_name = ''
		)
		add_worker_data(worker, graphite)
