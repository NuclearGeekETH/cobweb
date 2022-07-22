from flask import Flask, request, render_template, redirect, url_for, jsonify
import test
from cobweb import startBot
from OpenSSL import SSL
import threading
import time

def start_thread(func, name=None, args = []):
    threading.Thread(target=func, name=name, args=args).start()

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get_site/', methods=['GET', 'POST'])
def get_site():
  if request.method == "POST":
    website = request.form['site']
    print(website)
    print('clicked')
    # link = start_thread(startBot, args=[website])
    link = startBot(website)
    # time.sleep(20)
    print(link)
  return render_template('getsite.html', link=link)
  

if __name__ == '__main__':
  # context = SSL.Context(SSL.TLSv1_2_METHOD)
  # context.use_privatekey_file('/etc/letsencrypt/live/cobweb.aifrens.io/privkey.pem')
  # context.use_certificate_file('/etc/letsencrypt/live/cobweb.aifrens.io/fullchain.pem')
  from waitress import serve
  serve(app, host="0.0.0.0", port=80)
  # context=('/etc/letsencrypt/live/cobweb.aifrens.io/fullchain.pem', '/etc/letsencrypt/live/cobweb.aifrens.io/privkey.pem')
  # app.run(host="0.0.0.0", ssl_context=context, threaded=True, port=80)
  # app.run(host="0.0.0.0", ssl_context=('adhoc'), port=80)
  # app.run(debug=False)  
  # app.run(host="0.0.0.0", port=80, ssl_context=('/etc/letsencrypt/live/cobweb.aifrens.io/fullchain.pem', '/etc/letsencrypt/live/cobweb.aifrens.io/privkey.pem'))