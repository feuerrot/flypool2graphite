#!/usr/bin/env python
import graphitesend
import requests

config = {
	'graphite_server': 'localhost',
	'graphite_prefix': 'mining.stats.{}.',
	'miner': [
		'',
	],
	'stats_url': 'https://api-zcash.flypool.org/miner/{}/currentStats'
}

def get_stats(worker):
	r = requests.get(config['stats_url'].format(worker))
	j = r.json()
	return j

def add_worker_data(worker, graphite):
	data = get_stats(worker)
	if data['status'] != 'OK':
		print('[!] Error: status for worker {} not OK:\n    {}'.format(worker, data))
	graphite.send_dict(data['data'])

if __name__ == '__main__':
	for worker in config['miner']:
		graphite = graphitesend.init(
			graphite_server = config['graphite_server'],
			prefix = config['graphite_prefix'].format(worker),
			system_name = ''
		)
		add_worker_data(worker, graphite)
