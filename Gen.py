import os, httpx, websocket, base64, json, random, time, threading, ctypes, string, requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from colorama import Fore, Style
from base64 import b64encode

with open('config.json') as config_file:config = json.load(config_file)

solved = 0
genned = 0
errors = 0
genStartTime = time.time()

def TitleWorkerr():
    global genned, solved, errors, verified 
    ctypes.windll.kernel32.SetConsoleTitleW(f'Space Generator | Generated : {genned} | Errors : {errors} | Solved : {solved} | Speed : {round(genned / ((time.time() - genStartTime) / 60))}/m')

class Logger:
    def CenterText(var:str, space:int=None): # From Pycenter
        if not space:
            space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
        return "\n".join((' ' * int(space)) + var for var in var.splitlines())
    
    def Success(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'[{current_time}] ({Fore.LIGHTGREEN_EX}+{Fore.WHITE}) {text}')
        lock.release()
    
    def Error(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'[{current_time}] ({Fore.RED}-{Fore.WHITE}) {text}')
        lock.release()
    
    def Question(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'[{current_time}] ({Fore.YELLOW}?{Fore.WHITE}) {text}')
        lock.release()
    
    def Debug(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'[{current_time}] [DEBUG] ({Fore.LIGHTBLUE_EX}*{Fore.WHITE}) {text}')
        lock.release()
    
    def Console():
        os.system('clear')
        text = """
        ╔═╗┌─┐┌─┐┌─┐┌─┐  ╔═╗┌─┐┌┐┌
        ╚═╗├─┘├─┤│  ├┤   ║ ╦├┤ │││
        ╚═╝┴  ┴ ┴└─┘└─┘  ╚═╝└─┘┘└┘
        """        
        faded = ''
        red = 40
        for line in text.splitlines():
            faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
            if not red == 255:
                red += 15
                if red > 255:
                    red = 255
        print(Logger.CenterText(faded))

