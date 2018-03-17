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
	url = 'https://www.nytimes.com/'
	if not check_net():
		print('[!] Please check your internet connection.')
		sys.exit(1)
	req = requests.get(url)
	soup = BeautifulSoup(req.text, 'lxml')
	with open('articles.txt', 'w') as f:
		for article in soup.find_all('article'):
			try:
				p = article.h2.a.text.strip('\n').strip(r'^( )+')
				link = article.h2.a['href']
				f.write('~~~~~~> ' + p + ' <~~~~~~\n')
				f.write(link + '\n\n')
			except Exception as e:
				continue
	f.close()
	pwd = os.environ.get('HOME')
	print('[+] articles saved in %s/%s' %(pwd, 'articles.txt'))

if __name__ == '__main__':
	main()