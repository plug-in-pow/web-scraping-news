from bs4 import BeautifulSoup
import requests
import csv

sr_no = 0
base_url = 'https://www.factchecker.in/fact-check/'
pages = 0
file = open('fake-real-dataset-1.csv', 'w')
writer = csv.writer(file, delimiter='|')

writer.writerow(['Sr.no', 'title', 'content', 'author', 'image url', 'news url', 'label'])
while pages < 34:
    print('started')
    url = base_url + str(pages)
    html1 = requests.get(url).text
    soup1 = BeautifulSoup(html1, 'lxml')

    articles = soup1.find_all('article', attrs={'class': 'row section_margin animate-box mob-flex mob-pd15 fadeInUp '
                                                         'animated-fast'})

    for news in articles:
        isFactCheck = True if news.find('span', attrs={'class': 'meta_categories mob-hide'}).a.text == 'Fact Check' else False
        if isFactCheck:
            sr_no += 1
            news_image_url = news.find('img')['data-src']
            news_title = news.find('h3', attrs={'class': 'alith_post_title mob-h3-style'}).a.text
            news_url = url + news.find('h3', attrs={'class': 'alith_post_title mob-h3-style'}).a['href']
            news_author = news.find('span', attrs={'class': 'meta_author_name mob-hide'}).a.strong.text

            html2 = requests.get(news_url).text
            soup2 = BeautifulSoup(html2, 'lxml')
            story = soup2.find('div', attrs={'class': 'story_content details-content-story'})
            para_in_story = story.find_all('p')
            for para in para_in_story:
                if 'Claim' in para.text:
                    news_content = para.text.replace('Claim:', '').strip()
                elif 'Fact' in para.text:
                    if 'True' in para.text:
                        label = 0
                    else:
                        label = 1

            # print('Sr No: ', sr_no)
            # print('Title: ', news_title)
            # print('Content: ', news_content)
            # print('Image Url: ', news_image_url)
            # print('News Url: ', news_url)
            # print('Author: ', news_author)
            # print('Label: ', label)
            # print('')
            writer.writerow([sr_no, news_title, news_content, news_author, news_image_url, news_url, label])
            print('completed')
            print('')
    pages += 1

file.close()
