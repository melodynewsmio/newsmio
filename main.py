import os
import dropbox
from flask import Flask, render_template

app = Flask(__name__)

DROPBOX_APP_KEY = 'p6f5a5j7su9wuqn'
DROPBOX_APP_SECRET = '37ztarzben724z5'

@app.route('/')
def index():
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(DROPBOX_APP_KEY, DROPBOX_APP_SECRET)
    authorize_url = flow.start()
    return render_template('authentication.html', title='Index', **locals())

@app.route('/info')
def info():

    return render_template('info.html', **locals())