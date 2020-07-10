import time
from typing import *
from random import randint
from logging import Logger, getLogger

from database_engines import PostgreSQL as PostgreSQLEngine

import constants


MAX_RANDOM_VALUE = 9999999999


class NullDatabase:
    def user_get_id_by_phone(self, phone: str) -> List[Dict[str, Any]]:
        return NotImplemented

    def user_get_id_by_email(self, email: str) -> List[Dict[str, Any]]:
        return NotImplemented

    def user_get_by_email(self, email: str) -> List[Dict[str, Any]]:
        return NotImplemented

    def user_get_by_phone(self, phone: str) -> List[Dict[str, Any]]:
        return NotImplemented

    def user_get_by_id(self, user_id: int) -> List[Dict[str, Any]]:
        return NotImplemented

    def user_create(
        self,
        first_name: str,
        second_name: str,
        birthday: int,
        password: str,
        phone: str,
        email: str,
        role: constants.Roles,
        points: int,
        status: constants.Status,
        patronymic: Optional[str],
    ) -> Any:
        return NotImplemented

    def user_set_online(self, user_id: int, session: int) -> None:
        return NotImplemented

    def user_delete(self, user_id: int) -> None:
        return NotImplemented

    def user_get_id_online_by_session(
        self, user_session: int
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def user_get_session_by_id(self, user_id: int) -> List[Dict[str, Any]]:
        return NotImplemented

    def user_get_blocked(self, user_id: int) -> List[Dict[str, Any]]:
        return NotImplemented

    def user_get_blocked_at(self, user_id: int) -> List[Dict[str, Any]]:
        return NotImplemented

    def single_chat_ids_get_by_user_id(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def chat_create(
        self, owner: int, chat_name: str, *user_ids: int
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def single_chat_get_by_chat_id(self, chat_id: int) -> List[Dict[str, Any]]:
        return NotImplemented

    def single_chat_get_by_users_ids(
        self, source_user_id: int, target_user_id: int
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def single_chat_delete_by_user_id_and_chat_id(
        self, chat_id: int, user_id: int
    ) -> None:
        return NotImplemented

    def single_chats_get_by_users_id(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def single_chat_meta_info_get_by_chat_id(
        self, chat_id: int
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def singe_chat_send_message(
        self, chat_id: int, from_user_id: int, message: str
    ) -> None:
        return NotImplemented

    def single_chat_get_messages(
        self,
        chat_id: int,
        message_limit: Optional[int] = None,
        time_from: Optional[int] = None,
        time_to: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def friends_get_all_ids_by_user_id(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def friends_get_to_add_waiter_ids(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def friends_add_to_waiter(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        return NotImplemented

    def friends_add_to_friend(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        return NotImplemented

    def friends_delete_from_waiter(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        return NotImplemented

    def friends_delete(self, source_user_id: int, target_user_id: int) -> None:
        return NotImplemented

    def friends_block_user(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        return NotImplemented

    def friends_find(
        self, simple_keys: Dict[str, Any], difficult_keys: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def action_create(
        self,
        name: str,
        latitude: float,
        longitude: float,
        owner: int,
        users_ids: List[int],
        description: str,
        action_time: int,
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def action_get_users(self, action_id: int) -> List[Dict[str, Any]]:
        return NotImplemented

    def action_get(self, action_id: int) -> List[Dict[str, Any]]:
        return NotImplemented

    def action_find(
        self,
        latitude: float,
        longitude: float,
        r: float,
        delta_time: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def user_get_actions(self, user_id: int) -> List[Dict[str, Any]]:
        return NotImplemented

    def action_get_by_action_and_user_id(
        self, action_id: int, user_id: int
    ) -> List[Dict[str, Any]]:
        return NotImplemented

    def action_add_user(self, action_id: int, user_id: int) -> None:
        return NotImplemented

    def user_add_to_chat(self, user_id: int, chat_id: int) -> None:
        return NotImplemented

    def user_leave_action(self, user_id: int, action_id: int) -> None:
        return NotImplemented

    def user_leave_chat(self, user_id: int, chat_id: int) -> None:
        return NotImplemented


class Database(PostgreSQLEngine):
    def user_get_id_by_phone(self, phone: str) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.USERS_DB, "phone='%s'" % phone, ["user_id"]
        )

    def user_get_id_by_email(self, email: str) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.USERS_DB, "email='%s'" % email, ["user_id"]
        )

    def user_get_by_email(self, email: str) -> List[Dict[str, Any]]:
        return self.get_from_where(constants.USERS_DB, "email='%s'" % email)

    def user_get_by_phone(self, phone: str) -> List[Dict[str, Any]]:
        return self.get_from_where(constants.USERS_DB, "phone='%s'" % phone)

    def user_get_by_id(self, user_id: int) -> List[Dict[str, Any]]:
        return self.get_from_where(constants.USERS_DB, "user_id=%d" % user_id)

    def user_create(
        self,
        first_name: str,
        second_name: str,
        birthday: int,
        password: str,
        phone: str,
        email: str,
        role: constants.Roles,
        points: int,
        status: constants.Status,
        patronymic: Optional[str] = None,
    ) -> Any:
        data = {
            "first_name": first_name,
            "second_name": second_name,
            "password": password,
            "birthday": birthday,
            "phone": phone,
            "email": email,
            "role": int(role),
            "points": points,
            "status": int(status),
        }
        if patronymic is not None:
            data["patronymic"] = patronymic
        self.insert_value("users", data)
        return self.user_get_id_by_email(email)[0]["user_id"]

    def user_set_online(self, user_id: int, session: int) -> None:
        self.insert_value(
            constants.USER_SESSION_DB,
            {
                "user_id": user_id,
                "start_timestamp": int(time.time()),
                "user_session": session,
            },
        )

    def user_delete(self, user_id: int) -> None:
        self.delete_from_where(constants.USERS_DB, "user_id=%d" % user_id)

    def user_get_id_online_by_session(
        self, user_session: int
    ) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.USER_SESSION_DB,
            "user_session=%d" % user_session,
            ["user_id"],
        )

    def user_get_session_by_id(self, user_id: int) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.USER_SESSION_DB, "user_id=%d" % user_id, ["user_session"]
        )

    def user_get_blocked(self, user_id: int) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.BLOCKED_BY_USER_DB,
            "source_user_id=%s" % user_id,
            ["target_user_id"],
        )

    def user_get_blocked_at(self, user_id: int) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.BLOCKED_BY_USER_DB,
            "target_user_id=%s" % user_id,
            ["source_user_id"],
        )

    def single_chat_ids_get_by_user_id(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.SINGLE_CHATS_DB, "user_id=%d" % user_id, ["chat_id"]
        )

    def chat_create(
        self, owner: int, chat_name: str, *user_ids: int
    ) -> List[Dict[str, Any]]:
        while True:
            chat_id = randint(1, MAX_RANDOM_VALUE)
            if not self.get_from_where(
                constants.SINGLE_CHAT_IDS_DB, "chat_id=%s" % chat_id
            ):
                break
        self.insert_value(
            constants.SINGLE_CHAT_IDS_DB,
            {"chat_id": chat_id, "chat_name": chat_name, "owner": owner},
        )
        data = [{"chat_id": chat_id, "user_id": owner}]
        for u_d in user_ids:
            data.append({"chat_id": chat_id, "user_id": u_d})
        self.mass_insert_values(constants.SINGLE_CHATS_DB, data)
        return [{"chat_id": chat_id}]

    def single_chat_get_by_chat_id(self, chat_id: int) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.SINGLE_CHATS_DB, "chat_id=%d" % chat_id
        )

    def single_chats_get_by_users_id(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.SINGLE_CHATS_DB, "user_id=%d" % user_id, ["chat_id"],
        )

    def single_chat_delete_by_user_id_and_chat_id(
        self, chat_id: int, user_id: int
    ) -> None:
        self.delete_from_where(
            constants.SINGLE_CHATS_DB,
            "user_id=%d AND chat_id=%d" % (user_id, chat_id),
        )

    def single_chat_meta_info_get_by_chat_id(
        self, chat_id: int
    ) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.SINGLE_CHAT_IDS_DB, "chat_id=%d" % chat_id
        )

    def singe_chat_send_message(
        self, chat_id: int, from_user_id: int, message: str
    ) -> None:
        self.insert_value(
            constants.SINGLE_CHAT_MESSAGES_DB,
            {
                "chat_id": chat_id,
                "from_user_id": from_user_id,
                "message": message,
                "time": int(time.time()),
                "read": False,
            },
        )

    def single_chat_get_messages(
        self,
        chat_id: int,
        message_limit: Optional[int] = None,
        time_from: Optional[int] = None,
        time_to: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        condition = "%s"
        if message_limit is not None:
            condition %= "%s LIMIT {}".format(message_limit)
        if time_from is not None:
            condition %= "%s AND time >= {}".format(time_from)
        if time_to is not None:
            condition %= "%s AND time <= {}".format(time_to)
        return self.get_from_where(
            constants.SINGLE_CHAT_MESSAGES_DB,
            condition % ("chat_id=%d" % chat_id),
        )

    def friends_get_all_ids_by_user_id(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.FRIENDS_DB,
            "source_user_id=%s" % user_id,
            ["target_user_id"],
        )

    def friends_get_to_add_waiter_ids(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.FRIENDS_WAIT_FRIEND_ADD,
            "target_user_id=%d" % user_id,
            ["source_user_id"],
        )

    def friends_add_to_waiter(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        self.insert_value(
            constants.FRIENDS_WAIT_FRIEND_ADD,
            {
                "source_user_id": source_user_id,
                "target_user_id": target_user_id,
            },
        )

    def friends_add_to_friend(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        self.delete_from_where(
            constants.FRIENDS_WAIT_FRIEND_ADD,
            "source_user_id=%d AND target_user_id=%d"
            % (source_user_id, target_user_id),
        )
        self.delete_from_where(
            constants.FRIENDS_WAIT_FRIEND_ADD,
            "source_user_id=%d AND target_user_id=%d"
            % (target_user_id, source_user_id),
        )
        self.mass_insert_values(
            constants.FRIENDS_DB,
            [
                {
                    "source_user_id": source_user_id,
                    "target_user_id": target_user_id,
                },
                {
                    "source_user_id": target_user_id,
                    "target_user_id": source_user_id,
                },
            ],
        )

    def friends_delete_from_waiter(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        self.delete_from_where(
            constants.FRIENDS_WAIT_FRIEND_ADD,
            "source_user_id=%d AND target_user_id=%d"
            % (source_user_id, target_user_id),
        )

    def friends_delete(self, source_user_id: int, target_user_id: int) -> None:
        self.delete_from_where(
            constants.FRIENDS_DB,
            "source_user_id=%d AND target_user_id=%d"
            % (source_user_id, target_user_id),
        )
        self.delete_from_where(
            constants.FRIENDS_DB,
            "source_user_id=%d AND target_user_id=%d"
            % (target_user_id, source_user_id),
        )

    def friends_block_user(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        self.insert_value(
            constants.BLOCKED_BY_USER_DB,
            {
                "source_user_id": source_user_id,
                "target_user_id": target_user_id,
            },
        )

    def friends_find(
        self, simple_keys: Dict[str, Any], difficult_keys: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        results = []
        simple_condition = " AND ".join(
            ["%s='%s'" % (k, v) for k, v in simple_keys.items()]
        )
        if simple_condition:
            results.extend(
                self.get_from_where(
                    constants.USERS_DB, simple_condition, ["user_id"]
                )
            )
        difficult_condition = " AND ".join(
            [
                "%s%s%s" % (method["key"], method["condition"], method["data"])
                for method in difficult_keys
            ]
        )
        if difficult_condition:
            results.extend(
                self.get_from_where(
                    constants.USERS_DB, difficult_condition, ["user_id"]
                )
            )
        return results

    def action_create(
        self,
        name: str,
        latitude: float,
        longitude: float,
        owner: int,
        users_ids: List[int],
        description: str,
        action_time: int,
    ) -> List[Dict[str, Any]]:
        while True:
            action_id = randint(1, MAX_RANDOM_VALUE)
            if not self.get_from_where(
                constants.ACTIONS_DB, "action_id=%s" % action_id
            ):
                break
        chat_id = self.chat_create(owner, name, *users_ids)[0][
            "chat_id"
        ]  # Careful
        self.insert_value(
            constants.ACTIONS_DB,
            {
                "action_id": action_id,
                "name": name,
                "latitude": latitude,
                "longitude": longitude,
                "owner": owner,
                "description": description,
                "chat_id": chat_id,
                "creation_time": int(time.time()),
                "action_time": action_time,
            },
        )
        data = [{"action_id": action_id, "user_id": owner}]
        for u_d in users_ids:
            data.append({"action_id": action_id, "user_id": u_d})
        self.mass_insert_values(constants.ACTION_MEMBERS_DB, data)
        return [{"action_id": action_id}]

    def action_get_users(self, action_id: int) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.ACTION_MEMBERS_DB,
            "action_id=%d" % action_id,
            ["user_id"],
        )

    def action_get(self, action_id: int) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.ACTIONS_DB, "action_id=%d" % action_id
        )

    def action_find(
        self,
        latitude: float,
        longitude: float,
        r: float,
        delta_time: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.ACTIONS_DB,
            "latitude>=%f AND latitude<=%f AND longitude>=%f AND longitude<=%f %s"
            % (
                latitude - r,
                latitude + r,
                longitude - r,
                longitude + r,
                ""
                if delta_time is None
                else ("AND action_time<=%d" % int(time.time() + delta_time)),
            ),
            ["action_id"],
        )

    def user_get_actions(self, user_id: int) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.ACTION_MEMBERS_DB, "user_id=%d" % user_id, ["action_id"]
        )

    def action_get_by_action_and_user_id(
        self, action_id: int, user_id: int
    ) -> List[Dict[str, Any]]:
        return self.get_from_where(
            constants.ACTION_MEMBERS_DB,
            "action_id=%d AND user_id=%d" % (action_id, user_id),
        )

    def action_add_user(self, action_id: int, user_id: int) -> None:
        self.insert_value(
            constants.ACTION_MEMBERS_DB,
            {"action_id": action_id, "user_id": user_id},
        )

    def user_add_to_chat(self, user_id: int, chat_id: int) -> None:
        self.insert_value(
            constants.SINGLE_CHATS_DB, {"user_id": user_id, "chat_id": chat_id}
        )

    def user_leave_action(self, user_id: int, action_id: int) -> None:
        self.delete_from_where(
            constants.ACTION_MEMBERS_DB,
            "user_id=%d AND action_id=%d" % (user_id, action_id),
        )

    def user_leave_chat(self, user_id: int, chat_id: int) -> None:
        self.delete_from_where(
            constants.SINGLE_CHATS_DB,
            "user_id=%d AND chat_id=%d" % (user_id, chat_id),
        )


if __name__ == "__main__":
    import config

    db = Database(
        config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD
    )
    print(db.user_get_id_by_email("test03@migra.net"))
    print(db.user_get_id_by_email("test04@migra.net"))
    result = db.user_get_id_by_phone("+79111112233")
    # I know results =)
    # Don't use this without check =)
    print(result)
    print(db.user_get_by_id(result[0]["user_id"]))
