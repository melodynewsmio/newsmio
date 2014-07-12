import os
import dropbox
from flask import Flask, request, render_template, redirect, url_for
from forms import LoginForm

app = Flask(__name__)
app.config.from_object('config')

DROPBOX_APP_KEY = 'p6f5a5j7su9wuqn'
DROPBOX_APP_SECRET = '37ztarzben724z5'

@app.route('/')
def index():
	return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(DROPBOX_APP_KEY, DROPBOX_APP_SECRET)
	authorize_url = flow.start()
	if form.validate_on_submit():
		code = form.openid.data
		access_token, user_id = flow.finish(code)
		return redirect('/info' + "?token=" + access_token)
	return render_template('authentication.html', title='Authenticate', **locals())

@app.route('/info')
def info():
	access_token = request.args.get('token')
	f1 = open('./log.txt', 'rb')
	client = dropbox.client.DropboxClient(access_token)
	client_info = client.account_info()
	display_name = client_info['display_name']
	client.put_file('/test.txt', f1)
	return render_template('info.html', **locals())