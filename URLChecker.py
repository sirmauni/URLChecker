# python broken class object

import requests;
import re;

#Broken URL checker class 
class URLChecker:

	def __init__(self, config):
		# set default variable values
		self.URL_Map = {};
		self.URLListLength = -1;
		
		# set configurations
		self.setURL_List(config["URL_List"]);
		self.setRegularExpressions(config["regExpressions"]);
		self.setReqHeaders(config["headers"]);
		self.setURLsToSkip(config["URLsToSkip"]);
		
	# URL List functions
	def setURL_List(self, *newURL_List):
		self.URL_List = newURL_List[0];
		self.URLListLength = len(self.URL_List);
	
	def getURL_List(self):
		return self.URL_List;
		
	def getURLFromList(self, index):
		return self.URL_List[index];
		
	def addToURLList(self, newURL):
		self.URL_List.append(newURL);
		self.URLListLength += 1;
		
	def getURLListLength(self):
		return self.URLListLength;
	
	# reguar expression functions
	def setRegularExpressions(self, *newRegExps):
		self.regExpressions = newRegExps[0];
		
	def getRegularExpressions(self):
		return self.regExpressions;
		
	# request headers 
	def setReqHeaders(self, newHeaders):
		self.reqHeaders = newHeaders;
		
	def getReqHeaders(self):
		return self.reqHeaders;
		
	def setURLsToSkip(self, newUrlsToSkip):
		self.URLsToSkip = newUrlsToSkip;
	
	def getURLsToSkip(self):
		return self.URLsToSkip;
	
	def urlToSkip(self, url):
		for skipURL in self.URLsToSkip:
			if skipURL in url:
				return True;
		
		return False;
		
	# url map funcitons
	def setURLMap(self, newURLMap):
		self.URL_Map = newURLMap;
		
	def getURLMap(self):
		return self.URL_Map;
	
	def addToURLMap(self, newURL, status):
		self.URL_Map[newURL] = status;
		
	def removeFromURLMap(self, url):
		if url in self.URL_Map:
			del self.URL_Map[url];
			return true;
		
		return false;
	
	def URLMapped(self, url):
		return url in self.URL_Map;
		
	# http request functions
	def requestURL(self, url):
		responseInfo = {"statusCode": -1, "content": None};
		
		try:
			response = requests.get(url, headers=self.reqHeaders);
			responseInfo["statusCode"] = response.status_code;
			responseInfo["content"] = response.content;
		except Exception as e:
			pass;
		
		return responseInfo;
	
	def formatURL(self, url):
		
		if url.startswith("//"):
			url = "https:" + url;
		elif not url.startswith("http"):
			if not url.startswith("/"):
				url = "/" + url;
			url = self.getURLFromList(0) + url;
			
		# remove up to trailing #
		if "#" in url:
			url = url[:url.find("#")];
			
		return url;
	
	def parseAdditionalLinks(self, content):
		foundURLs = [];
		
		for reg_exp in self.regExpressions:
			tmp_arr = re.findall(reg_exp, str(content));
			
			for foundURL in tmp_arr:
				if not self.urlToSkip(foundURL):
					foundURLs.append(self.formatURL(foundURL));
					
		return foundURLs;
		
		
		
	