import hashlib
import psycopg2  # type: ignore
from psycopg2 import sql  # type: ignore

import config


def get_hash(s: str) -> str:
    return (
        hashlib.md5(s.encode(errors="replace"))
        .digest()
        .decode(errors="replace")
    )


def main():
    # fmt: off
    with psycopg2.connect(dbname=config.DB_NAME,
                          user=config.DB_USER,
                          password=config.DB_PASSWORD,
                          host=config.DB_HOST
                          ) as conn:
        with conn.cursor() as cursor:
            # Users
            stmt = sql.SQL("CREATE TABLE users ("
                           "user_id BIGSERIAL NOT NULL PRIMARY KEY, "
                           "first_name TEXT NOT NULL, "
                           "second_name TEXT NOT NULL, "
                           "patronymic TEXT, "
                           "birthday INT, "
                           "email TEXT NOT NULL UNIQUE, "
                           "phone TEXT NOT NULL UNIQUE, "
                           "password TEXT NOT NULL, "
                           "role INT NOT NULL, "
                           "points INT NOT NULL, "
                           "status INT NOT NULL"
                           ");")
            cursor.execute(stmt)
            stmt = sql.SQL("INSERT INTO users (first_name, second_name, birthday, email, phone, password, role, points, status) VALUES "
                           "('Kirill', 'Kim', 805791292, 'test01@migra.net', '+79111112233', '%s', 3, 0, 1),"
                           "('Целищев', 'Никита', 900399313, 'test02@migra.net', '+79111112234', '%s', 1, 1000, 1);" % (get_hash("админ"), get_hash("Nick")))
            cursor.execute(stmt)
            stmt = sql.SQL("INSERT INTO users (first_name, second_name, patronymic, birthday, email, phone, password, role, points, status) VALUES "
                           "('Кривуля', 'Святослав', 'Валерьевич', 931935342, 'test03@migra.net', '+79111112235', '%s', 2, 100, 1);" % (get_hash("читер")))
            cursor.execute(stmt)
            # Friends
            stmt = sql.SQL("CREATE TABLE friends ("
                           "source_user_id BIGINT NOT NULL, "
                           "target_user_id BIGINT NOT NULL, "
                           "UNIQUE(source_user_id, target_user_id), "
                           "FOREIGN KEY (source_user_id) REFERENCES users (user_id) ON DELETE CASCADE,"
                           "FOREIGN KEY (target_user_id) REFERENCES users (user_id) ON DELETE CASCADE"
                           ");")
            cursor.execute(stmt)
            cursor.execute(
                "INSERT INTO friends (source_user_id, target_user_id) VALUES (1, 2), (2, 1);")
            # Waiting to be added to friends
            cursor.execute(sql.SQL("CREATE TABLE wait_friend_add ("
                           "source_user_id BIGINT NOT NULL, "
                           "target_user_id BIGINT NOT NULL, "
                            "UNIQUE(source_user_id, target_user_id), "
                           "FOREIGN KEY (source_user_id) REFERENCES users (user_id) ON DELETE CASCADE,"
                           "FOREIGN KEY (target_user_id) REFERENCES users (user_id) ON DELETE CASCADE"
                           ");"))
            # Block
            cursor.execute(sql.SQL("CREATE TABLE blocked_by_user ("
                                   "source_user_id BIGINT NOT NULL, "
                                   "target_user_id BIGINT NOT NULL, "
                                   "UNIQUE(source_user_id, target_user_id), "
                                   "FOREIGN KEY (source_user_id) REFERENCES users (user_id) ON DELETE CASCADE,"
                                   "FOREIGN KEY (target_user_id) REFERENCES users (user_id) ON DELETE CASCADE"
                                   ");"))
            # Single chat
            # TODO: add creator
            cursor.execute("CREATE TABLE chat_ids(chat_id BIGINT NOT NULL PRIMARY KEY,"
                           "owner BIGINT NOT NULL, "
                           "chat_name TEXT NOT NULL, "
                           "FOREIGN KEY (owner) REFERENCES users (user_id) ON DELETE CASCADE"
                           ");")
            
            #insert into chat_ids
            cursor.execute(sql.SQL("insert into chat_ids values (2, 1, 'Футболисты' );"))
            cursor.execute(sql.SQL("insert into chat_ids values (3, 2, 'Баскетболисты');"))
            cursor.execute(sql.SQL("insert into chat_ids values (4, 3, 'Волейбол');"))
            cursor.execute(sql.SQL("insert into chat_ids values (5, 1, 'Музей');"))
            cursor.execute(sql.SQL("insert into chat_ids values (6, 2, 'Геймеры');"))          
            stmt = sql.SQL("CREATE TABLE chats (user_id BIGINT NOT NULL, "
                           "chat_id BIGINT NOT NULL, "
                           "UNIQUE (user_id, chat_id), "
                           "FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,"
                           "FOREIGN KEY (chat_id) REFERENCES chat_ids (chat_id) ON DELETE CASCADE"
                           ");")
            cursor.execute(stmt) 
            #insert into chats
            cursor.execute(sql.SQL("Insert into chats values (1, 2);"))
            cursor.execute(sql.SQL("Insert into chats values (2, 2);"))
            cursor.execute(sql.SQL("Insert into chats values (3, 2);"))
            cursor.execute(sql.SQL("Insert into chats values (1, 3);"))
            cursor.execute(sql.SQL("Insert into chats values (2, 3);"))
            cursor.execute(sql.SQL("Insert into chats values (3, 3);"))
            cursor.execute(sql.SQL("Insert into chats values (1, 4);"))
            cursor.execute(sql.SQL("Insert into chats values (2, 4);"))
            cursor.execute(sql.SQL("Insert into chats values (3, 4);"))
            cursor.execute(sql.SQL("Insert into chats values (1, 5);"))
            cursor.execute(sql.SQL("Insert into chats values (2, 5);"))
            cursor.execute(sql.SQL("Insert into chats values (3, 5);"))
            cursor.execute(sql.SQL("Insert into chats values (1, 6);"))
            cursor.execute(sql.SQL("Insert into chats values (2, 6);"))
            cursor.execute(sql.SQL("Insert into chats values (3, 6);")) 
            # Single message
            cursor.execute(sql.SQL("CREATE TABLE chat_messages ("
                                   "chat_id BIGINT NOT NULL, "
                                   "from_user_id BIGINT NOT NULL, "
                                   "message TEXT NOT NULL,"
                                   "read BOOL NOT NULL, "
                                   "time BIGINT NOT NULL,"
                                   "FOREIGN KEY (chat_id) REFERENCES chat_ids (chat_id) ON DELETE CASCADE,"
                                   "FOREIGN KEY (from_user_id) REFERENCES users (user_id) ON DELETE CASCADE"
                                   ");")) 
            #insert into chat_messages						   		 
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 1, 'Давайте сегодня поиграем в футбол?', True, 1593582860);"))								   
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 1, 'Я предлагаю, как обычно в 18:00', True, 1593583160);"))
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 2, 'Я буду, но опоздаю', True, 1593583560);"))							
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 3, 'Я тоже буду', True, 1593583960);"))								   
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 1, 'Возьмите мяч', True, 1593584160);"))							   
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 3, 'Хорошо', True, 1593585160);"))								   
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 3, 'А ты возьми воды', True, 1593585160);"))								   
            cursor.execute(sql.SQL("Insert into chat_messages values ( 2, 1,'Ок', True, 1593585360);"))								   
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 2, 'Опоздаю на 30 минут', True, 1593586760);"))								   
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 2, 'Извините', True, 1593586810);"))								   
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 1, 'Не страшно. Я приведу 2 друзей с работы', True, 1593586830);"))								  
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 1, 'Покажем им это приложение, чтобы они тоже в чате были', True, 1593586840);"))								   
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 2, 'Ок', True, 1593586810);"))								   
            cursor.execute(sql.SQL("Insert into chat_messages values (2, 2, 'До встречи', True, 1593586810);"))
            cursor.execute(sql.SQL("Insert into chat_messages values (3, 3, 'Сегодня в баскетбол?', True, 1593582860);"))
            cursor.execute(sql.SQL("Insert into chat_messages values (3, 3, 'Кто в деле?', True, 1593582890);"))
            cursor.execute(sql.SQL("Insert into chat_messages values (3, 1, 'я', True, 1593582890);"))
            # Actions
            cursor.execute(sql.SQL("CREATE TABLE actions ("
                                   "action_id BIGINT NOT NULL, "
                                   "name TEXT NOT NULL, "
                                   "latitude FLOAT NOT NULL,"
                                   "longitude FLOAT NOT NULL,"
                                   "owner BIGINT NOT NULL, "
                                   "description TEXT NOT NULL, "
                                   "chat_id BIGINT NOT NULL, "
                                   "creation_time BIGINT NOT NULL, "
                                   "action_time  BIGINT NOT NULL, "
                                   "PRIMARY KEY (action_id), "
                                   "FOREIGN KEY (owner) REFERENCES users (user_id) ON DELETE CASCADE, "
                                   "FOREIGN KEY (chat_id) REFERENCES chat_ids (chat_id) ON DELETE CASCADE"
                                   ");"))
            #insert into actions									  
            cursor.execute(sql.SQL("insert into actions values (36, 'Футбол на Ломоносовской', 59.88005312, 30.43818982, 2, 'Играем в футбол 5 на 5 в 19:00', 2, 1593410060, 1593619200);"))
            cursor.execute(sql.SQL("CREATE TABLE action_members ("
                                   "user_id BIGINT NOT NULL, "
                                   "action_id BIGINT NOT NULL, "
                                   "UNIQUE(user_id, action_id), "
                                   "FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE, "
                                   "FOREIGN KEY (action_id) REFERENCES actions (action_id) ON DELETE CASCADE"
                                   ");"))
            #insert into action_members		
            cursor.execute(sql.SQL("Insert into action_members values (1, 36);"))							 					   
            cursor.execute(sql.SQL("Insert into action_members values (2, 36);"))								 						   
            cursor.execute(sql.SQL("Insert into action_members values (3, 36);"))
            # Crime detector
            cursor.execute(sql.SQL("CREATE TABLE geolocations ("
                                   "user_id BIGINT NOT NULL,"
                                   "latitude FLOAT,"
                                   "longitude FLOAT,"
                                   "time INT,"
                                   "FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE"
                                   ");"))
            # Actives
            cursor.execute(sql.SQL("CREATE TABLE user_sessions ("
                                   "user_id BIGINT NOT NULL UNIQUE,"
                                   "user_session BIGINT NOT NULL UNIQUE,"
                                   "start_timestamp INT,"
                                   "FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,"
                                   "PRIMARY KEY (user_id)"
                                   ");"))
    # fmt: on


if __name__ == "__main__":
    main()
