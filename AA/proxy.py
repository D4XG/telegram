import os, concurrent.futures, time, threading, random, string, json, ctypes, sys
try:
    import requests, colorama, pystyle, datetime, aiosocks, asyncio, aiohttp_socks, socks, socket, tls_client
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install datetime")
    os.system("pip install aiosocks")
    os.system("pip install asyncio")
    os.system("pip install aiohttp-socks")
    os.system("pip install socks")
    os.system("pip install socket")
    os.system("pip install tls_client")

from pystyle import Write, System, Colors, Colorate, Anime
from colorama import Fore, Style
from datetime import datetime
from aiohttp_socks import ProxyConnector, ProxyType

https_scraped = 0
socks4_scraped = 0
socks5_scraped = 0

http_checked = 0
socks4_checked = 0
socks5_checked = 0

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT
output_lock = threading.Lock()

def get_time_rn():
    date = datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def update_title():
    global https_scraped, socks4_scraped, socks5_scraped
    ctypes.windll.kernel32.SetConsoleTitleW(f"[ LunusBPS ] By H4cK3dR4Du & 452b | HTTP/s Scraped : {https_scraped} ~ Socks4 Scraped : {socks4_scraped} ~ Socks5 Scraped : {socks5_scraped}")

def update_title2():
    global https_scraped, socks4_scraped, socks5_scraped
    ctypes.windll.kernel32.SetConsoleTitleW(f"[ LunusBPS ] By H4cK3dR4Du & 452b | HTTP/s Valid : {http_checked} ~ Socks4 Valid : {socks4_checked} ~ Socks5 Valid : {socks5_checked}")

def ui():
    ctypes.windll.kernel32.SetConsoleTitleW(f"[ LunusBPS ] By H4cK3dR4Du & 452b | HTTP/s Valid : {http_checked} ~ Socks4 Valid : {socks4_checked} ~ Socks5 Valid : {socks5_checked}")
    System.Clear()
    Write.Print(f"""
Hi.                                                                      
""", Colors.red_to_blue, interval=0.000)
    time.sleep(3)

ui()
http_links = [
    "https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://proxyspace.pro/https.txt",
    "http://rootjazz.com/proxies/proxies.txt",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=https",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "http://worm.rip/http.txt",
    "https://openproxylist.xyz/http.txt",
    "http://alexa.lr2b.com/proxylist.txt",
    "https://proxyspace.pro/http.txt",
    "https://proxyspace.pro/https.txt"
    "https://proxy-spider.com/api/proxies.example.txt",
    "https://multiproxy.org/txt_all/proxy.txt",
]

socks4_list = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
    "https://api.openproxylist.xyz/socks4.txt",
    "https://proxyspace.pro/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://proxyspace.pro/socks4.txt",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
    "https://www.proxyscan.io/download?type=socks4",
]

socks5_list = [
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
    "https://proxyspace.pro/socks5.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
    "https://spys.me/socks.txt",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
]

def scrape_proxy_links_https(link):
    global https_scraped
    response = requests.get(link)
    if response.status_code == 200:
        with output_lock:
            time_rn = get_time_rn()
            print(f'[ {pink}{time_rn}{reset} ] | ( {green}SUCCESS{reset} ) {pretty}Scraped -->')
            sys.stdout.flush()
            Write.Print(link[:60] + "*******\n", Colors.purple_to_red, interval=0.000)
        proxies = response.text.splitlines()
        https_scraped += len(proxies)
        update_title()
        return proxies
    return []

proxies = []
num_threads = 100
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = executor.map(scrape_proxy_links_https, http_links)
    for result in results:
        proxies.extend(result)

with open("http_proxies.txt", "w") as file:
    for proxy in proxies:
        if ":" in proxy and not any(c.isalpha() for c in proxy):
            file.write(proxy + "\n")

def scrape_proxy_links_socks4(link):
    global socks4_scraped
    response = requests.get(link)
    if response.status_code == 200:
        with output_lock:
            time_rn = get_time_rn()
            print(f'[ {pink}{time_rn}{reset} ] | ( {green}SUCCESS{reset} ) {pretty}Scraped -->')
            sys.stdout.flush()
            Write.Print(link[:60] + "*******\n", Colors.purple_to_red, interval=0.000)
        proxies = response.text.splitlines()
        socks4_scraped += len(proxies)
        update_title()
        return proxies
    return []

proxies = []
num_threads = 100
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = executor.map(scrape_proxy_links_socks4, socks4_list)
    for result in results:
        proxies.extend(result)

with open("socks4_proxies.txt", "w") as file:
    for proxy in proxies:
        if ":" in proxy and not any(c.isalpha() for c in proxy):
            file.write(proxy + "\n")

