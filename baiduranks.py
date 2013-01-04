# -*- coding: cp936 -*-
from __future__ import division
import urllib2
import time
import datetime
from bs4 import BeautifulSoup
import re
currenttime=time.time()
term='诺基亚'
today=str(datetime.date.today())
url='http://www.baidu.com/s?wd='+term
html=urllib2.urlopen(url).read()
soup=BeautifulSoup(html)
titles=[]
dess=[]
urls=[]
updates=[]
crawed_date=[]
notes=[]
postions=[]
ranks=[]
def get_left_paids(soup):
     leftpaids=soup.find_all('td',id=re.compile(r'taw\d'))
     if len(leftpaids)==0:
          return None
     left_titles=[leftpaid.font.get_text().strip() for leftpaid in leftpaids[0:int(len(leftpaids)/2):2]]
     left_dess=[leftpaid.get_text().strip() for leftpaid in leftpaids[1:int(len(leftpaids)/2):2]]
     left_urls=[leftpaid.find('font',attrs={'color':'#008000'}).get_text().strip() for leftpaid in leftpaids[0:int(len(leftpaids)/2):2]]
     global titles,urls,updates,notes,postions,ranks,dess
     titles+=left_titles
     dess+=left_dess
     urls+=left_urls
     updates+=list(''*len(left_titles))
     notes+=list(''*len(left_titles))
     postions+=list('left'*len(left_titles))
     ranks+=list(range(1,len(left_titles)+1))
     for n in range(len(left_titles)):
          print left_titles[n]
          print left_dess[n]
          print left_urls[n]
     return left_titles,left_dess,left_urls

def get_right_paids(soup):
     rightpaids=soup.find_all('div',id=re.compile(r'bdfs\d'))
     if len(rightpaids)==0:
          return None
     right_titles=[rightpaid.a.get_text().strip() for rightpaid in rightpaids]
     right_dess=[rightpaid.find('font',attrs={'color':'#000000'}).get_text().strip() for rightpaid in rightpaids]
     right_urls=[rightpaid.find('font',attrs={'color':'#008000'}).get_text().strip() for rightpaid in rightpaids]
     global titles,urls,updates,notes,postions,ranks,dess
     titles+=right_titles
     dess+=right_dess
     urls+=right_urls
     updates+=list(''*len(right_titles))
     notes+=list(''*len(right_titles))
     postions+=list('right'*len(right_titles))
     ranks+=list(range(1,len(right_titles)+1))
     for n in range(len(right_titles)):
          print right_titles[n]
          print right_dess[n]
          print right_urls[n]
     return right_titles,right_dess,right_urls

def get_organics(soup):
     organics=soup.find_all('table',attrs={'class':re.compile(r'result( - op)?')})
     organic_titles=[organic.h3.get_text().strip() for organic in organics]
     organic_dess=[]
     organic_urls=[]
     organic_updates=[]
     organic_notes=[]
     for organic in organics:
          if organic.has_key('mu'):##百度开放平台，百度百科等
               organic_des=''
               organic_url=organic['mu']
               note='op'
               try:
                    organic_update=organic.find('font',attrs={'color':'#008000'}).get_text().strip().split(' ')[-1]
               except AttributeError:
                    organic_update=''          
          else:
               organic_url=organic.find('span',attrs={'class':'g'}).get_text().strip().split(' ')[0]
               organic_update=organic.find('span',attrs={'class':'g'}).get_text().strip().split(' ')[-1]
               organic_des=organic.find('font',attrs={'size':'-1'}).get_text(strip=True).replace(organic_url+' '+organic_update+'-百度快照'.decode('gbk','ignore'),'')##没想到很好的方法，有部分信息冗余
               note=''
          organic_dess.append(organic_des)
          organic_urls.append(organic_url)
          organic_updates.append(organic_update)
          organic_notes.append(note)
     global titles,dess,urls,updates,notes,postions,ranks
     titles+=organic_titles
     dess+=organic_dess
     urls+=organic_urls
     updates+=organic_updates
     notes+=organic_notes
     postions+=list('organic'*len(organic_titles))
     ranks+=list(range(1,len(organic_titles)+1))     
     for n in range(len(organic_titles)):
          print organic_titles[n]
          print organic_dess[n]
          print organic_urls[n]
          print organic_updates[n]
          print notes[n]
     return organic_titles,organic_dess,organic_urls,organic_updates
ranks=[]=list(today*len(titles))
print 'leftpaids'
get_left_paids(soup)
print 'rightpaids'
get_right_paids(soup)
print 'organics'
get_organics(soup)