class Utils(object):
    @staticmethod
    def GenerateBornDate():
        year=str(random.randint(1997,2001));month=str(random.randint(1,12));day=str(random.randint(1,28))
        if len(month)==1:month='0'+month
        if len(day)==1:day='0'+day
        return year+'-'+month+'-'+day
    
    @staticmethod
    def RandomCharacter(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))
    
    @staticmethod
    def CreateEmail():
        return f"{Utils.RandomCharacter(8)}{random.choice(config['email_domains'])}"
    
    @staticmethod
    def GetVerifyToken(email):
        return httpx.get(f'{config["email_server_link"]}{email}').text
    
    @staticmethod
    def GetUsername():
        chars = ['🙂 ','🙃','🌹','🥀','🧛🏾','🧤','👕','🔫','💊','🅾','😺','😻','😾','😿','😹','😽','👾','😀','😃','😄','😁','😆','😅','😂','🤣','🥲','☺️','😊','😇','🙂','🙃','😉','😌','😍','🥰','😘','😗','😙','😚','😋','😛','😝','😜','🤪','🤨','🧐','🤓','😎','🥸','🤩','🥳','😏','😒','😞','😔','😟','😕','🙁','☹️','😣','😖','😫','😩','🥺','😢','😭','😤','😠','😡','🤬','🤯','😳','🥵','🥶','😱','😨','😰','😥','😓','🤗','🤔','🤭','🤫','🤥','😶','😐','😑','😬','🙄','😯','😦','😧','😮','😲','🥱','😴','🤤','😪','😵','🤐','🥴','🤢','🤮','🤧','😷','🤒','🤕','🤑','🤠','🔕','📣','📢','👁‍🗨','💬','💭','🗯','♠️','♣️','♥️','♦️','🃏','🎴','🀄️','🕐','🕑','🕒','🕓','🕔','🕕','🕖','🕗','🕘','🕙','🕚','🕛','🕜','🕝','🕞','🕟','🕠','🕡','🕢','🕣','🕤','🕥','🕦','🕧','⌛️','⏳','📡','🔋','🔌','💡','🔦','🕯','🪔','🧯','🛢','💸','💵','💴','💶','💷','🪙','💰','💳','💎','⚖️','🪜','🧰','🪛','🔧','🔨','⚒','🛠','⛏','🪚','🔩','⚙️','🪤','🧱','⛓','🧲','🔫','💣','🧨','🪓','🔪','🗡','⚔️','🛡','🚬','⚰️','🪦','⚱️','🏺','🔮','📿','🧿','💈','⚗️','🔭','🔬','🕳','🩹','🩺','💊','💉','🩸','🧬','🦠','🧫','🧪','🌡','🧹','🪠','🧺','🧻','🚽','🚰','🚿','🛁','🛀','🧼','🪥','🪒','🧽','🪣','🧴','🛎','🔑','🗝','🚪','🪑','🛋','🛏','🛌','🧸','🪆','🖼','🪞','🪟','🛍','🛒','🎁','🎈','🎏','🎀','🪄','🪅','🎊','🎉','🎎','🏮','🎐','🧧','✉️','📩','📨','📧','💌','📥','📤','📦','🏷','🪧','📪','📫','📬','📭','📮','📯','📜','📃','📄','📑','🧾','📊','📈','📉','🗒','🗓','📆','📅','🗑','📇','🗃','🗳','🗄','📋','📁','📂','🗂','🗞','📰','🐭','🐹','🐰','🦊','🐻','🐼','🐻‍❄️','🐨','🐯','🦁','🐮','🐷','🐽','🐸','🐵','🙈','🙉','🙊','🐒','🐔','🐧','🐦','🐤','🐣','🐥','🦆','🦅','🦉','🦇','🐺','🐗','🐴','🦄','🐝','🪱','🐛','🦋','🐌','🐞','🐜','🪰','🪲','🪳','🦟','🦗','🕷','🕸','🦂','🐢','🐍','🦎','🦖','🦕','🐙','🦑','🦐','🦞','🦀','🐡','🐠','🐟','🐬','🐳','🐋','🦈','🐊','🐅','🐆','🦓','🦍','🦧','🦣','🐘','🦛','🦏','🐪','🐫','🦒','🦘','🦬','🐃','🐂','🐄','🐎','🐖','🐏','🐑','🦙','🐐','🦌','🐕','🐩','🦮','🐕‍🦺','🐈','🐈‍⬛','🪶','🐓','🦃','🦤','🦚','🦜','🦢','🦩','🕊','🐇','🦝','🦨','🦡','🦫','🦦','🦥','🐁','🐀','🐿','🦔','🐾','🐉','🐲','🌵','🎄','🌲','🌳','🌴','🪵','🌱','🌿','☘️','🍀','🎍','🪴','🎋','🍃','🍂','🍁','🍄','🐚','🪨','🌾','💐','🌷','🌹','🥀','🌺','🌸','🌼','🌻','🌞','🌝','🌛','🌜','🌚','🌕','🌖','🌗','🌘','🌑','🌒','🌓','🌔','🌙','🌎','🌍','🌏','🪐','💫','⭐️','🌟','✨','⚡️','☄️','💥','🔥','🌪','🌈','☀️','🌤','⛅️','🌥','☁️','🌦','🌧','⛈','🌩','🌨','❄️','☃️','⛄️','🌬','💨','💧','💦','☔️','☂️','🌊','🌫','🍡','🍧','🍨','🍦','🥧','🧁','🍰','🎂','🍮','🍭','🍬','🍫','🍿','🍩','🍪','🌰','🥜','🍯','🥛','🍼','🫖','☕️','🍵','🧃','🥤','🧋','🍶','🍺','🍻','🥂','🍷','🥃','🍸','🍹','🧉','🍾','🧊','🥄','🍴','🍽','🥣','🥡','🥢','🧂','⚽️','🏀','🏈','⚾️','🥎','🎾','🏐','🏉','🥏','🎱','🪀','🏓','🏸','🏒','🏑','🥍','🏏','🪃','🥅','⛳️','🪁','🏹','🎣','🤿','🥊','🥋','🎽','🛹','🛼','🛷','⛸','🥌','🎿','⛷','🏂','🪂','🏋️‍♀️','🏋️','🏋️‍♂️','🤼‍♀️','🤼','🤼‍♂️','🤸‍♀️','🤸', '诶', '比', '西', '迪', '伊', '艾弗', '吉', '艾尺', '艾', '杰', '开', '艾勒', '艾马', '艾娜', '哦', '屁', '吉吾', '艾儿', '艾丝', '提', '伊吾', '维', '豆贝尔维', '吾艾']
        #usernames = open("input/usernames.txt", encoding="cp437").read().splitlines()
        #return random.choice(usernames)
        return  ".gg/hcap | " + Utils.RandomCharacter(5)
    
    @staticmethod
    def GetProxy():
      with open('input/proxies.txt', "r") as f:
        return random.choice(f.readlines()).strip()
    
    @staticmethod
    def GetFormattedProxy(proxy):
        if '@' in proxy:
            return proxy
        elif len(proxy.split(':')) == 2:
            return proxy
        else:
            if '.' in proxy.split(':')[0]:
                return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
            else:
                return ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])
    
    @staticmethod
    def PostTokenInWebhook(token):
        for webhook in config["webhook_urls"]:
            try:
                httpx.post(webhook, json={ "username": "Space Generator", "content": token})
            except Exception as e:
                pass

    @staticmethod
    def GetRandomGame():
        status = [ "PLAYING", "LISTENING", "PLAYING", "PLAYING", "PLAYING", "PLAYING"]
        type_status = random.choice(status)
        if type_status == "PLAYING":
            game = random.choice([ "Minecraft", "Lunar CLient", "Roblox", "Grand Theft Auto V", "Visual Studio Code", "Chrome", "Fortnite", "FarmVille 2: Country Escape", "Fall Guys", "Brawlhalla", "Far Cry 6", "Tiny Tina's Wonderland", "Call of the Wild: The Angler™", "Red Dead Redemption", "Genshin Impact", "FIFA 23 Ultimate Edition", "Rocket League", "Knockout City™", "Saints Row", "Grand Theft Auto IV", "Arcade Paradise" ])
            return { "name": game, "type": 0 }
        elif type_status == "LISTENING":
            game = random.choice([ "Spotify", "Deezer","YouTube", "SoundCloud" ])
            return { "name": game, "type": 2 }
            

