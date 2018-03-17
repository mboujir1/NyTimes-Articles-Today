#!/usr/bin/python3

import requests
import sys, os
from bs4 import BeautifulSoup

def check_net(flag='c'):
	if 'win' in sys.platform.lower():
		flag = 'n'
	cmd = 'ping -{}1 8.8.8.8'.format(flag)
	for line in os.popen(cmd):
		if 'TTL' in line.strip('\n').upper():
			return True
	return False

def main():
	if not check_net():
		print('[!] Please check your internet connection.')
		sys.exit(1)
	url = 'https://www.nytimes.com/'
	req = requests.get(url)
	if int(req.status_code) != 200:
		print('[!] Error')
		sys.exit(1)
	soup = BeautifulSoup(req.text, 'lxml')
	save_path = os.environ.get('HOME') + '/articles.txt'
	with open(save_path, 'w') as f:
		for article in soup.find_all('article'):
			try:
				p = article.h2.a.text.strip('\n').strip(r'^( )+')
				link = article.h2.a['href']
				f.write('~~~~~~> ' + p + ' <~~~~~~\n')
				f.write(link + '\n\n')
			except Exception as e:
				continue
	f.close()
	print('[+] articles saved in %s' %(save_path))

if __name__ == '__main__':
	main()
