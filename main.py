import requests,random,telebot,time,re
from config import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from json import JSONDecodeError
from database import create_db_and_tables,engine,Request
from sqlmodel import Session,select
from bs4 import BeautifulSoup
from loguru import logger

logger.add("khamsat_bot.log",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {function} | {message}",colorize=False,enqueue=True,mode="w")

create_db_and_tables()

bot = telebot.TeleBot(bot_token)

request_page = 'https://khamsat.com/community/requests/'
requests_session = requests.Session()
requests_session.headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                            'x-requested-with': 'XMLHttpRequest',}

def set_new_proxy() : 
    creds = str(random.randint(10000,0x7fffffff)) + ":" + "foobar"
    requests_session.proxies = {'http': 'socks5h://{}@localhost:9050'.format(creds), 'https': 'socks5h://{}@localhost:9050'.format(creds)}

def extract_id(link) :
    pattern = r'\d{6}'
    match = re.search(pattern, link)
    if match:
        return match.group()
    else:
        return None
    
def get_last_contributors_section() :
    requests_ids = []
    response = requests_session.get('https://khamsat.com/community/stories/1',allow_redirects=True)
    if response.status_code == 200 : 
        soup = BeautifulSoup(response.text,features='lxml')
        requests = soup.find_all("div", {"class": "o-media__body pt-2"})
        for request in requests : 
            if 'request' in str(request) :
                requests_ids.append(extract_id(request.a['href']))
    return requests_ids

def get_request_description(request_id) :
    description = {}
    response = requests_session.get(request_page+str(request_id))
    if response.status_code == 200 : 
        soup = BeautifulSoup(response.text,features='lxml')
        description['request_id']       = request_id
        description['title']            = soup.h1.text
        description['description']      = soup.find('article').text.strip()
        description['requester_name']   = soup.find("td", {"class": "details-td avatar-td__small-padding"}).h3.text
        description['requester_rating'] = soup.find("td", {"class": "details-td avatar-td__small-padding"}).li.text
    return description

def build_message(request : Request): 
    return f'''📣📣 New Request Alert 📣📣

🔹 Request Title: {request.title}
------------------------------------------------------------------------
🔹 Request Description: {request.description}
------------------------------------------------------------------------
🔹 Requester Name: {request.requester_name}
------------------------------------------------------------------------
🔹 Requester Rating: {request.requester_rating}
------------------------------------------------------------------------
'''

def send_alert(chat_id,request : Request) : 
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ Click here to visit the request's page ➡️", url=request_page+str(request.request_id)))
    bot.send_message(chat_id=int(chat_id),
                     text=build_message(request),
                     reply_markup=markup)

while True : 
    database_session = Session(engine)
    set_new_proxy()
    requests_ids = get_last_contributors_section()
    try : 
        logger.info(f'fetched {len(requests_ids)} requests from contributors page.')
        for request in requests_ids : 
            logger.info(f'start fetch request_id : {request}')
            fetched_request = database_session.exec(select(Request).where(Request.request_id == request)).first()
            if fetched_request :
                continue
            request_description = get_request_description(request_id=request)
            request_to_send = Request(request_id=request,
                                      title=request_description['title'],
                                      description=request_description['description'],
                                      requester_name=request_description['requester_name'],
                                      requester_rating=request_description['requester_rating'])
            database_session.add(request_to_send)
            database_session.commit()
            send_alert(chat_id=chat_id,
                       request=request_to_send)
    except Exception as e :  
        logger.error(f'error occured : {str(e)}')
    logger.info('sleep for 1 minute to release the resources')
    time.sleep(60)
    database_session.close()
    


