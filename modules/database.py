from pony.orm import Database, PrimaryKey, Required

db = Database("sqlite", "../fsinchatbot.db", create_db=True)


class Counter(db.Entity):
    msgId = PrimaryKey(str)
    count = Required(int, default=0)


db.generate_mapping(create_tables=True)
