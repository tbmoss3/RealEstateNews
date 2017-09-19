"""
https://beautiful-soup-4.readthedocs.io/en/latest/
https://stackoverflow.com/questions/35469540/scraping-using-beautiful-soup-not-working-for-a-particular-url-as-expected
http://searchengineland.com/meta-robots-tag-101-blocking-spiders-cached-pages-more-10665
https://stackoverflow.com/questions/42584357/cannot-scrape-web-page-using-python
https://stackoverflow.com/questions/29858752/error-message-chromedriver-executable-needs-to-be-available-in-the-path
https://stackoverflow.com/questions/14095511/beautifulsoup-in-python-getting-the-n-th-tag-of-a-type
https://stackoverflow.com/questions/35416575/get-the-href-text-of-a-link-that-has-a-certain-class-attribute-using-beautifulso
https://stackoverflow.com/questions/43478496/extracting-an-articles-text-using-beautifulsoup
https://stackoverflow.com/questions/157938/hiding-a-password-in-a-python-script-insecure-obfuscation-only#comment48424_157975
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
import time
import os
import csv
import base64

##cities = ['washington','newyork','triangle','losangeles','chicago','dallas','houston','philadelphia','atlanta','southflorida'
##          ,'boston','sanfrancisco','charlotte','baltimore','tampa','minneapolis','seattle','nashville','lasvegas']
NC = ['charlotte','triangle','triad']
cities = ['washington', 'newyork', 'atlanta','nashville','boston','baltimore']
emails = [NC , cities]

links_final=[]
links_visited=[]
driverpath = '.\chromedriver.exe'


def crawler(location,path,article_limit):
    print 'Getting source for links to crawl...'
    url = 'URL_HIDDEN_FOR_COPYRIGHT_REASONS'+location+'URL_HIDDEN_FOR_COPYRIGHT_REASONS'
    driver = webdriver.Chrome(path) 
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    pages_to_visit_raw=[]
    pages_to_visit_final=[]
    
    links = soup.find_all('a', {'class': 'item item--flag ', 'href': True}, limit = article_limit)
    print 'Getting links to visit...'
    for link in links:  
        pages_to_visit_raw.append(link['href'])

    for page in pages_to_visit_raw:
        if str(page).startswith('http://'):
            pages_to_visit_final.append(str(page))
        else:
            correct_version = 'URL_HIDDEN_FOR_COPYRIGHT_REASONS'+str(page)
            pages_to_visit_final.append(correct_version)

    driver.quit()
    return pages_to_visit_final
    print pages_to_visit_final


def articles(links_to_check,links_checked):
    for page in links_to_check:
        if page not in links_checked:
            try:
                print 'Getting page source...'
                driver = webdriver.Chrome(driverpath)
                try:
                    driver.get(page)
                except:
                    print 'Driver not working.'
                    print Exception
                    pass
                try:
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                except:
                    print 'Problem with BeautifulSoup Object.'
                    print Exception
                    pass
                try:
                    print 'Getting article limit...'
                    limit = [e.get_text() for e in soup.find_all('span', attrs={'class':'prompt__headline__counter'})]
                except:
                    print '\nCouldn\'t get an article limit.'
                    print Exception
                    pass

                try:
                    print 'Getting date...'
                    date = [e.get_text() for e in soup.find_all('span', {'class': 'detail__meta__datetime'})]
                except:
                    print'\nDate unavailable.\n'
                    print Exception
                    pass

                try:
                    print 'Getting title...'
                    title = [e.get_text() for e in soup.find_all('h1', {'class':'detail__headline'})]
                except:
                    print '\nCouldn\'t get a title.\n'
                    print Exception
                    pass
                try:
                    print 'Getting author...'
                    author = [e.get_text() for e in soup.find_all('a', {'data-ct':'APT: Reporter byline name'})]
                except:
                    print 'Did not find author.'
                    print Exception
                    pass

                try:
                    print 'Getting article...'
                    paragraphs = [e.get_text() for e in soup.find_all('p', {'class': 'content__segment'})]
                    article = '\n\n'.join(paragraphs)
                except:
                    print '\nCouldn\'t get the article to load.'
                    print Exception
                    pass
                driver.quit()
                print 'Opening file...'
                f = open('crenews.txt','a')
                print 'Writing to file...'
                try:
                    f.write('\n')
                    f.write(page.encode('utf-8').strip())
                except:
                    print 'Could not get html link.'
                    print Exception
                    pass
                try:
                    f.write('\n\n')
                    f.write(title[0].encode('utf-8').strip())
                except:
                    print 'Could not get title to article in file.'
                    print Exception
                    pass
                try: 
                    f.write('\n')
                    f.write(date[0].encode('utf-8').strip())
                except:
                    print 'Could not get date to article in file.'
                    print Exception
                    pass
                try:
                    f.write('\n')
                    f.write(author[0].encode('utf-8').strip())
                except:
                    print 'Could not write author to file.'
                    print Exception
                    pass
                try:
                    f.write('\n\n')
                    f.write(article.encode('utf-8').strip())
                except:
                    print 'Could not write article to file.'
                    print Exception
                    pass
                f.write('\n---------------------------------------------------------------------------------------------------------\n')
                f.write('---------------------------------------------------------------------------------------------------------\n')
                print 'Closing file...'
                f.close()
                try:
                    if str(limit[0]) != '0 of 3':
                        links_checked.append(page)
                        print 'Subscription article.'
                        pass
                    elif str(limit[0]) == '0 of 3':
                        links_checked.append(page)
                        print 'Subscription article.'
                        driver.quit()
                        articles(links_final,links_visited)
                except IndexError:
                    print 'This was a free article.'
                    links_checked.append(page)
                    pass
                
            except:
                print '\nUnexpected Error.'
                print Exception
                pass
    if links_checked == links_final:
        print 'Checked all links for current metropolitan area successfully.'
    else:
        print 'Didn\'t quite get to all links.'
    
if __name__ == '__main__':
    start = time.time()
    confFile = '.\peekaboo.csv'
    for email in emails:
        for city in email:
            try:
                links_final.append(crawler(city,driverpath,3))
            except:
                'Crawler is not working right.'
                print Exception
            try:
                links_final = links_final[-1]
                articles(links_final,links_visited)
            except:
                print '\nFetching articles not working properly.'
                print Exception

        f = open('crenews.txt','r')
        message = f.read()
        
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    with open(confFile, 'rb') as csvfile:
        peekaboo = csv.reader(csvfile, delimiter=',', quotechar='|')
        for encrypted in peekaboo:
            password = str(base64.b64decode(str(encrypted)))
    smtpObj.login('YOUR_EMAIL_HERE', password)
    print 'Emailing articles...'
    smtpObj.sendmail('FROM_YOUR_EMAIL', 'TO_YOUR_EMAIL','Subject: Real Estate News\n' + message)
    smtpObj.quit()
    f.close()
    
    print 'Cleaning up and finishing...'
    os.remove('crenews.txt')
    end = time.time()
    print 'Operations successful in : ', (end - start)/float(60), ' minutes.'
