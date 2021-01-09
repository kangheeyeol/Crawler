import time
from urllib import parse
import urllib.request
from multiprocessing import Pool

from bs4 import BeautifulSoup
import re
import PostgresqlDBConnent
import MorphAnal
import json
from PgHelper import PgHelper

# text 정제하기


def clean_text(text):
    # content = text.get_text()
    content = text
    cleaned_text = re.sub('[a-zA-Z]', '', content)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>▶▽♡◀━@\#$%&\\\=\(\'\"ⓒ(\n)(\t)]', '', cleaned_text)
    cleaned_text = cleaned_text.replace("🇲\u200b🇮\u200b🇱\u200b🇱\u200b🇮\u200b🇪\u200b", "")
    cleaned_text = cleaned_text.replace("오류를 우회하기 위한 함수 추가 ", "")
    cleaned_text = cleaned_text.replace("동영상 뉴스 오류를 우회하기 위한 함수 추가 ", "")
    cleaned_text = cleaned_text.replace("무단전재 및 재배포 금지", "")
    cleaned_text = cleaned_text.strip('\n')
    return cleaned_text


def blog_crawling(crawling_url):
    print(crawling_url[0])
    # print(crawling_url[1])
    try:
        req = urllib.request.urlopen(crawling_url[0])
        res = req.read()
        soup = BeautifulSoup(res, 'html.parser')

        try:
            # keywords = soup.findAll('div', {'class': 'se_textView'})
            # keywords = soup.findAll('div', {'class': 'se-main-container'})
            # keywords = soup.findAll('div', {'class': 'se-module se-module-text'})
            keywords = soup.find_all('span', {'class': 'se-fs- se-ff- '})
            # print(len(keywords))
            # print(1)
            if len(keywords) > 0:
                for a in keywords:
                    text = clean_text(a.get_text())
                    if len(text) > 0:
                        # print('\t' + text)
                        PostgresqlDBConnent.update_raw_data(text, crawling_url[1])
                    # print(keywords.get_text(strip=True))
                    # MorphAnal.add_data(keywords.get_text(strip=True))
            else:
                keywords = soup.find_all('div', {'id': 'postViewArea'})
                # print('2')
                if len(keywords) > 0:
                    for a in keywords:
                        # text = a.get_text()
                        text = clean_text(a.get_text())
                        if len(text) > 0:
                            # print(text)
                            PostgresqlDBConnent.update_raw_data(text, crawling_url[1])
                else:
                    keywords = soup.findAll('div', {'class': 'se_textView'})
                    # print('3')
                    if len(keywords) > 0:
                        # print(keywords.get_text(strip=True))
                        # print(keywords)
                        for a in keywords:
                            # text = a.get_text()
                            text = clean_text(a.get_text())
                            if len(text) > 0:
                                # print('\t' + text)
                                PostgresqlDBConnent.update_raw_data(text, crawling_url[1])
                    else:
                        print('xxxxxxxxxxxxxxxx')
        except Exception as err:
            print('??????', err)

    except urllib.error.HTTPError as e:
        # err = e.read()
        code = e.getcode()
        print(code)


def search_keyword(pghelper: object, keyword: object) -> object:
    client_id = "7o0ZnBCQzfLEleVV5JDM"
    client_secret = "uHZM6Mq0hE"
    start = 1
    display = 100
    enc_text = parse.quote(keyword)

    while start <= 1000:
        url = "https://openapi.naver.com/v1/search/blog?query=" + enc_text + "&display=" \
                      + str(display) + "&start=" + str(start)  # json 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        resp_code = response.getcode()

        if resp_code == 200:
            response_body = response.read()
            # print(response_body.decode('utf-8'))
            jsonobject = json.loads(response_body)
            jsonarray = jsonobject.get("items")
            print("\tTotal : ", jsonobject.get("total"))
            print("\tStart : ", jsonobject.get("start"))
            if jsonobject.get("total") == 0:
                break
            else:
                # PostgresqlDBConnent.keyword_add_db(jsonarray)
                if len(jsonarray) > 0:
                    pghelper.keyword_add_db(jsonarray)
                else:
                    print("xxxxx")
        else:
            print("Error Code:" + str(resp_code))

        start = start + display


if __name__ == '__main__':
    print("Search_Keyword call")
    # Search_Keyword("강원도")
    bloglink = []
    rawdata = []
    tour_api_keyword = []

    start_time = time.time()
    # kangwong = ['춘천 맛집', '원주 맛집', '강릉 맛집', '동해 맛집', '태백 맛집', '속초 맛집', '삼척 맛집', '홍천 맛집', '횡성 맛집',
    #             '영월 맛집', '평창 맛집', '정선 맛집', '철원 맛집', '화천 맛집', '양구 맛집', '인제 맛집', '고성 맛집', '양양 맛집']

    # pghelper = PgHelper()

    # pghelper.get_keyword_data(tour_api_keyword)
    # # print(tour_api_keyword.index('[강릉 바우길 11구간] 신사임당길'))
    # for i in tour_api_keyword[3214:]:
    #     print(i)
    #     Search_Keyword(pghelper, i)

    # for i in kangwong:
    #     print(i)
    #     Search_Keyword(pghelper, i)

    # pghelper.get_blog_link(bloglink)
    # pghelper.CloseDB()
    # url1 ="https://blog.naver.com/PostView.nhn?blogId=soapdiary&logNo=222087156559"
    # url2 ="https://blog.naver.com/PostView.nhn?blogId=soapdiary&logNo=222087156559"
    # bloglink.append([url1, url2])
    # for i in bloglink:
    #     Blog_crawling(i)

    # pool = Pool(processes=8)  # 4개의 프로세스를 사용합니다.
    # pool.map(Blog_crawling, bloglink)  # get_contetn 함수를 넣어줍시다.

    print("--- %s seconds ---" % (time.time() - start_time))
    PostgresqlDBConnent.get_raw_data(rawdata)
    #
    # print(rawdata)
    # print(len(rawdata))
    MorphAnal.process_data(rawdata)
    print("--- %s seconds ---" % (time.time() - start_time))
    # PostgresqlDBConnent.update_raw_data('111asdfasdfasdf',
    # 'https://blog.naver.com/eye4y?Redirect=Log&logNo=222091294214')
    # PostgresqlDBConnent.blog_add_db()
    # Blog_crawing("https://blog.naver.com/PostView.nhn?blogId=d2house&1364")
    # Blog_crawing("https://withbeatles.tistory.com/3544")
    print("Search_Keyword return")
