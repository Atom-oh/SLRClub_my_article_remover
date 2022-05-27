import requests
from bs4 import BeautifulSoup 
from urllib.parse import urlparse, parse_qs
import re, time

base_url = 'http://www.slrclub.com'

user_id = '' # <user_id>

password = '' # <user_password>
data = { "user_id":user_id, "password":password}
sess = requests.session() 
res = sess.post(f"{base_url}/login/process.php",data=data )
res.raise_for_status() 

# def get_my_article(sess):        
my_article = f'{base_url}/mypage/myarticle.php'
res = sess.get(my_article)
res.raise_for_status()

soup = BeautifulSoup(res.text, 'html.parser') 
table = soup.select_one('#mypage > table > tr > td:nth-child(3)')
table_rows = table.find_all('tr')
link = [l["href"] for l in table.find_all("a") ]
last_page = [l for l in link if str(l).startswith('/mypage')][-2]
last_page = int(re.findall('[0-9]+',last_page)[0])
my_articles = []

for page_num in range(1, last_page+1):
    res = sess.get(f'{base_url}/mypage/myarticle.php?page={page_num}&')
    soup = BeautifulSoup(res.text, 'html.parser') 
    table = soup.select_one('#mypage > table > tr > td:nth-child(3)')    
    table_rows = table.find_all('tr')
    for row in table_rows:
        table_cols = row.find_all('td')
        if len(table_cols)==3 and table_cols[1].string and '장터' not in table_cols[1].string:
            query_params=parse_qs(urlparse(table_cols[0].find("a")["href"]).query)
            my_articles.append( {'id':query_params['id'][0], 'no': query_params['no'][0], 'url': table_cols[0].find("a")["href"]})
print(my_articles)

# delete all articles
delete_url = '/bbs/remove_confirm.php'
for article in my_articles:
    data={"id": article['id'], "no": article['no'],"page": None, "page_num": None, "category": None, "mode": None,"c_no": None, "x": 57, "y": 18}
    headers = {'Referer':f'{base_url}/bbs/delete.php?id={article["id"]}&no={article["no"]}'}
    res = sess.post(f'{base_url}/bbs/remove_confirm.php', headers=headers, data=data)
    
    print(res.status_code)
    print(res.text)
    time.sleep(11)