class CreateWebsocket(object):
    def __init__(self, token:str):
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        response = ws.recv()
        event = json.loads(response)
        auth = {'op': 2, 'd': {'token': token, 'capabilities': 61, 'properties': {'os': 'Windows', 'browser': 'Chrome', 'device': '',  'system_locale': 'en-GB', 'browser_user_agent': config['useragent'], 'browser_version': '90.0.4430.212', 'os_version': '10', 'referrer': '', 'referring_domain': '', 'referrer_current': '', 'referring_domain_current': '', 'release_channel': 'stable', 'client_build_number': '85108', 'client_event_source': 'null'}, 'presence': {'status': random.choice(['online', 'dnd', 'idle']), 'game': Utils.GetRandomGame(), 'since': 0, 'activities': [], 'afk': False}, 'compress': False, 'client_state': {'guild_hashes': {}, 'highest_last_message_id': '0', 'read_state_version': 0, 'user_guild_settings_version': -1}}};
        ws.send(json.dumps(auth))

class SolveCaptcha(object):
    def init(proxy, site_url, site_key):
        global solved
        captcha_key = httpx.post('http://65.109.64.111:6969/solve', json={ 'site_url': None, 'site_key': None, 'proxy_url': proxy }, timeout=None).text
        if "P0_" in captcha_key:
            solved += 1
            TitleWorkerr()
            Logger.Debug(f"Solved hCaptcha : {captcha_key[:40]}...")
            return captcha_key
        else:
            return False

