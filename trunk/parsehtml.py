# -*- coding: utf-8 -*-

import re
import HTMLParser
from BeautifulSoup import BeautifulSoup

def prettify_html(html):
        soup = BeautifulSoup(html)
        return soup.prettify()

def parse_html_images(html):
	soup = BeautifulSoup(html)
	urls = []
	image_tags = ('real_src', 'src')
	num = 1
	for image in soup.findAll('img'):
		for tag in image_tags:
			if image.has_key(tag):
				urls.append(image[tag])
				image.replaceWith('[[Image %d: %s]]' % (num, image[tag]))
				num += 1
				break
	return urls, str(soup)

def parse_html_texts(html):
	text = re.compile(r'<(script|style).*?</\1>', re.S|re.I).sub('', html)
	text = re.sub(r'\s+', ' ', text)
	text = re.compile(r'</?(h\d|p|br|div｜li)[^>]*>', re.I).sub('\n', text)
	text = re.sub(r'<[^>]*>', '', text)
	text = HTMLParser.HTMLParser().unescape(text)
	return text
	
def compress_spaces(html):
	text = re.compile(r'\n(\s*?\n)+').sub('\n\n', html)
	return text

