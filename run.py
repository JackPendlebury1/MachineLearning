import os
import sys

from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from util import base64_to_pil
from selenium import webdriver
import ast
import uuid
import urllib.request
import zipfile

app = Flask(__name__)

from keras.applications.mobilenet_v2 import MobileNetV2
model = MobileNetV2(weights='imagenet')

def model_predict(img, model):
	img = img.resize((224, 224))
	x = image.img_to_array(img)
	# x = np.true_divide(x, 255)
	x = np.expand_dims(x, axis=0)
	x = preprocess_input(x, mode='tf')
	preds = model.predict(x)
	return preds

import uuid
filename = str(uuid.uuid4())
@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')
		
@app.route('/predict', methods=['GET', 'POST'])
def predict():
	if request.method == 'POST':
		img = base64_to_pil(request.json)
		img.save("uploads/" + filename + ".png")
		preds = model_predict(img, model)
		pred_proba = "{:.3f}".format(np.amax(preds))
		pred_class = decode_predictions(preds, top=1)
		result = str(pred_class[0][0][1])
		result = result.replace('_', ' ').capitalize()
	searchterm = result
	directory = "./images/"
	url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
	browser = webdriver.Chrome('C:\WebDrivers\chromedriver.exe')
	browser.get(url)
	extensions = { "jpg", "jpeg", "png", "gif" }
	if not os.path.exists(directory):
			os.mkdir(directory)
	for _ in range(500):
		browser.execute_script("window.scrollBy(0,10000)")  
	html = browser.page_source.split('["')
	imges = []
	for i in html:
		if i.startswith('http') and i.split('"')[0].split('.')[-1] in extensions:
			imges.append(i.split('"')[0])
	print(imges)
	def save_image(img, directory):
		for img in imges:
			img_url = img
			img_type = img.split('.')[-1]
			try:
				path = os.path.join(directory, searchterm + "_" + str(uuid.uuid4()) + "." + 'jpg')
				urllib.request.urlretrieve(img, path)
			except Exception as e:
				print(e)
	save_image(imges,directory)
	browser.close()
	fantasy_zip = zipfile.ZipFile('C:\\Users\\User\\Desktop\\FYP\\images.zip', 'w')
 
	for folder, subfolders, files in os.walk('C:\\Users\\User\\Desktop\\FYP\\images'):
 
		for file in files:
			if file.endswith('.jpg'):
				fantasy_zip.write(os.path.join(folder, file), file, compress_type = zipfile.ZIP_DEFLATED)
	fantasy_zip.close()
	return jsonify(result=result, probability=pred_proba)
	
if __name__ == '__main__':
	http_server = WSGIServer(('0.0.0.0', 5000), app)
	http_server.serve_forever()