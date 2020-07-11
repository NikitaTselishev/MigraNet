from typing import *
from dataclasses import dataclass

import constants
import exceptions
import interfaces


ONE_MESSAGE = 1


@dataclass
class User:
    user_id: int
    password: str
    first_name: str
    second_name: str
    birthday: int
    phone: str
    email: str
    role: constants.Roles
    points: int
    status: constants.Status
    patronymic: Optional[str] = None

    @classmethod
    def create_from_database(
        cls,
        database: interfaces.Database,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> "User":
        if user_id is not None:
            user_data = database.user_get_by_id(user_id)
        elif phone is not None:
            user_data = database.user_get_by_phone(phone)
        elif email is not None:
            user_data = database.user_get_by_email(email)
        else:
            raise Exception("Nulls arguments!")
        if not user_data:
            raise exceptions.UnknownUserInDatabaseError(
                "Can't find user with id: %s, email: %s, phone: %s"
                % (str(id), str(email), str(phone))
            )
        if len(user_data) > 1:
            raise exceptions.SomethingGoesWrong(
                "Found more than 1... %s; id: %s, email: %s, phone: %s"
                % (str(user_data), str(id), str(email), str(phone))
            )
        return cls(**user_data[0])

    @classmethod
    def create_in_database(
        cls,
        database: interfaces.Database,
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
    ) -> "User":
        user_id = database.user_create(
            first_name=first_name,
            second_name=second_name,
            birthday=birthday,
            password=password,
            phone=phone,
            email=email,
            role=role,
            points=points,
            status=status,
            patronymic=patronymic,
        )
        return cls(
            user_id=user_id,
            first_name=first_name,
            second_name=second_name,
            birthday=birthday,
            password=password,
            phone=phone,
            email=email,
            role=role,
            points=points,
            status=status,
            patronymic=patronymic,
        )

    def convert_to_json(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "second_name": self.second_name,
            "patronymic": self.patronymic,
            "birthday": self.birthday,
        }

    def __hash__(self):
        return self.user_id

    def __eq__(self, other):
        return isinstance(other, User) and other.user_id == self.user_id


@dataclass
class Message:
    chat_id: int
    from_user_id: int
    message: str
    read: bool
    time: int

    def convert_to_json(self) -> Dict[str, Any]:
        return {
            "chat_id": self.chat_id,
            "from_user": self.from_user_id,
            "message": self.message,
            "read": self.read,
            "time": self.time,
        }


@dataclass
class Chat:
    chat_id: int
    chat_name: str
    owner: interfaces.User
    users: List[interfaces.User]
    messages: Optional[List[interfaces.Message]] = None

    def __post_init__(self):
        if self.messages is None:
            self.messages = []

    @classmethod
    def create_from_database(
        cls,
        database: interfaces.Database,
        chat_id: int,
        message_limit: Optional[int] = None,
        time_from: Optional[int] = None,
        time_to: Optional[int] = None,
    ) -> "Chat":
        chat_data = database.single_chat_get_by_chat_id(chat_id)
        users: List[interfaces.User] = []
        for data in chat_data:
            users.append(
                User.create_from_database(database, user_id=data["user_id"])
            )
        meta_data = database.single_chat_meta_info_get_by_chat_id(chat_id)[0]
        owner = User.create_from_database(database, user_id=meta_data["owner"])
        raw_messages = database.single_chat_get_messages(
            chat_id, message_limit, time_from, time_to
        )
        return cls(
            chat_id,
            meta_data["chat_name"],
            owner,
            users,
            [
                Message(
                    chat_id=m["chat_id"],
                    from_user_id=m["from_user_id"],
                    message=m["message"],
                    read=m["read"],
                    time=m["time"],
                )
                for m in raw_messages
            ],
        )

    @classmethod
    def create_in_database(
        cls,
        database: interfaces.Database,
        owner: interfaces.User,
        chat_name: str,
        *users: interfaces.User
    ):
        chat_id = database.chat_create(
            owner.user_id, chat_name, *[u.user_id for u in users]
        )[0]["chat_id"]
        return cls(chat_id, chat_name, owner, list(users), [])

    def convert_to_json(self) -> Dict[str, Any]:
        self.messages = cast(List[interfaces.Message], self.messages)
        return {
            "chat_id": self.chat_id,
            "owner": self.owner.user_id,
            "users": [u.user_id for u in self.users],
            "messages": [m.convert_to_json() for m in self.messages],
        }

    # TODO: Set is good. Don't use list =)
    def delete_user(
        self, database: interfaces.Database, user: interfaces.User
    ) -> None:
        if user in self.users:
            database.user_leave_chat(user.user_id, self.chat_id)
            self.users.pop(self.users.index(user))


@dataclass
class Action:
    action_id: int
    name: str
    latitude: int
    longitude: int
    owner: interfaces.User
    users: List[interfaces.User]
    description: str
    chat: interfaces.Chat
    creation_time: int
    action_time: int

    @classmethod
    def create_from_database(
        cls, database: interfaces.Database, action_id: int
    ) -> interfaces.Action:
        raw_data = database.action_get(action_id)[0]
        data = {
            "action_id": raw_data["action_id"],
            "name": raw_data["name"],
            "latitude": raw_data["latitude"],
            "longitude": raw_data["longitude"],
            "description": raw_data["description"],
            "creation_time": raw_data["creation_time"],
            "action_time": raw_data["action_time"],
            "owner": User.create_from_database(
                database, user_id=raw_data["owner"]
            ),
        }
        user_ids = database.action_get_users(data["action_id"])
        data["users"] = []
        for u_i in user_ids:
            data["users"].append(
                User.create_from_database(database, user_id=u_i["user_id"])
            )
        data["chat"] = Chat.create_from_database(
            database, chat_id=raw_data["chat_id"]
        )  # TODO: Fix bug
        return cls(**data)

    @classmethod
    def create_in_database(
        cls,
        database: interfaces.Database,
        name: str,
        latitude: float,
        longitude: float,
        owner: interfaces.User,
        users: List[interfaces.User],
        description: str,
        action_time: int,
    ) -> interfaces.Action:
        action = database.action_create(
            name=name,
            latitude=latitude,
            longitude=longitude,
            owner=owner.user_id,
            users_ids=[u.user_id for u in users],
            description=description,
            action_time=action_time,
        )[0]
        return cls.create_from_database(database, action["action_id"])

    # TODO: Really? More simple. JSONConverterMixIn. isinstance(...)
    def convert_to_json(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.convert_to_json(),
            "users": [u.convert_to_json() for u in self.users],
            "description": self.description,
            "chat": self.chat.convert_to_json(),
            "creation_time": self.creation_time,
            "action_time": self.action_time,
        }

    def add_user(
        self, database: interfaces.Database, user: interfaces.User
    ) -> None:
        if not database.action_get_by_action_and_user_id(
            self.action_id, user.user_id
        ):
            self.users.append(user)
            database.action_add_user(self.action_id, user.user_id)
            self.chat.users.append(user)
            database.user_add_to_chat(user.user_id, self.chat.chat_id)

    def delete_user(
        self, database: interfaces.Database, user: interfaces.User
    ) -> None:
        if user in self.users:
            database.user_leave_action(user.user_id, self.action_id)
            self.users.pop(self.users.index(user))
            self.chat.delete_user(database, user)
