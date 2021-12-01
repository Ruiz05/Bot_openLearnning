import json
import requests
from datetime import datetime
from time import sleep
linkPgae_couese = 'https://umkt.ucm.ac.id/courses/example-class/A_1/'
data1 = {
    'user' : 'masukkan email/username',
    'password' : 'masukkan passwd openlearning',
    "tokenType":"legacy-temporary"
}
data_couse = {
    'cohortPath' : '',
    'coursePath' : '', #coursePath itu yang 2021ee ujungnya
    'subscriptionId' : '',
    'userId': '',
    'cohortId':'',
    'courseId':'',
    'institutionId':'',
    'next_page' : '',
    'link_now' : linkPgae_couese,
    'blockid' : '' #blockid dipakai buat post slide dibaca
}
kokies = {
    'csrftoken' : '',
    'sessionid' : ""
}
heder = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Csrftoken': '',
    'Referer': data_couse['link_now'],
}
heder_learning_time = {
    'Authorization': 'SharedAccessSignature sr=https%3A%2F%2Flearningtime.servicebus.windows.net%2Flearningtime&sig=9sm9tD%2B%2BKzgRwJBxII088SG3eUfP%2Bb2Yo46qEmS8mO0%3D&se=1941521597&skn=OLClientSenderLive',
    'Accept': '*/*',
    'Origin': 'https://umkt.ucm.ac.id',
    'Referer': 'https://umkt.ucm.ac.id/'
}
proxies = {
   'http': 'http://127.0.0.1:8080'
}
def pecah_link(link):
    if 'https' or 'https' in link:
        link = link.replace(link[:8],'')
    data = link.split('/')
    if '' in data:
        del data[-1]
    if len(data) == 5:
        data_couse['link_now'] = data[-2] + '/' + data[-1]
        return [data[2],data[-2] + '/' + data[-1]]
    else:
        data_couse['link_now'] = data[-1]
        return [data[2],data[-1]]
    
def login(data):
    meh = requests.session()
    meh.get('https://umkt.ucm.ac.id/')
    z = meh.post('https://umkt.ucm.ac.id/json/auth',data=data)
    kokies['csrftoken'] = meh.cookies.get_dict()['csrftoken']
    kokies['sessionid'] = meh.cookies.get_dict()['sessionid']
    heder['X-Csrftoken'] = meh.cookies.get_dict()['csrftoken']
    if z.status_code == 200:
        print('login sukses...!')
    else:
        print("login gagal...!?")

def next_pages(data,chorlink):
    url = 'https://umkt.ucm.ac.id/json/page/multi/read/' + data + '/?methodsJSON=[{"method":"getTraversalLinks","args":{"cohortPath":"'+ chorlink +'"}}]'
    url_get_block_id = 'https://umkt.ucm.ac.id/json/page/multi/read/' + data + '/?methodsJSON=["data","getLatestRevisionId"]'
    elmo = requests.get(url, cookies=kokies).json()
    data_couse['link_now'] = elmo['id']
    data_couse['next_page'] = elmo['result'][0]['result']['next']['url']
    data_couse['blockid'] = requests.get(url_get_block_id,cookies=kokies).json()['result'][0]['result']['blockIndexes'][0]

def ambil_data(couse_name):
    url = 'https://umkt.ucm.ac.id/json/course/read/getEnrolledClassDataForUser/umkt/courses/' + couse_name + '/'
    begarang = requests.get(url, cookies=kokies).json()
    data_couse['coursePath'] = begarang['result']['enrolments'][0]['coursePath']
    data_couse['cohortPath'] = begarang['result']['enrolments'][0]['cohortPath']
    data_couse['subscriptionId'] = begarang['result']['course']['subscriptionId']
    data_couse['userId'] = begarang['result']['enrolments'][0]['userId']
    data_couse['institutionId'] = begarang['result']['course']['institution']
    data_couse['courseId'] = begarang['result']['course']['id']
    data_couse['cohortId'] = str(begarang['result']['cohorts']).split('{')[1].replace("'",'').replace(':','').replace(' ','').replace("'","")
    return 'data sukses didapat'
def posting(block_id,link):
    data = {
        'methodsJSON' : [
            {
                "method":"updateBlockInteraction",
                "args":{
                    "blockID":block_id,
                    "interaction":"{\"visits\":1,\"interactions\":1}",
                    "group":None
                    }
            },
            {
                "method":"getBlockCompletion",
                "args":{
                    "blockID":block_id}
            }
            ]
    }
    garing = str(data).replace(' ','').replace('{"visits":1,"interactions":1}','{\\"visits\\":1,\\"interactions\\":1}')
    armadilo = garing.replace(garing[:15], '').replace(garing[-1], '')
    puma = armadilo.replace('None', 'null}}').replace("'", '"').replace('":1"', '":1}"')
    bahrain = puma.replace(puma[-1], '}}]')
    url = 'https://umkt.ucm.ac.id/json/page/multi/update/' + link + '/'
    cumi = requests.post(url,data={'methodsJSON' : bahrain},cookies=kokies,headers=heder)
    if ((cumi.status_code == 200) and (cumi.json()['result'][0]['success'] == True)):
        print("Sukses")
    else:
        print('eror bos...?!!')
        print(cumi)
def ngelike(link):
    url = 'https://umkt.ucm.ac.id/json/page/update/addFavourite/' + link + '/'
    ngelik = requests.post(url,cookies=kokies,headers=heder)
    if(ngelik.status_code == 200):
        print("berhasil ngelike page "+link)
    else:
        print('data gagal di print bos')
def learningtime(time):
    data = {
    "timestamp":time, #datetime.utcnow().isoformat()[:-3] + "Z",
    "userId":data_couse['userId'],
    "pagePath":data_couse['link_now'],
    "cohortId":data_couse['cohortId'],
    "courseId":data_couse['courseId'],
    "subscriptionId":data_couse['subscriptionId'],
    "institutionId":data_couse['institutionId'],
    "ip":"114.122.235.56",
    "device":"web",
    "newView":True
    }
    esme = requests.post('https://learningtime.servicebus.windows.net/learningtime/messages',json=data,headers=heder_learning_time)
    if(esme.status_code == 201):
        print("learning time sukses dikirim")
    else:
        print('learning time gagal dikirim bos')
sesio = login(data1)
ambil_data(pecah_link(linkPgae_couese)[0])
p = next_pages(data_couse['coursePath'] + '/' + data_couse['link_now'],data_couse['cohortPath'])
ngelike(data_couse['link_now'])
learningtime(datetime.utcnow().isoformat()[:-3] + "Z")
print('setelah ini Masuk lopping')
while True:
    next_pages(data_couse['coursePath'] + '/' + pecah_link(data_couse['next_page'])[1],data_couse['cohortPath'])
    posting(data_couse['blockid'],data_couse['link_now'])
    ngelike(data_couse['link_now'])
    learningtime(datetime.utcnow().isoformat()[:-3] + "Z")
    print(data_couse)
