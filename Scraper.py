from selenium import webdriver
import os
import ast
import uuid
import urllib.request

searchterm = "dog"
url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
	browser = webdriver.Chrome('C:\WebDrivers\chromedriver.exe')#insert path to chromedriver inside parentheses
	browser.get(url)
	extensions = { "jpg", "jpeg", "png", "gif" }
	if not os.path.exists(searchterm):
			os.mkdir(searchterm)
	for _ in range(500):
		browser.execute_script("window.scrollBy(0,10000)")
	  
	html = browser.page_source.split('["')
	imges = []
	for i in html:
		if i.startswith('http') and i.split('"')[0].split('.')[-1] in extensions:
			imges.append(i.split('"')[0])
	print(imges)
	def save_image(img, searchterm)
	for img in imges:
		img_url = img
		img_type = img.split('.')[-1]
		try:
			path = os.path.join(searchterm, searchterm + "_" + str(uuid.uuid4()) + "." + 'jpg')
			urllib.request.urlretrieve(img, path)
		except Exception as e:
			print(e)
	save_image(imges,directory)