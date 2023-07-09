# Khamsat Scraper
Unofficial bot who scrapes not found requests the moment they are published on Khamsat freelance platform using Tor service.

**Run Tor service :** 

*   Download Tor from [here](https://www.torproject.org/download/tor/) for windows. For Linux you need only to type this command :  
```bash
  sudo apt install tor && service tor start
```

*   Unzip the file and run tor.exe file for Windows.

*   Tor service is running on 127.0.0.1:9050.


**Why do we use Tor service?**

We use Tor service to scrape data, as it allows us to change our IP address for each request, thus avoiding potential bans. Tor service provides this IP rotation functionality, and it is free to use.

**How to start the bot?**

*   Get your telegram chat\_id from [here](https://t.me/get_id_bot) 
*   Create new bot from [here](http://https://t.me/BotFather) and extract the bot_token.
*   Send at least one message from your Telegram account to the Bot.
*   Open config.py file and put the chat\_id and bot_token to their corresponding name.
*   Clone the repository or download it from [here](https://github.com/mouh2020/mostaql_scraper/archive/refs/heads/master.zip) and unzip it.
*   Open mostaql\_scraper folder on cmd and type :  
```bash
  pip install -r requirements 
```
```bash
  python main.py
```
     
*   The bot starts listening for new requests and send them to Telegram.
