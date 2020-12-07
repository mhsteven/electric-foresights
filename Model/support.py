import requests
def download_links(date,link):    
    r=requests.get(link,allow_redirects=False)
    path='./data/'+date+'.csv'
    open(path,'wb').write(r.content)