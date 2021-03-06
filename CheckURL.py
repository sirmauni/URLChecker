# Checks list of urls provided in URLChecker.config file for broken list.
# Returns JSON object detailing "Working" or "Not Working".
# Working: http(s) request returned with status code 200.
# Not Working: http(s) request did not return 200.

import json;
from URLChecker import URLChecker;

# config data
config = None;

# read config file
with open("./URLChecker.config") as file:
	config = json.loads(file.read());

# construct URL checker with configuration data
uChecker = URLChecker(config);

# iter counter for URL list
currentIndex = 0;	

# loop through every url in url_list 
while currentIndex < uChecker.getURLListLength() :
	# current url from url list 
	currentURL = uChecker.getURLFromList(currentIndex);
	
	# if url is in map
	if uChecker.URLMapped(currentURL):
		# skip to next iteration
		currentIndex += 1;
		continue;
		
	# get http response for url at iter counter[x]
	responseInfo = uChecker.requestURL(currentURL);
	
	# if response code == 200
	if responseInfo["statusCode"] == 200:
		uChecker.addToURLMap(currentURL, "Working");
	else:
		uChecker.addToURLMap(currentURL, "Not Working");
		
	# if external link, continue to  next iter
	if uChecker.getURLFromList(0) not in currentURL:
		currentIndex += 1;
		continue;
		
	# parse content for additional links
	additionalURLs = uChecker.parseAdditionalLinks(responseInfo["content"]);
	
	# add any unmapped list to url list 
	for url in additionalURLs:
		if not uChecker.URLMapped(url):
			uChecker.addToURLList(url);
	
	# increment index 
	currentIndex += 1;

# print JSON data to console
print(json.dumps(uChecker.getURLMap(), indent=4));
