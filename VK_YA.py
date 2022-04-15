import json
import requests
import os
import time
from tqdm import tqdm
from pprint import pprint

TOKEN_VK = ''
TOKEN_YA = ''
id_user = '552934290'

#_______________________________________________________________________

def info_photos(id_user):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': id_user,
        'access_token': TOKEN_VK,
        'v': '5.131',
        'album_id': 'profile',
        'extended': '1'
    }
    res = requests.get(URL, params=params).json()
    return res
#_______________________________________________________________________

def search_name_file(name, file_list):
    otvet = ''
    for name_file in file_list:
        if name != name_file['file_name']:
            otvet = 'NO'
        else:
            otvet = 'YES'
    return otvet
#_______________________________________________________________________

def make_list_file(id_user):
    sum_file = 5
    list_info = info_photos(id_user)['response']['items']
    list_info_file = []
    for info in list_info:
        name_file = str(info['likes']['count']) + '.jpg'
        name_file_date = str(info['likes']['count'])
        if search_name_file(name_file, list_info_file) =='NO' or len(list_info_file) == 0:
            info_new = {'file_name': name_file,
                    'size': info['sizes'][-1]['type'],
                    'url': info['sizes'][-1]['url']
                    }
            if len(list_info_file) < sum_file:
               list_info_file.append(info_new)
            else:
                break

        else:
            info_new = {'file_name': f"{name_file_date}_{info['date']}.jpg",
                    'size': info['sizes'][-1]['type'],
                    'url': info['sizes'][-1]['url']
                     }
            if len(list_info_file) < sum_file:
               list_info_file.append(info_new)
            else:
                break

    return list_info_file
#_______________________________________________________________________

def write_file_info_photos(id_user):
    list_info_file = make_list_file(id_user)
    with open('list_info_foto.json', 'w') as f:
        json.dump(list_info_file, f, ensure_ascii=False, indent=3)
#_______________________________________________________________________

def write_photos_pc(id_user):
    write_file_info_photos(id_user)
    list_info_file = make_list_file(id_user)

    for file in list_info_file:
        url = file['url']
        file_name = file['file_name']
        r = requests.get(url)
        with open(f"FOTO_YA/{file_name}",'wb') as f:
            f.write(r.content)
#_______________________________________________________________________

def write_photos_ya(id_user, TOKEN):
    if not os.path.isdir('FOTO_YA'):
        os.mkdir('FOTO_YA')

    p = {'path': 'vk_foto'}
    h = {'Content-Type': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
    URL_PATH = 'https://cloud-api.yandex.net/v1/disk/resources'
    r = requests.put(URL_PATH, headers=h, params=p)

    write_photos_pc(id_user)

    FILE_PATH = 'FOTO_YA'
    BASE_PATH = os.getcwd()
    PATH_FILES = os.path.join(BASE_PATH, FILE_PATH)
    list_file = os.listdir(PATH_FILES)

    for file in tqdm(list_file):
        name_file = 'vk_foto/' + file
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        h = {'Content-Type': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
        p = {'path': name_file, 'overwrite': 'true'}
        req = requests.get(upload_url, headers=h, params=p).json()

        href = req['href']
        req = requests.put(href, data=open('FOTO_YA/' + file, 'rb'))
        req.raise_for_status()
        if req.raise_for_status() == 201:
            print('Success')

    print('Процесс загрузки завершен!')

write_photos_ya(id_user, TOKEN_YA)




