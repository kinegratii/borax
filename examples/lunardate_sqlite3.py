# coding=utf8

import sqlite3

from borax.calendars.lunardate import LunarDate


def adapt_lunardate(ld):
    return ld.encode()


sqlite3.register_adapter(LunarDate, adapt_lunardate)
sqlite3.register_converter("lunardate", LunarDate.decode)


def lunardate_sqlite3_demo():
    con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute('CREATE TABLE member (pid INT AUTO_INCREMENT PRIMARY KEY,birthday lunardate);')
    ld = LunarDate(2018, 5, 3)
    cur.execute("INSERT INTO member(birthday) VALUES (?)", (ld,))
    cur.execute("SELECT pid, birthday FROM member;")
    my_birthday = cur.fetchone()[1]
    cur.close()
    con.close()
    print(my_birthday)


if __name__ == '__main__':
    lunardate_sqlite3_demo()
