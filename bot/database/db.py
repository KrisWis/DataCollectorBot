import sqlite3

# Функция для инициализации базы данных
def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS bot_data (crypto_draw_is_turned_on BOOLEAN)')
    cursor.execute('INSERT INTO bot_data (crypto_draw_is_turned_on) VALUES (True)')
    conn.commit()
    conn.close()


# Функция для получения того включен ли розыгрыш
def get_crypto_draw_is_turned_on():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT crypto_draw_is_turned_on FROM bot_data')
    value = cursor.fetchone()[0]
    conn.close()
    return value


# Функция для установки того, что розыгрыш включен
def set_crypto_draw_is_turned_on():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE bot_data SET crypto_draw_is_turned_on = True')
    conn.commit()
    conn.close()



# Функция для установки того, что розыгрыш выключен
def set_crypto_draw_is_turned_off():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE bot_data SET crypto_draw_is_turned_on = False')
    conn.commit()
    conn.close()