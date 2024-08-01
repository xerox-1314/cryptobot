import sqlite3
con = sqlite3.connect('crypto_db.db', check_same_thread=False)
cur = con.cursor()


def change_info(chat_id, procent, last_price):
    res = cur.execute(f"SELECT * FROM chats WHERE chat_id = '{chat_id}'").fetchall()
    if len(res) == 0:
        cur.execute(f"INSERT INTO chats (chat_id, procent, last_price) VALUES ('{chat_id}', '{procent}', '{last_price}')")
        con.commit()
    else:
        cur.execute(f"UPDATE chats SET procent='{procent}', last_price='{last_price}' WHERE chat_id='{chat_id}'")
        con.commit()


def get_info(chat_id):
    res = cur.execute(f"SELECT procent, last_price FROM chats WHERE chat_id='{chat_id}'").fetchall()[0]
    return res