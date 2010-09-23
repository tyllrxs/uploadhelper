# -*- coding: utf-8 -*-

import re
from BeautifulSoup import BeautifulSoup


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
	text = re.compile(r'<(script|style).*?</\1>', re.S|re.I).sub('', html)
	return re.sub(r'<[^>]*>', '', text)