def scrape_proxy_links_socks5(link):
    global socks5_scraped
    response = requests.get(link)
    if response.status_code == 200:
        with output_lock:
            time_rn = get_time_rn()
            print(f'[ {pink}{time_rn}{reset} ] | ( {green}SUCCESS{reset} ) {pretty}Scraped -->')
            sys.stdout.flush()
            Write.Print(link[:60] + "*******\n", Colors.purple_to_red, interval=0.000)
        proxies = response.text.splitlines()
        socks5_scraped += len(proxies)
        update_title()
        return proxies
    return []

proxies = []
num_threads = 100
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = executor.map(scrape_proxy_links_socks5, socks5_list)
    for result in results:
        proxies.extend(result)

with open("socks5_proxies.txt", "w") as file:
    for proxy in proxies:
        if ":" in proxy and not any(c.isalpha() for c in proxy):
            file.write(proxy + "\n")

time.sleep(1)
nameFile = f"Results"
if not os.path.exists(nameFile):
    os.mkdir(nameFile)

a = open("http.txt", "w")
b = open("socks4.txt", "w")
c = open("socks5.txt", "w")

a.write("")
b.write("")
c.write("")

a.close()
b.close()
c.close()

valid_http = []
valid_socks4 = []
valid_socks5 = []

def check_proxy_http(proxy):
    global http_checked

    proxy_dict = {
        "http": "http://" + proxy,
        "https": "https://" + proxy
    }
    
    try:
        url = "http://httpbin.org/get" 
        r = requests.get(url, proxies=proxy_dict, timeout=30)
        if r.status_code == 200:
            with output_lock:
                time_rn = get_time_rn()
                print(f'[ {pink}{time_rn}{reset} ] | ( {green}VALID{reset} ) {pretty}HTTP/S -->')
                sys.stdout.flush()
                Write.Print(proxy + "\n", Colors.cyan_to_blue, interval=0.000)
            valid_http.append(proxy)
            http_checked += 1
            update_title2()
            with open(f"http.txt", "a+") as f:
                f.write(proxy + "\n")
    except requests.exceptions.RequestException as e:
        pass

def checker_proxy_socks4(proxy):
    global socks4_checked
    try:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, proxy.split(":")[0], int(proxy.split(":")[1]))
        socket.socket = socks.socksocket
        socket.create_connection(("www.google.com", 443), timeout=5)
        socks4_checked += 1
        update_title2()
        with output_lock:
            time_rn = get_time_rn()
            print(f'[ {pink}{time_rn}{reset} ] | ( {green}VALID{reset} ) {pretty}SOCKS4 -->')
            sys.stdout.flush()
            Write.Print(proxy + "\n", Colors.cyan_to_blue, interval=0.000)
        with open("socks4.txt", "a+") as f:
            f.write(proxy + "\n")
    except (socks.ProxyConnectionError, socket.timeout, OSError):
        pass

def checker_proxy_socks5(proxy):
    global socks5_checked
    try:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy.split(":")[0], int(proxy.split(":")[1]))
        socket.socket = socks.socksocket
        socket.create_connection(("www.google.com", 443), timeout=5)
        socks5_checked += 1
        update_title2()
        with output_lock:
            time_rn = get_time_rn()
            print(f'[ {pink}{time_rn}{reset} ] | ( {green}VALID{reset} ) {pretty}SOCKS5 -->')
            sys.stdout.flush()
            Write.Print(proxy + "\n", Colors.cyan_to_blue, interval=0.000)
        with open("socks5.txt", "a+") as f:
            f.write(proxy + "\n")
    except (socks.ProxyConnectionError, socket.timeout, OSError):
        pass

def check_all(proxy_type, pathTXT):
    with open(pathTXT, "r") as f:
        proxies = f.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxies)) as executor:
        if proxy_type.startswith("http") or proxy_type.startswith("https"):
            executor.map(check_proxy_http, proxies)
        if proxy_type.startswith("socks4"):
            executor.map(checker_proxy_socks4, proxies)
        if proxy_type.startswith("socks5"):
            executor.map(checker_proxy_socks5, proxies)

def LetsCheckIt(proxy_types):
    threadsCrack = []
    for proxy_type in proxy_types:
        if os.path.exists(f"{proxy_type}_proxies.txt"):
            t = threading.Thread(target=check_all, args=(proxy_type, f"{proxy_type}_proxies.txt"))
            t.start()
            threadsCrack.append(t)
    for t in threadsCrack:
        t.join()


proxy_types = ["http", "socks4", "socks5"]
LetsCheckIt(proxy_types)


os.remove("http_proxies.txt")
os.remove("socks4_proxies.txt")
os.remove("socks5_proxies.txt")
input()