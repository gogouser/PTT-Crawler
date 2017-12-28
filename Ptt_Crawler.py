
# coding: utf-8

# In[124]:


get_ipython().system('pip install --user --upgrade beautifulsoup4 lxml html5lib==1.0b8')


# In[2]:


import requests
from bs4 import BeautifulSoup


# In[4]:


def funtion(url,cookies):
    resp = requests.get(
        url, 
        cookies=cookies
    )

    soup = BeautifulSoup(resp.text.encode('utf-8'), 'lxml')

    gossip_list = soup.find('div', {'class': 'r-list-container action-bar-margin bbs-screen'})

    a_list = gossip_list.find_all('a')
    #print(type(a_list))

    bbs_url_list = [link.get('href') for link in a_list]

    bbs_text_list = [link.text for link in a_list]

    author_list = gossip_list.find_all('div', {'class': 'author'})
    author_list = [link.text for link in author_list]
    
    re_dic = {
        'bbs_url_list': bbs_url_list,
        'bbs_text_list': bbs_text_list,
        'author_list': author_list
    }
    
    return re_dic


# In[5]:


# up_url_list = ['1','2','3','4','5']
up_url_list = []

url = "https://www.ptt.cc/bbs/Gossiping/index.html"

for i in range(0, 5):
    resp = requests.get(
        url, 
        cookies={'over18': '1'}
    )
    soup = BeautifulSoup(resp.text.encode('utf-8'), 'lxml')

    page_list = soup.find('div', {'class': 'btn-group btn-group-paging'})
    up_list = page_list.find_all('a')
#     up_url_list[i] = 'https://www.ptt.cc' + up_list[1].get('href')
    up_url_list.append('https://www.ptt.cc' + up_list[1].get('href'))
    url = up_url_list[i]
    
page_info = []

for i in range(0, 5):
    print(up_url_list[i])
    page_info.append(funtion(up_url_list[i],{'over18': '1'}))

for i in range(0, 5):
    print(len(page_info[i]['bbs_url_list']))
    print(len(page_info[i]['bbs_text_list']))
    print(len(page_info[i]['author_list']))
    print(' ')
    
    
    


# In[4]:


class PttCrawler:
    def __init__(self, board, write= False ):
        self.ptt_url = 'https://www.ptt.cc'
        self.board = board
        self.now_page = board
        self.session = requests.Session()
        self.session.cookies.update({
            'over18':'1'
        })
        self.write=write
        
        
    def page_info(self,url):
        resp = self.session.get(
            url
        )

        soup = BeautifulSoup(resp.text.encode('utf-8'), 'lxml')

        gossip_list = soup.find('div', {'class': 'r-list-container action-bar-margin bbs-screen'})

        a_list = gossip_list.find_all('div',{'r-ent'})
        
        re_dic = []
        
        for link in a_list:
            bbs_a = link.find('a')
            
            author = link.find('div', {'class': 'author'})
            date = link.find('div', {'class': 'date'})
            
            if(bbs_a != None):
                bbs_url = 'https://www.ptt.cc' + bbs_a.get('href')
                resp = self.session.get(
                    bbs_url
                )
                soup = BeautifulSoup(resp.text.encode('utf-8'), 'lxml')

                bbs_content = soup.find('div',{'id': 'main-content'})

                content = ''
                s = list(bbs_content.strings)
                for i in range(8,len(s)-1):
                    content = content + s[i]
                text = bbs_a.text
            else:
                content = '找不到文章'
                text = '找不到文章'

            re_dic.append({
                'bbs_url': bbs_url,
                'bbs_text': text,
                'author': author.text,
                'date': date.text,
                'content': content
            })
        
        return re_dic
    
    
    def previous_page_url(self,url):
        resp = self.session.get(
            url
        )
        soup = BeautifulSoup(resp.text.encode('utf-8'), 'lxml')

        page_list = soup.find('div', {'class': 'btn-group btn-group-paging'})
        up_list = page_list.find_all('a')
        if not up_list[1].get('href'):
            re_str = 'this is first page!'
        else:
            re_str = 'https://www.ptt.cc' + up_list[1].get('href')
            self.now_page = re_str
        return self.now_page
    
    def next_page_url(self,url):
        resp = self.session.get(
            url
        )
        soup = BeautifulSoup(resp.text.encode('utf-8'), 'lxml')

        page_list = soup.find('div', {'class': 'btn-group btn-group-paging'})
        up_list = page_list.find_all('a')
        if not up_list[2].get('href'):
            re_str = 'this is last page!'
        else:
            re_str = 'https://www.ptt.cc' + up_list[2].get('href')
            self.now_page = re_str
        return self.now_page
    
    def to_page(self,page):
        re_str = self.board
        for i in range(0, page):
            re_str = self.previous_page(re_str)
        self.now_page = re_str
        return self.now_page
    
    @property
    def show_now_page(self):
        return self.now_page
    
    @property
    def next_page(self):
        self.next_page_url(self.now_page)
        return self.now_page
    
    @property
    def previous_page(self):
        self.previous_page_url(self.now_page)
        return self.now_page
    
    @property
    def return_to_board(self):
        self.now_page = self.board
        return self.now_page


# In[7]:


test = PttCrawler('https://www.ptt.cc/bbs/Gossiping/index.html')
print(test.previous_page_url('https://www.ptt.cc/bbs/Gossiping/index.html'))
print(test.previous_page)
print(test.next_page)
print(test.now_page)
print(test.return_to_board)

re_dic = test.page_info(test.now_page)
i=10
print(len(re_dic))
print()
print(re_dic[i]['bbs_text'])
print()
print(re_dic[i]['bbs_url'])
print()
print(re_dic[i]['author'])
print()
print(re_dic[i]['content'])
print()
print(re_dic[i]['date'])

