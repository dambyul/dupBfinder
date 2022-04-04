from bs4 import BeautifulSoup
import requests

#YES24
goods_id = '106337382'
url = "http://www.yes24.com/product/goods/" + goods_id
request_isbn = requests.get(url)
soup = BeautifulSoup(request_isbn.content.decode('utf-8', 'replace'), "html.parser")
isbn = soup.select_one('#infoset_specific > div.infoSetCont_wrap > div > table > tbody > tr:nth-child(6) > td')
print(isbn.get_text())

#KYOBO
goods_id = '4801197377144'
url = "https://digital.kyobobook.co.kr/digital/ebook/ebookDetail.ink?barcode=" + goods_id
request_isbn = requests.get(url)
soup = BeautifulSoup(request_isbn.content.decode('utf-8', 'replace'), "html.parser")
isbn = soup.find('table','tb01')
isbn = isbn.select_one('tbody > tr:nth-child(2) > td')
print(isbn.get_text().strip()[-14:-1])

#ALADIN
goods_id = 'ALADIN287117574'
goods_id = goods_id.replace("ALADIN","")
url = "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=" + goods_id
request_isbn = requests.get(url)
soup = BeautifulSoup(request_isbn.content.decode('utf-8', 'replace'), "html.parser")
isbn = soup.find('div','conts_info_list2')
isbn = isbn.select_one('ul > li:nth-child(5)')
print(isbn.get_text()[-13:])

