from bs4 import BeautifulSoup
import requests
import shutil
import csv

# Initializing variables.
sr_no = 1625
base_url = 'https://www.boomlive.in/fake-news'
pages = 161

# opening / creating csv file
file = open('boom_live_fake_news_dataset_01.csv', 'a', encoding="utf-8")
writer = csv.writer(file, delimiter='|')
# writer.writerow(['Sr.no', 'title',
#                  'content', 'author',
#                  'image url', 'news url',
#                  'label'])

# Navigating to each pages
while pages <= 180:

    # For displaying the current page
    print('started' + str(pages))

    # Getting the html of the current page
    url = base_url + '/' + str(pages)
    html1 = requests.get(url).text
    soup1 = BeautifulSoup(html1, 'lxml')

    # Getting the list of news article in current page
    news_list = soup1.find_all('div', attrs={'class': 'card-wrapper horizontal-card'})

    # Looping through the news article
    for news in news_list:

        # Serial no for each row
        sr_no += 1

        # Scrapping the image_url, news_title, news_content and news_url
        news_image_url = news.find('figure', attrs={'class': 'card-image'}).a.img['data-src']
        news_title = news.find('h2', attrs={'class': 'entry-title'}).a.text
        news_content = news.find('p', attrs={'class': 'selectionShareable common-p'}).a.text
        news_url = base_url + news.find('h2', attrs={'class': 'entry-title'}).a['href']

        # Going to the actual news article
        html2 = requests.get(news_url).text
        soup2 = BeautifulSoup(html2, 'lxml')

        # Going to the claim section of the news article
        claims = soup2.find_all('div', attrs={'class': 'claim-value'})

        # Initializing author and fact_check to null
        # if no result is found
        news_author = 'Null'
        fact_check = 'Null'

        # If the news article is found having the
        # claim tag then assigning the value.
        # else breaking the loop and dropping the result.
        if len(claims) != 0:
            news_author = claims[1].find('span', attrs={'class': 'value'}).text
            fact_check = claims[2].find('span', attrs={'class': 'value'}).text
        else:
            sr_no -= 1
            continue

        # Checking the fact_check result and assigning the label
        if fact_check == 'False' or fact_check == 'Misleading':
            label = '1'
        else:
            label = '0'

        # Saving the images in a file
        try:
            image_response = requests.get(news_image_url, stream=True)
            image_file = open("./boom_live_image_dataset_01/"+str(sr_no)+"_Boom_live_news_image.png", "wb")
            image_response.raw_decode_content = True
            shutil.copyfileobj(image_response.raw, image_file)
            del image_response
        except:
            sr_no -= 1
            print("Some error occurred! dropping this news")
            print("")
            continue

        print('Sr No: ', sr_no)
        # print('Title: ', news_title)
        # print('Content: ', news_content)
        # print('Image Url: ', news_image_url)
        # print('News Url: ', news_url)
        # print('Author: ', news_author)
        # print('Label:', label)
        print('')

        # Finally writing the row in the csv
        writer.writerow([sr_no, news_title,
                         news_content, news_author,
                         news_image_url, news_url,
                         label])

    # Incrementing the page
    pages += 1

# Closing the file
file.close()
