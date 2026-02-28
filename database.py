import sqlite3 as sq

with sq.connect("test.db") as con:
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_nickname TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_geolocation TEXT NOT NULL,
        rating REAL DEFAULT 5.0
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS ads (
        ad_id INTEGER PRIMARY KEY AUTOINCREMENT,
        seller_id INTEGER,
        seller_geolocation TEXT NOT NULL,
        title TEXT NOT NULL,
        price INTEGER NOT NULL,
        description TEXT,
        category TEXT NOT NULL,
        FOREIGN KEY (seller_id) REFERENCES users (user_id)
    )""")

    def register_user(nickname, email, password, geo):
        try:
            cur.execute("INSERT INTO users (user_nickname, email, password, user_geolocation) VALUES (?, ?, ?, ?)", (nickname, email, password, geo))
            con.commit()
            print(f"Пользователь {nickname} добавлен в базу данных")
        except sq.IntegrityError:
            print("Ошибка: почта занята другим пользователем")

    def login_user(email, password):
        try:
            cur.execute("SELECT email, password FROM users WHERE email = ?", (email,))
            result = cur.fetchone()
            if result is not None:
                if result[1]==password:
                    print("Вы успешно авторизировались!")
                    return True
                else:
                    print("Ошибка: Неверный логин или пароль.")
                    return False
            else:
                print("Ошибка: Неверный логин или пароль.")
                return False
        except sq.Error as e:
            print(f"Ошибка: {e}")
            return False
             
        

    
   

    

