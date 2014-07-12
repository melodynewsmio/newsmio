import base64
from flask import abort, Flask, redirect, request, session, url_for, render_template
import os
import requests
import urllib
import dropbox

app = Flask(__name__)
app.secret_key = 'abc123'

APP_KEY = 'p6f5a5j7su9wuqn';
APP_SECRET = '37ztarzben724z5';

@app.route('/')
def index():
	csrf_token = base64.urlsafe_b64encode(os.urandom(18))
	session['csrf_token'] = csrf_token
	return redirect('https://www.dropbox.com/1/oauth2/authorize?%s' % urllib.urlencode({
		'client_id': APP_KEY,
		'redirect_uri': url_for('callback', _external=True),
		'response_type': 'code',
		'state': csrf_token
	}))

@app.route('/callback')
def callback():
	if request.args['state'] != session.pop('csrf_token'):
		abort(403)
	data = requests.post('https://api.dropbox.com/1/oauth2/token',
		data={
			'code': request.args['code'],
			'grant_type': 'authorization_code',
			'redirect_uri': url_for('callback', _external=True)
		},
		auth=(APP_KEY, APP_SECRET)).json()
	token = data['access_token']
	return redirect('/upload?token=' + token)

@app.route('/upload')
def upload():
	access_token = request.args.get('token')
	client = dropbox.client.DropboxClient(access_token)
	f1 = open('./log.txt', 'rb')
	client.put_file('/test.txt', f1)
	client_info = client.account_info()
	display_name = client_info['display_name']
	return render_template('index.html', **locals())

if __name__=='__main__':
	app.run(debug=True)