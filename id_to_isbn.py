import chardet as chardet
from bs4 import BeautifulSoup
import mysql.connector
import requests
import urllib.request
stored_data = []

outdb = mysql.connector.connect(
    host='',
    user='',
    password='',
    port=,
    buffered=True
)
out_cursor = outdb.cursor(dictionary=True)
sql = "use hongji"
out_cursor.execute(sql)

def id_search(url : str) -> list :
    rawdata = urllib.request.urlopen(url).read()
    encode = chardet.detect(rawdata)['encoding']
    res = requests.post(url)
    soup = BeautifulSoup(res.content.decode(encode, 'replace'), "html.parser")
    a = soup.find_all("tr")
    for i in range (1,len(a)):
        data = a[i].find_all("td")
        stored_data.append([data[1].get_text().strip(),data[2].get_text().strip(),data[3].get_text().strip()])

id_search('')

def isbn_search(comcode : str, goods_id : str) -> str:
    comcode = comcode.upper()
    if comcode in ["YES24", "YES"]:  # YES24
        url = "https://www.yes24.com/product/goods/" + goods_id
        request_isbn = requests.get(url)
        soup = BeautifulSoup(request_isbn.content.decode('utf-8', 'replace'), "html.parser")
        isbn = soup.select_one('#infoset_specific > div.infoSetCont_wrap > div > table > tbody > tr:nth-child(6) > td')
        if isbn:
            return isbn.get_text()
        else:
            print("YES24 : 결과 없음")

    elif comcode in ["KYOBO", "KB"]:  # KYOBO
        url = "https://digital.kyobobook.co.kr/digital/ebook/ebookDetail.ink?barcode=" + goods_id
        request_isbn = requests.get(url)
        soup = BeautifulSoup(request_isbn.content.decode('utf-8', 'replace'), "html.parser")
        isbn = soup.find('table', 'tb01')
        if isbn:
            isbn = isbn.select_one('tbody > tr:nth-child(2) > td')
            isbn = isbn.get_text().strip()
            isbn_loc = isbn.find('ISBN')
            if isbn_loc > -1 :
                isbn_tmp = isbn[isbn_loc + 5:isbn_loc + 18]
                isbn_check = isbn_tmp.find(':')
                if isbn_check > -1 :
                    isbn = isbn[isbn_loc + 7:isbn_loc + 20]
                else :
                    isbn = isbn_tmp
                return isbn
            else :
                print("KYOBO : 결과 없음")
        else:
            print("KYOBO : 결과 없음")

    elif comcode in ["ALADIN"]:  # ALADIN
        goods_id = goods_id.replace("ALADIN", "")
        url = "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=" + goods_id
        request_isbn = requests.get(url)
        soup = BeautifulSoup(request_isbn.content.decode('utf-8', 'replace'), "html.parser")
        isbn = soup.find('div', 'conts_info_list2')
        if isbn:
            isbn = isbn.select_one('ul > li:nth-child(5)')
            try:
                isbn = int(isbn.get_text()[-13:])
                return str(isbn)
            except :
                print("ALADIN : 결과 없음")
        else:
            print("ALADIN : 결과 없음")

    else:  # 미지원 유통사
        print("지원하지 않는 유통사")


for i in stored_data :
    comcode = i[0]
    if comcode.upper() in ['YS','YES','YES24'] :
        comcode = 'YES24'
    elif comcode.upper() in ['KB','KYOBO'] :
        comcode = "KYOBO"
    elif comcode.upper() in ['ALADIN'] :
        comcode = "ALADIN"
    goods_id = i[1]
    content_title = i[2]
    sql = "select * from isbn where comcode ='" + comcode + "'and goods_id ='" + goods_id + "'"
    out_cursor.execute(sql)
    row_result = out_cursor.rowcount
    if row_result == 0 :
        print("조회 결과 없음 - " + goods_id)
        isbn_result = isbn_search(comcode, goods_id)
        if isbn_result :
            sql = "insert into isbn (comcode,goods_id,isbn,content_title) values ('" + comcode + "','" + goods_id + "','" + isbn_result + "','" + content_title.replace("'","\\'") +"')"
            out_cursor.execute(sql)
            outdb.commit()
            print("검색된 isbn - " + isbn_result)
        else :
            sql = "insert into isbn (comcode,goods_id,isbn,content_title) values ('" + comcode + "','" + goods_id + "','','" + content_title.replace("'","\\'") +"')"
            out_cursor.execute(sql)
            outdb.commit()
    else :
        for x in out_cursor:
            print("DB 존재 데이터 - " + goods_id)

#isbn_search("aladin","ALADIN281744175")
#isbn_search("kyobo","4808960534018")
#isbn_search("yes24","11259630")

# YES24 검색 결과 중 전자책 ISBN이 아닌 종이책 ISBN이 입력된 도서가 있음
