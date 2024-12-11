ngay = str(__import__('time').strftime("%d"))
thang = str(__import__('time').strftime("%m"))
nam = str(__import__('time').strftime("%Y"))
class Key:
    def keyfree():
        return __import__('hashlib').md5(f"NgTuw-{ngay}{thang}{nam}{ip}{pyver}".encode()).hexdigest()
    def keyvip():
        return ["keyvipbytoolngtuw", "ngtuwdz"]
if __import__('os').path.exists("NgTuwKey.json"):
    code = __import__('json').loads(open("NgTuwKey.json", "r").read())
    inp = code['key']
    mode = code['mode']
    key = Key.keyfree() if mode == 1 else Key.keyvip()
    if inp in key:
        pass
    else:
        __import__('sys').exit()
else:
    __import__('sys').exit()


import requests, time, os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

chars = f" \033[1;37;40m➤ \033[1;31;40m[\033[1;33;40m«\033[1;37;40m/\033[1;33;40m»\033[1;31;40m] \033[1;37;40m>"
def display_countdown(seconds, username):
    for i in range(seconds, 0, -1):
        print(f'{chars} \033[1;36;40mVui Lòng Chờ \033[1;37;40m{i} \033[1;36;40mGiây cho \033[1;37;40m@{username}...', end='\r')
        time.sleep(1)
    print(' ' * 50, end='\r')

def buff_follow(username, max_retries=3):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }
    retry_count = 0
    while retry_count < max_retries:
        try:
            access = requests.get('https://tikfollowers.com/free-tiktok-followers', headers=headers, timeout=10)
            session = access.cookies.get('ci_session')
            if not session:
                print(f'{chars} \033[1;36;40mKhông thể lấy session cho tài khoản \033[1;37;40m@{username}. \033[1;36;40mThử lại...')
                retry_count += 1
                continue
            headers.update({'cookie': f'ci_session={session}'})
            token = access.text.split("csrf_token = '")[1].split("'")[0]
            data = '{"type":"follow","q":"@'+username+'","google_token":"t","token":"'+token+'"}'
            search = requests.post('https://tikfollowers.com/api/free', headers=headers, data=data, timeout=10).json()
            if search.get('success'):
                data_follow = search['data']
                data = '{"google_token":"t","token":"'+token+'","data":"'+data_follow+'","type":"follow"}'
                send_follow = requests.post('https://tikfollowers.com/api/free/send', headers=headers, data=data, timeout=10).json()
                if send_follow.get('o') == 'Success!' and send_follow.get('success') and send_follow.get('type') == 'success':
                    print(f'{chars} \033[1;36;40mTăng Follow TikTok Thành Công cho tài khoản \033[1;37;40m@{username}')
                    return True
                elif send_follow.get('o') == 'Oops...' and not send_follow.get('success') and send_follow.get('type') == 'info':
                    thoigian = send_follow['message'].split('You need to wait for a new transaction. : ')[1].split('.')[0]
                    phut = int(thoigian.split(' Minutes')[0])
                    display_countdown(phut * 60, username)
            else:
                print(f'{chars} \033[1;36;40mKhông thể thực hiện yêu cầu follow cho tài khoản \033[1;37;40m@{username}.')
                retry_count += 1
        except requests.RequestException:
            print(f'{chars} \033[1;36;40mLỗi mạng khi xử lý tài khoản \033[1;37;40m@{username}. \033[1;36;40mThử lại...')
            retry_count += 1
            time.sleep(5)  
        except Exception as e:
            print(f'{chars} \033[1;36;40mLỗi không xác định cho tài khoản \033[1;37;40m@{username}: \033[1;31;40m{e}')
            retry_count += 1
            time.sleep(5) 
    print(f'{chars} \033[1;36;40mThất bại sau \033[1;37;40m{max_retries} \033[1;36;40mlần thử cho tài khoản \033[1;37;40m@{username}')
    return False

if __name__ == '__main__':
    usernames = input(f'{chars} \033[1;32;40mNhập các Username TikTok \033[1;37;40m(\033[1;36;40mkhông có @\033[1;37;40m) \033[1;32;40mcách nhau bằng dấu phẩy: \033[1;37;40m').split(',')
    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            future_to_username = {executor.submit(buff_follow, username.strip()): username.strip() for username in usernames}
            for future in as_completed(future_to_username):
                username = future_to_username[future]
                try:
                    success = future.result()
                    if success:
                        print(f'{chars} \033[1;36;40mHoàn thành việc tăng follow cho \033[1;37;40m@{username}')
                    else:
                        print(f'{chars} \033[1;36;40mKhông thể tăng follow cho \033[1;37;40m@{username}')
                except Exception as exc:
                    print(f'{chars} \033[1;36;40mLỗi trong luồng xử lý cho tài khoản \033[1;37;40m@{username}: {exc}')