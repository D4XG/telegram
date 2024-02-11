import telebot
import datetime
import sqlite3
import threading
import requests

bot_token = '6360725690:AAEs3zEAZV28hNDiGhJ7om8Ask8hyMAWpUs'
bot = telebot.TeleBot(bot_token)

# Thiết lập kết nối cơ sở dữ liệu SQLite
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()

# Tạo bảng để lưu thông tin keys
cursor.execute('''
    CREATE TABLE IF NOT EXISTS keys (
        key TEXT PRIMARY KEY,
        expiration_date TEXT,
        used INTEGER
    )
''')
conn.commit()

# Tạo bảng để lưu thông tin người dùng đã nhập key
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        key TEXT,
        expiration_date TEXT
    )
''')
conn.commit()

# Lock để đảm bảo truy cập cơ sở dữ liệu đồng thời từ nhiều luồng
db_lock = threading.Lock()

def run_sms(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 180:
                cmd_process.terminate()
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return

ADMIN_ID = 6425545597
chat_id = -1001620650938

@bot.message_handler(commands=['taokey'])
def generate_key(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        return

    key = message.text.split()[1]
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)

    with db_lock:
        cursor.execute('INSERT INTO keys (key, expiration_date, used) VALUES (?, ?, ?)', (key, expiration_time.strftime('%Y-%m-%d %H:%M:%S'), 0))
        conn.commit()

    bot.reply_to(message, f'Tạo key "{key}" thành công. Key sẽ hết hạn sau 30 ngày.')
active_attacks = {}

@bot.message_handler(commands=['vip'])
def attack_command(message):
    user_id = str(message.from_user.id)

    with db_lock:
        cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        user_info = cursor.fetchone()

        if user_info:
            expiration_date = datetime.datetime.strptime(user_info[3], '%Y-%m-%d %H:%M:%S')
            if expiration_date > datetime.datetime.now():
                args = message.text.split()

                if len(args) < 2:
                    bot.reply_to(message, 'Vui lòng nhập đúng cú pháp.\nVí dụ: /vip + [số điện thoại]')
                    return

                phone_number = args[1]
                bot.reply_to(message, f'Đang tiến hành spam')

                command = ["python", "sms.py", phone_number, "180"]
                duration = 180

                attack_thread = threading.Thread(target=run_sms, args=(phone_number, duration), name=user_id)
                active_attacks[user_id] = attack_thread
                attack_thread.start()

                bot.reply_to(message, f'┏━━━━━━━━━━━━━━┓\n┃   Spam Thành Công!!!\n┗━━━━━━━━━━━━━━➤\n┏━━━━━━━━━━━━━━┓\n┣➤ Phone: {phone_number} \n┣➤ Time: 300 Giây\n┣➤ Plan: VIP \n┣➤ Bot Ver: 2.0\n┗━━━━━━━━━━━━━━➤')
            else:
                bot.reply_to(message, 'Key đã hết hạn. Vui lòng nhập key mới.')
        else:
            bot.reply_to(message, 'Bạn chưa nhập key hoặc key không hợp lệ. Vui lòng nhập key.')

@bot.message_handler(commands=['nhapkey'])
def enter_key(message):
    user_id = message.from_user.id
    key = message.text.split()[1]

    with db_lock:
        cursor.execute('SELECT * FROM keys WHERE key=? AND used=0', (key,))
        key_info = cursor.fetchone()

        if key_info:
            expiration_date = datetime.datetime.strptime(key_info[1], '%Y-%m-%d %H:%M:%S')
            if expiration_date > datetime.datetime.now():
                cursor.execute('UPDATE keys SET used=1 WHERE key=?', (key,))
                cursor.execute('INSERT INTO users (user_id, key, expiration_date) VALUES (?, ?, ?)', (user_id, key, expiration_date.strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
                bot.reply_to(message, f'Nhập key thành công. Bạn có thể sử dụng lệnh /vip trong vòng 30 ngày.')
            else:
                bot.reply_to(message, 'Key đã hết hạn.')
        else:
            bot.reply_to(message, 'Key không hợp lệ hoặc đã được sử dụng.\nBuy Key Tại: shop.viduchung.info')

# Rest of your bot logic

bot.infinity_polling()
