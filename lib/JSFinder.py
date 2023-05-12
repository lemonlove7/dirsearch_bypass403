#!/usr/bin/env python"
# coding: utf-8
# By Threezh1
# https://threezh1.github.io/

import requests, argparse, sys, re,csv,os
from requests.packages import urllib3
from urllib.parse import urlparse
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from concurrent.futures import ThreadPoolExecutor

from colorama import init, Fore, Style


init()

# Regular expression comes from https://github.com/GerbenJavado/LinkFinder
def extract_URL(JS):
	pattern_raw = r"""
	  (?:"|')                               # Start newline delimiter
	  (
	    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
	    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
	    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
	    |
	    ((?:/|\.\./|\./)                    # Start with /,../,./
	    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
	    [^"'><,;|()]{1,})                   # Rest of the characters can't be
	    |
	    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
	    [a-zA-Z0-9_\-/]{1,}                 # Resource name
	    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
	    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
	    |
	    ([a-zA-Z0-9_\-]{1,}                 # filename
	    \.(?:php|asp|aspx|jsp|json|
	         action|html|js|txt|xml)             # . + extension
	    (?:\?[^"|']{0,}|))                  # ? mark with parameters
	  )
	  (?:"|')                               # End newline delimiter
	"""
	pattern = re.compile(pattern_raw, re.VERBOSE)
	result = re.finditer(pattern, str(JS))
	if result == None:
		return None
	js_url = []
	return [match.group().strip('"').strip("'") for match in result
		if match.group() not in js_url]

# Get the page source
def Extract_html(URL):
	header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
			  }
	# "Cookie": args.cookie}
	try:
		raw = requests.get(URL, headers = header, timeout=3, verify=False)
		raw = raw.content.decode("utf-8", "ignore")
		return raw
	except:
		return None

# Handling relative URLs
def process_url(URL, re_URL):
	black_url = ["javascript:"]	# Add some keyword for filter url.
	URL_raw = urlparse(URL)
	ab_URL = URL_raw.netloc
	host_URL = URL_raw.scheme
	if re_URL[0:2] == "//":
		result = host_URL  + ":" + re_URL
	elif re_URL[0:4] == "http":
		result = re_URL
	elif re_URL[0:2] != "//" and re_URL not in black_url:
		if re_URL[0:1] == "/":
			result = host_URL + "://" + ab_URL + re_URL
		else:
			if re_URL[0:1] == ".":
				if re_URL[0:2] == "..":
					result = host_URL + "://" + ab_URL + re_URL[2:]
				else:
					result = host_URL + "://" + ab_URL + re_URL[1:]
			else:
				result = host_URL + "://" + ab_URL + "/" + re_URL
	else:
		result = URL
	return result

def find_last(string,str):
	positions = []
	last_position=-1
	while True:
		position = string.find(str,last_position+1)
		if position == -1:break
		last_position = position
		positions.append(position)
	return positions

def find_by_url(url, js = False):
	if js == False:
		try:
			pass
			#print("url:" + url)
		except:
			print("Please specify a URL like https://www.baidu.com")
		html_raw = Extract_html(url)
		if html_raw == None: 
			print("Fail to access " + url)
			return None
		#print(html_raw)
		html = BeautifulSoup(html_raw, "html.parser")
		html_scripts = html.findAll("script")
		script_array = {}
		script_temp = ""
		for html_script in html_scripts:
			script_src = html_script.get("src")
			if script_src == None:
				script_temp += html_script.get_text() + "\n"
			else:
				purl = process_url(url, script_src)
				script_array[purl] = Extract_html(purl)
		script_array[url] = script_temp
		allurls = []
		for script in script_array:
			#print(script)
			temp_urls = extract_URL(script_array[script])
			if len(temp_urls) == 0: continue
			for temp_url in temp_urls:
				allurls.append(process_url(script, temp_url)) 
		result = []
		for singerurl in allurls:
			url_raw = urlparse(url)
			domain = url_raw.netloc
			positions = find_last(domain, ".")
			miandomain = domain
			if len(positions) > 1:miandomain = domain[positions[-2] + 1:]
			#print(miandomain)
			suburl = urlparse(singerurl)
			subdomain = suburl.netloc
			#print(singerurl)
			if miandomain in subdomain or subdomain.strip() == "":
				if singerurl.strip() not in result:
					result.append(singerurl)
		return result
	return sorted(set(extract_URL(Extract_html(url)))) or None


