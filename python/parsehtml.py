# -*- coding: utf-8 -*-

import re
from BeautifulSoup import BeautifulSoup


def prettify_html(html):
	soup = BeautifulSoup(html)
	return soup.prettify()

def parse_html_images(html):
	soup = BeautifulSoup(html)
	urls = []
	num = 1
	for image in soup.findAll('img'):
		try:
			urls.append(image['src'])
			image.replaceWith('[[Image %d: %s]]' % (num, image['src']))
			num += 1
		except:
			pass
	return urls, str(soup)

def parse_html_texts(html):
	return re.sub(r'<[^>]*>', '', html)
