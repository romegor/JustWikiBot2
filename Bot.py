import telebot
import time
import requests
from bs4 import BeautifulSoup


def WikiBot():
    TOKEN = "377124564:AAGMAac_fqA8ViAQRa99-kD7LQKi7U9bZPw"
    bot = telebot.TeleBot(TOKEN)
    # Обработчик команд '/start' и '/help'.
    @bot.message_handler(commands=['start', 'help'])
    def handle_start_help(message):
        bot.send_message(message.chat.id,'добро пожаловать, {name}, в гости к ВикиБоту. Для поиска по википедии введите название на английском или русском языке'.format(name=message.from_user.first_name))   
    @bot.message_handler(content_types=["text"])
    def handle_all_messages(message):
        bot.send_message(message.chat.id, "Поиск информации на Википедии...")
        article = RequestToWiki2(message.text)
        astart = 0
        if len(article[0])>40000:
            bot.send_message(message.chat.id, "Слишком большая статья, будет показана ее часть")
            time.sleep(2)
        for i in range(4000,len(article[0])+4000,4000):
            if i>40000:
                break
            if len(article)<i:
                bot.send_message(message.chat.id, article[0][astart:])
            else:
                bot.send_message(message.chat.id, article[0][astart:i])
            astart +=4000        
            time.sleep(3)
        #Код отправки ссылки на википедию
        #if len(article[1])>5:
        #    bot.send_message(message.chat.id, article[1])
    bot.polling(none_stop=True)
    return True

def RequestToWiki(S):
    out = ''
    goodurl = ''
    lang = {0:'ru', 1:'en'}
    req = PrepareInString(S)
    for lang_cur in lang.values():
        try:
            url = 'https://'+ lang_cur +'.wikipedia.org/wiki/' + req
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content)
            #Content = soup.find('div', {'class': 'mw-parser-output'}).text

            Content = soup.find('div', {'class': 'mw-parser-output'})
            flag = False
            text = ''
            #for elem in Content:
            #    if elem.name=='p':
            #        text+=elem.text
            #        flag = True
            #    elif (elem.name=='div') and (flag):
            #        break
              
            if (Content.find('div', {'class': 'toctitle'})):
                for elem in Content:
                    if elem.name=='p':
                        text+=elem.text
                        flag = True
                    elif (elem.name=='div') and (flag):
                        break
            else:
                for elem in Content:
                    if (elem.name=='p') or (elem.name=='ul'):
                        text+=elem.text
                        flag = True
                    elif (elem.name=='table') and (flag):
                        break
            if len(text)>0:
                goodurl = url

        except Exception:
            out ='Статьи с таким именем не существует!'
        else:
            out = PrepareOutString(text)
            break

    return out, goodurl

def RequestToWiki2(S):
    out = ''
    goodurl = ''
    url = ''
    url0 ='http://www.google.com/search?q='
    page = requests.get(url0 + S)
    soup0 = BeautifulSoup(page.text)
    h3 = soup0.find_all("h3",class_="r")
    for elem in h3:
	    elem=elem.contents[0]
	    elem = elem["href"]
	    if "wikipedia" in elem:
		    url=("https://www.google.com" + elem)
		    break

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content)
        Content = soup.find('div', {'class': 'mw-parser-output'})
        flag = False
        text = ''              
        if (Content.find('div', {'class': 'toctitle'})):
            for elem in Content:
                if elem.name=='p':
                    text+=elem.text
                    flag = True
                elif (elem.name=='div') and (flag):
                    break
        else:
            for elem in Content:
                if (elem.name=='p') or (elem.name=='ul'):
                    text+=elem.text
                    flag = True
                elif (elem.name=='table') and (flag):
                    break
        if len(text)>0:
            goodurl = url
    except Exception:
        out ='По запросу ничего не найдено!'
    else:
        out = PrepareOutString(text)

    return out, goodurl

def PrepareInString(S):
    out = ''
    flag = False
    for i in S:
        if (i==' '):
            if (not flag):
                if (not out==''):
                    out+='_'
                    flag = True
            else:
                continue
        else:
            out+=i
            flag = False
    if (out[len(out)-1]=='_'):
        out = out[:len(out)-1]

    return out

def PrepareOutString(S):
    out = ''
    flag = False
    for i in S:
        if (i=='\n'):
            if (not flag):
                if (not out==''):
                    out+=i
                    flag = True
            else:
                continue
        else:
            out+=i
            flag = False
    if (out[len(out)-1]=='\n'):
        out = out[:len(out)-1]

    return out

