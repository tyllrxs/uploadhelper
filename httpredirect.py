# -*- coding: utf-8 -*-

import urllib2


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
 
    def http_error_301(self, req, fp, code, msg, headers):                        
	result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
	result.status = code
	return result                                     

    def http_error_302(self, req, fp, code, msg, headers):                                  
        result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
	result.status = code
	return result