def find_subdomain(urls, mainurl):
	url_raw = urlparse(mainurl)
	domain = url_raw.netloc
	miandomain = domain
	positions = find_last(domain, ".")
	if len(positions) > 1:miandomain = domain[positions[-2] + 1:]
	subdomains = []
	for url in urls:
		suburl = urlparse(url)
		subdomain = suburl.netloc
		#print(subdomain)
		if subdomain.strip() == "": continue
		if miandomain in subdomain:
			if subdomain not in subdomains:
				subdomains.append(subdomain)
	return subdomains

def find_by_url_deep(url):
	html_raw = Extract_html(url)
	if html_raw == None: 
		print("Fail to access " + url)
		return None
	html = BeautifulSoup(html_raw, "html.parser")
	html_as = html.findAll("a")
	links = []
	for html_a in html_as:
		src = html_a.get("href")
		if src == "" or src == None: continue
		link = process_url(url, src)
		if link not in links:
			links.append(link)
	if links == []: return None
	print("ALL Find " + str(len(links)) + " links")
	urls = []
	i = len(links)
	for link in links:
		temp_urls = find_by_url(link)
		if temp_urls == None: continue
		print("Remaining " + str(i) + " | Find " + str(len(temp_urls)) + " URL in " + link)
		for temp_url in temp_urls:
			if temp_url not in urls:
				urls.append(temp_url)
		i -= 1
	return urls

	
def find_by_file(file_path, js=False):
	with open(file_path, "r") as fobject:
		links = fobject.read().split("\n")
	if links == []: return None
	print("ALL Find " + str(len(links)) + " links")
	urls = []
	i = len(links)
	for link in links:
		if js == False:
			temp_urls = find_by_url(link)
		else:
			temp_urls = find_by_url(link, js=True)
		if temp_urls == None: continue
		print(str(i) + " Find " + str(len(temp_urls)) + " URL in " + link)
		for temp_url in temp_urls:
			if temp_url not in urls:
				urls.append(temp_url)
		i -= 1
	return urls

def giveresult(urls, domian):
	sss=[]
	if urls == None:
		return None
	print(Fore.MAGENTA + Style.BRIGHT+"Find " + str(len(urls)) + " URL:"+Style.RESET_ALL)
	print(Fore.YELLOW + Style.BRIGHT+"Start testing for survival!"+Style.RESET_ALL)
	content_url = ""
	content_subdomain = ""
	def process_url(url):
		title=''
		Exclusions=['.js','.png','.jpg','.ico','.css','.gif','.svg','.mp3','.wav','.mp4','.webm']
		try:
			headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
			res = requests.get(url,headers=headers, verify=False, timeout=2)
			status_code = res.status_code
			soup = BeautifulSoup(res.content, 'html.parser')
			title_tag = soup.find('title')
			if title_tag:
				title = title_tag.text
		except:
			status_code = 404

		if status_code == 200 or status_code == 201:
			colour = Fore.GREEN + Style.BRIGHT
		elif status_code == 301 or status_code == 302:
			colour = Fore.BLUE + Style.BRIGHT
		elif status_code == 403 or status_code == 404:
			colour = Fore.MAGENTA + Style.BRIGHT
		elif status_code == 500:
			colour = Fore.RED + Style.BRIGHT
		else:
			colour = Fore.WHITE + Style.BRIGHT
		if status_code != 404:
			if not any(url.endswith(ext) for ext in Exclusions):
				print( url + ' ' + colour + str(status_code)+Style.RESET_ALL)
				sss.append({"URL": url, "Code": str(status_code),"title":str(title)})
				if status_code == 403:
					try:
						with open('jsfind403list.txt', 'a+') as f:
							f.write(str(url) + '\n')
					except:
						pass


	def main():
		with ThreadPoolExecutor() as executor:
			executor.map(process_url, urls)
	main()

	def GreateFile(sss,domian):
		parsed_url = urlparse(domian)
		domain1 = parsed_url.netloc
		with open("reports/"+domain1+'.csv', 'w', newline='', encoding='GB18030') as csvf:
			fieldnames = ['URL','Code','title']
			writer = csv.DictWriter(csvf, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerows(sss)


	GreateFile(sss,domian)

	subdomains = find_subdomain(urls, domian)
	print(Fore.MAGENTA + Style.BRIGHT+"\nFind " + str(len(subdomains)) + " Subdomain:"+Style.RESET_ALL)


	for subdomain in subdomains:
		content_subdomain += subdomain + "\n"
		print(subdomain)
