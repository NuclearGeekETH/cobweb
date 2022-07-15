from flask import Flask, request, render_template, redirect, url_for, jsonify
import test
from cobweb import startBot

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get_site/', methods=['GET', 'POST'])
# @app.route('/get_site/')
def get_site():
  if request.method == "POST":
    website = request.form['site']
    print(website)
    # print(website)
    # website = "https://twitter.com/NuclearGeeketh/status/1547685440592834569"
    print('clicked')
    link = startBot(website)
    print(link)
    # return redirect(url_for(link))
    # return render_template('getsite.html', link=link)
  return render_template('getsite.html', link=link)
  
  # else:
  #   print('test')  
  #   website = request.form['return']
  #   print(website)
  #   print('clicked')
  #   link = startBot(website)
  #   # return link, res
  #   return link

# @app.route('/my-link/')
# def my_link():
#   print ('I got clicked!')

#   return 'Click.'

if __name__ == '__main__':
  app.run(debug=True)