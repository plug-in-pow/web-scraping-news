from bs4 import BeautifulSoup
import requests
import csv

sr_no = 0
base_url = 'https://www.boomlive.in/fake-news'
pages = 0
file = open('fake-news-2.csv', 'w')
writer = csv.writer(file, delimiter='|')

writer.writerow(['Sr.no', 'title', 'content', 'author', 'image url', 'news url', 'label'])

while pages < 175:
    print('started')
    url = base_url + '/' + str(pages)
    html1 = requests.get(url).text
    soup1 = BeautifulSoup(html1, 'lxml')

    news_list = soup1.find_all('div', attrs={'class': 'card-wrapper horizontal-card'})

    for news in news_list:
        sr_no += 1
        news_image_url = news.find('figure', attrs={'class': 'card-image'}).a.img['data-src']
        news_title = news.find('h2', attrs={'class': 'entry-title'}).a.text
        news_content = news.find('p', attrs={'class': 'selectionShareable common-p'}).a.text
        news_url = base_url + news.find('h2', attrs={'class': 'entry-title'}).a['href']

        html2 = requests.get(news_url, allow_redirects=False).text
        soup2 = BeautifulSoup(html2, 'lxml')
        author_div = soup2.find('div', attrs={'class': 'post-meta large-12 small-12 columns'})
        if author_div is not None:
            news_author = author_div.a.text + '-BoomLive'
        else:
            news_author = 'BoomLive'

        # print('Sr No: ', sr_no)
        # print('Title: ', news_title)
        # print('Content: ', news_content)
        # print('Image Url: ', news_image_url)
        # print('News Url: ', news_url)
        # print('Author: ', news_author)
        # print('Label: 1')
        # print('')

        writer.writerow([sr_no, news_title, news_content, news_author, news_image_url, news_url, '1'])
    print('completed')
    print('')
    pages += 1

file.close()
