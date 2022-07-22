COBWEB

Archive the internet with Web3!

Use http://www.cobweb.aifrens.io to pin any link to IPFS using Web3.storage

Try out the Twitter bot by replying to a tweet with any text and @AiFrensBot at the end, or just @AiFrensBot

[Twitter Bot](https://twitter.com/AiFrensBot)

Clone the repository

For the Flask Server to run the website:
Run server.py and install missing dependencies. You might need to comment off lines 34 and 35 from server.py and turn on your own version of app.run() depending on how you want to host it. You will need a .env file in root with your web3.storage or pinata keys.

For the Twitter Bot:
Run bot.py and install missing dependencies. Add your keys for twitter and web3.storage or pinata to the .env file in root.

Troubleshooting:
You will need your version of chromedriver.exe for your version of chrome installed on your system. Flask app.run() will need to be modified for your environment. Make sure you add a .env file in root with your keys

Do Next:

 - Add a gallery of pins that are public and personal


