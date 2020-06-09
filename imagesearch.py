import requests
from fake_useragent import UserAgent
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
import time

ua = UserAgent()

ua = ua.firefox
headers = {'User-Agent':ua}

searchEngines = {}
searchEngines['google']='https://www.google.com/searchbyimage?image_url='
searchEngines['bing']='https://www.bing.com/images/searchbyimage?FORM=IRSBIQ&cbir=sbi&imgurl='
searchEngines['yandex']='https://yandex.com/images/search?source=collections&&url='

chrome = ''

def getGoogleName(url):
    furl = searchEngines['google']+urllib.parse.quote_plus(url)
    pg = requests.get(furl,headers=headers)

    if pg.status_code != 200:
        return ''

    html=BeautifulSoup(pg.text,"html.parser")

    name = html.find("input",{'aria-label':"Search"}).get('value')

    return name

def loadPageinChrome(furl):
    try:
        chrome.get(furl)
    except Exception as e:
        try:
            chrome.get(furl)
        except Exception as e:
            return False
    time.sleep(1.5)
    return True
        

def getBingName(url):
    furl = searchEngines['bing']+urllib.parse.quote_plus(url)
    name=''
    re_tries=5
    if loadPageinChrome(furl):
        while re_tries:
            try:
                name=chrome.find_element_by_xpath("//div[@class='iscscd_data']").find_element_by_tag_name('span').text
                break
            except Exception as e:
                print(e)
                re_tries-=1
                time.sleep(1.5)
    return name

def getYandexName(url):
    furl = searchEngines['yandex']+urllib.parse.quote_plus(url)
    name=''
    re_tries=5
    if loadPageinChrome(furl):
        while re_tries:
            try:
                name=chrome.find_element_by_xpath("//li[@class='other-sites__item']").text
                break
            except Exception as e:
                print(e)
                re_tries-=1
                time.sleep(1.5)
    return name



def fromScript(chromeB,url,uap):
    global chrome
    global ua

    chrome = chromeB
    ua = uap
    gname=bname=''
    
    try:
        gname = getGoogleName(url)
    except Exception as e:
        e=0
    
    try:
        bname = getBingName(url)
    except Exception as e:
        e=0
    return [gname,bname]