def GenerateToken(key, proxy, thread_id):
    try:
        global genned, solved, errors, verified

        client = httpx.Client(http2=True,timeout=3, proxies={"all://": f"http://{proxy}"})
    
        response = client.get("https://discord.com/register", headers={'user-agent': config['useragent']}, timeout=20)

        dcfduid = response.headers['Set-Cookie'].split('__dcfduid=')[1].split(';')[0]
        sdcfduid = response.headers['Set-Cookie'].split('__sdcfduid=')[1].split(';')[0]
        cookie_header = f'__dcfduid={dcfduid}; __sdcfduid={sdcfduid}'

        registerheaders  = { "Host":"discord.com", "User-Agent": config['useragent'], "Accept":"*/*", "Accept-Language":"en-US,en;q=0.5", "Accept-Encoding":"gzip,", "Content-Type":"application/json", "X-Track": config['x_super_properties'], "X-Fingerprint": config['x_fingerprint'], "Origin":"https://discord.com", "Alt-Used":"discord.com", "Connection":"keep-alive", "Referer":"https://discord.com/", 'Cookie': cookie_header, "Sec-Fetch-Dest":"empty", "Sec-Fetch-Mode":"cors", "Sec-Fetch-Site":"same-origin", "TE":"trailers"}
        account_email = Utils.CreateEmail()
        account_password = "SpaceGenxD!!??"
        account_username = Utils.GetUsername()#Utils.RandomCharacter(5) + ' | .gg/norobots'
    
        payload = { "email": account_email, "password": account_password, "date_of_birth": Utils.GenerateBornDate(), "username": account_username, "consent": True, "captcha_key": key, 'fingerprint': config['x_fingerprint'], "invite": config['invite_code']}

        response = client.post('https://discord.com/api/v9/auth/register', headers=registerheaders, json=payload, timeout=20)

        if response.status_code == 201:
            token = response.json()['token']
            Logger.Success(f"Created Token : {token}")
            genned = genned + 1
            file = open(f'output/{config["invite_code"]}.txt', 'a')
            file.write(f'{token}\n')
            TitleWorkerr()
            CreateWebsocket(token)
        else:
            TitleWorkerr()
            if 'captcha' in response.text:
                errors = errors + 1
                Logger.Error('Invalid Captcha Response, Retrying...')
            else:
                errors = errors + 1
                Logger.Error(response.json())
    except Exception as e:
        TitleWorkerr()
        errors = errors + 1
        Logger.Error(e)


def StartThread(thread_id,solver_address=None):
    while True:
        try:
            proxy =  Utils.GetProxy()
            proxy_raw = proxy
            proxy_formated = Utils.GetFormattedProxy(proxy_raw)
            key = SolveCaptcha.init(proxy_formated,   "https://discord.com/register" , "4c672d35-0701-42b2-88c3-78380b0db560")

            if key != False and key != 0 and key !="0":
                threading.Thread(target=GenerateToken,args=[key,proxy_formated,thread_id] ).start()

        except Exception as e:
            Logger.Error(e)

def StartGenerator():
    global threads
    
    try:
        Logger.Console()
        Logger.Question("How many threads do you want ? ")
        threads = int(input(''))
    except:
        Logger.Error("Please enter a valid number")
        os._exit(1)

    thread_running = threads
        
    with ThreadPoolExecutor(max_workers=threads) as exe:
        for x in range(threads):
            exe.map(StartThread,[x])

class CreatorUtils(object):
    def __init__(self, token):
        self.client = httpx.Client(headers={ "Authorization": token }, proxies=Utils.GetProxy())
        self.token = token
    
    def _get_headers(self, type):
        if type == "register":
            return { "Host":"discord.com", "User-Agent": config['useragent'], "Accept":"*/*", "Accept-Language":"en-US,en;q=0.5", "Accept-Encoding":"gzip,", "Content-Type":"application/json", "X-Track": config['x_super_properties'], "X-Fingerprint": config['x_fingerprint'], "Origin":"https://discord.com", "Alt-Used":"discord.com", "Connection":"keep-alive", "Referer":"https://discord.com/", 'Cookie': None, "Sec-Fetch-Dest":"empty", "Sec-Fetch-Mode":"cors", "Sec-Fetch-Site":"same-origin", "TE":"trailers"}
        elif type == "update_profile":
            return { }
    
    def _add_bio(self, bio):
        response  = self.client.patch('https://discord.com/api/v9/users/@me', headers=self._get_headers("update_profile"))
        print(response.json())

StartGenerator()