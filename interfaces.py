from typing import Optional, Dict, Any, List
from typing_extensions import Protocol, runtime_checkable

from constants import Roles, Status


@runtime_checkable
class User(Protocol):
    user_id: int
    first_name: str
    second_name: str
    birthday: int
    password: str
    phone: str
    email: str
    role: Roles
    points: int
    status: Status
    patronymic: Optional[str]

    @classmethod
    def create_from_database(
        cls,
        db: "Database",
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> "User":
        ...

    @classmethod
    def create_in_database(
        cls,
        database: "Database",
        first_name: str,
        second_name: str,
        birthday: int,
        password: str,
        phone: str,
        email: str,
        role: Roles,
        points: int,
        status: Status,
        patronymic: Optional[str] = None,
    ) -> "User":
        ...

    def convert_to_json(self) -> Dict[str, Any]:
        ...

    def __hash__(self):
        return self.user_id

    def __eq__(self, other):
        return isinstance(other, User) and other.user_id == self.user_id


class Chat(Protocol):
    chat_id: int
    chat_name: str
    owner: User
    users: List[User]
    messages: Optional[List["Message"]] = None

    @classmethod
    def create_from_database(
        cls,
        database: "Database",
        chat_id: int,
        message_limit: Optional[int] = None,
        time_from: Optional[int] = None,
        time_to: Optional[int] = None,
    ) -> "Chat":
        ...

    @classmethod
    def create_in_database(
        cls, database: "Database", owner: User, chat_name: str, *users: User
    ):
        ...

    def convert_to_json(self) -> Dict[str, Any]:
        ...

    def delete_user(self, database: "Database", user: User) -> None:
        ...


class Message(Protocol):
    chat_id: int
    from_user_id: int
    message: str
    read: bool
    time: int

    def convert_to_json(self) -> Dict[str, Any]:
        ...


class Action(Protocol):
    action_id: int
    name: str
    latitude: int
    longitude: int
    owner: User
    users: List[User]
    description: str
    chat: Chat
    creation_time: int
    action_time: int

    @classmethod
    def create_from_database(
        cls, database: "Database", action_id: int
    ) -> "Action":
        ...

    @classmethod
    def create_in_database(
        cls,
        database: "Database",
        name: str,
        latitude: float,
        longitude: float,
        owner: User,
        users: List[User],
        description: str,
        action_time: int,
    ) -> "Action":
        ...

    def convert_to_json(self) -> Dict[str, Any]:
        ...

    def add_user(self, database: "Database", user: User) -> None:
        ...

    def delete_user(self, database: "Database", user: User) -> None:
        ...


class Database(Protocol):
    def user_get_id_by_phone(self, phone: str) -> List[Dict[str, Any]]:
        ...

    def user_get_id_by_email(self, email: str) -> List[Dict[str, Any]]:
        ...

    def user_get_by_id(self, user_id: int) -> List[Dict[str, Any]]:
        ...

    def user_get_by_email(self, email: str) -> List[Dict[str, Any]]:
        ...

    def user_get_by_phone(self, phone: str) -> List[Dict[str, Any]]:
        ...

    def user_create(
        self,
        first_name: str,
        second_name: str,
        birthday: int,
        password: str,
        phone: str,
        email: str,
        role: Roles,
        points: int,
        status: Status,
        patronymic: Optional[str],
    ) -> Any:
        ...

    def user_set_online(self, user_id: int, session: int) -> None:
        ...

    def user_delete(self, user_id: int) -> None:
        ...

    def user_get_id_online_by_session(
        self, user_session: int
    ) -> List[Dict[str, Any]]:
        ...

    def user_get_session_by_id(self, user_id: int) -> List[Dict[str, Any]]:
        ...

    def user_get_blocked(self, user_id: int) -> List[Dict[str, Any]]:
        ...

    def user_get_blocked_at(self, user_id: int) -> List[Dict[str, Any]]:
        ...

    def single_chat_ids_get_by_user_id(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        ...

    def chat_create(
        self, owner: int, chat_name: str, *user_ids: int
    ) -> List[Dict[str, Any]]:
        ...

    def single_chat_get_by_chat_id(self, chat_id: int) -> List[Dict[str, Any]]:
        ...

    def single_chats_get_by_users_id(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        ...

    def single_chat_delete_by_user_id_and_chat_id(
        self, chat_id: int, user_id: int
    ) -> None:
        ...

    def single_chat_meta_info_get_by_chat_id(
        self, chat_id: int
    ) -> List[Dict[str, Any]]:
        ...

    def singe_chat_send_message(
        self, chat_id: int, from_user_id: int, message: str
    ) -> None:
        ...

    def single_chat_get_messages(
        self,
        chat_id: int,
        message_limit: Optional[int] = None,
        time_from: Optional[int] = None,
        time_to: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        ...

    def friends_get_all_ids_by_user_id(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        ...

    def friends_get_to_add_waiter_ids(
        self, user_id: int
    ) -> List[Dict[str, Any]]:
        ...

    def friends_add_to_waiter(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        ...

    def friends_add_to_friend(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        ...

    def friends_delete_from_waiter(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        ...

    def friends_delete(self, source_user_id: int, target_user_id: int) -> None:
        ...

    def friends_block_user(
        self, source_user_id: int, target_user_id: int
    ) -> None:
        ...

    def friends_find(
        self, simple_keys: Dict[str, Any], difficult_keys: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        ...

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
        ...

    def action_get_users(self, action_id: int) -> List[Dict[str, Any]]:
        ...

    def action_get(self, action_id: int) -> List[Dict[str, Any]]:
        ...

    def action_find(
        self, latitude: float, longitude: float, r: float
    ) -> List[Dict[str, Any]]:
        ...

    def user_get_actions(self, user_id: int) -> List[Dict[str, Any]]:
        ...

    def action_get_by_action_and_user_id(
        self, action_id: int, user_id: int
    ) -> List[Dict[str, Any]]:
        ...

    def action_add_user(self, action_id: int, user_id: int) -> None:
        ...

    def user_add_to_chat(self, user_id: int, chat_id: int) -> None:
        ...

    def user_leave_action(self, user_id: int, action_id: int) -> None:
        ...

    def user_leave_chat(self, user_id: int, chat_id: int) -> None:
        ...
