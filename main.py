from flask import Flask, url_for, send_from_directory, request
import logging, os
from werkzeug import secure_filename
import hashlib
import datetime
import pyminizip

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
	newpath = local_dir
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

@app.route('/', methods = ['POST'])
def api_root():
	app.logger.info(datetime.datetime.now())		
	if request.method == 'POST' and len(request.files.getlist(''))==1:		
		md5_hash = hashlib.md5()
		files = request.files.getlist('')		
		for file in files:		
			file_name = secure_filename(file.filename)
			create_new_folder(app.config['UPLOAD_FOLDER'])
			saved_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)			
			file.save(saved_path)			
			content = open(saved_path,'rb').read()
			md5_hash.update(content)
			digest = md5_hash.hexdigest()
			zip_path = os.path.join(app.config['UPLOAD_FOLDER'], digest + '.zip')			
			compression_level = 5 # 1-9			
			pyminizip.compress(saved_path, None, zip_path, "iii", compression_level)
			os.remove(saved_path)
		return digest
	else:
		return "error"

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False)
