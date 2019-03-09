# coding=utf8
""" DateSchema adapters for sqlite3
Store as bytes instead of str due to lead-zero-string, like "0199902040".
"""
import sqlite3

from borax.calendars.festivals import DateSchema, SolarSchema, LunarSchema, DateSchemaFactory


def adapt_schema(festival):
    return festival.encode().encode()


def convert_(raw):
    return DateSchemaFactory.decode(raw.decode())


sqlite3.register_adapter(DateSchema, adapt_schema)
sqlite3.register_adapter(SolarSchema, adapt_schema)
sqlite3.register_adapter(LunarSchema, adapt_schema)
sqlite3.register_converter("festival", convert_)


def lunardate_sqlite3_demo():
    con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute('CREATE TABLE festival_cn (pid INT AUTO_INCREMENT PRIMARY KEY,mdate festival);')

    dates = [
        LunarSchema(year=2001, month=12, day=3),
        SolarSchema(year=1999, month=2, day=4),
    ]

    for festival in dates:
        cur.execute("INSERT INTO festival_cn(mdate) VALUES (?);", (festival,))
    cur.execute("SELECT pid, mdate FROM festival_cn;")
    schema = cur.fetchmany()[0][1]
    cur.close()
    con.close()
    print(schema)


if __name__ == '__main__':
    lunardate_sqlite3_demo()
