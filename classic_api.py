import hashlib
from typing import *
from random import randint

import models
import jsonrpc
import database
import constants
import interfaces


_database: interfaces.Database = database.NullDatabase()


def init(database: interfaces.Database) -> None:
    global _database
    _database = database


def get_hash(s: str) -> str:
    return (
        hashlib.md5(s.encode(errors="replace"))
        .digest()
        .decode(errors="replace")
    )


def _user_exists(user_data: List[Dict[str, Any]]) -> None:
    if not user_data:
        raise jsonrpc.JSONRPCError({"code": -1000, "message": "Unknown user."})


def _get_user_by_user_id(user_id: int) -> interfaces.User:
    _user_exists(_database.user_get_by_id(user_id))
    return models.User.create_from_database(_database, user_id=user_id)


def _get_user_by_email(email: str) -> interfaces.User:
    _user_exists(_database.user_get_id_by_email(email))
    return models.User.create_from_database(_database, email=email)


def _get_random_session() -> int:
    while True:
        r = randint(1, 90000000)
        if not _database.user_get_id_online_by_session(r):
            break
    return r


def _get_user_id_by_session(session: int) -> int:
    user_id = _database.user_get_id_online_by_session(session)
    if not user_id:
        raise jsonrpc.JSONRPCError(
            {"code": -1004, "message": "Incorrect session"}
        )
    return user_id[0]["user_id"]


def _get_user_by_session(session: int) -> interfaces.User:
    return _get_user_by_user_id(_get_user_id_by_session(session))


def _authentication(
    user: interfaces.User, expected_role: constants.Roles
) -> None:
    if user.role < expected_role:
        raise jsonrpc.JSONRPCError(
            {"code": -1005, "message": "Incorrect role"}
        )


def _check_user_in_chat(user: interfaces.User, chat: interfaces.Chat) -> None:
    for u in chat.users:
        if u.user_id == user.user_id:
            break
    else:
        raise jsonrpc.JSONRPCError(
            {"code": -1008, "message": "Incorrect chat_id"}
        )


def _get_chat_id_by_user_ids(user_id1, user_id2) -> List[int]:
    raw_result = []
    raw_result.extend(_database.single_chats_get_by_users_id(user_id1))
    if not raw_result:
        return []
    for chat_data in raw_result:
        single_chat = _database.single_chat_get_by_chat_id(
            chat_data["chat_id"]
        )
        if len(single_chat) == 2:
            if (
                single_chat[0]["user_id"] == user_id2
                or single_chat[1]["user_id"] == user_id2
            ):
                return [chat_data["chat_id"]]
    return []


def _chat_exists(chat_id: int) -> None:
    current_chat_id = _database.single_chat_meta_info_get_by_chat_id(chat_id)
    if not current_chat_id:
        raise jsonrpc.JSONRPCError(
            {"code": -1007, "message": "Chat does not exists"}
        )


def _get_chat(
    chat_id: int,
    message_limit: Optional[int] = None,
    time_from: Optional[int] = None,
    time_to: Optional[int] = None,
) -> interfaces.Chat:
    _chat_exists(chat_id)
    return models.Chat.create_from_database(
        _database, chat_id, message_limit, time_from, time_to
    )


def _check_password(user: interfaces.User, password: str) -> None:
    if user.password != get_hash(password):
        raise jsonrpc.JSONRPCError(
            {"code": -1001, "message": "Incorrect password"}
        )


def _get_user_session(user_id: int) -> int:
    current_session = _database.user_get_session_by_id(user_id)
    if not current_session:
        session = _get_random_session()
        _database.user_set_online(user_id, session)
    else:
        session = current_session[0]["user_session"]
    return session


def _user_login(user: interfaces.User, password: str) -> int:
    _check_password(user, password)
    return _get_user_session(user.user_id)


def _get_blocked_user_ids(user: interfaces.User) -> List[int]:
    return [
        b["target_user_id"] for b in _database.user_get_blocked(user.user_id)
    ]


def _get_blocked_user_ids_at(user: interfaces.User) -> List[int]:
    return [
        b["source_user_id"]
        for b in _database.user_get_blocked_at(user.user_id)
    ]


def _check_blocks(user: interfaces.User, block_list: List[int]) -> None:
    if user.user_id in block_list:
        raise jsonrpc.JSONRPCError(
            {
                "code": -1006,
                "message": "User '%d' was blocked by someone" % user.user_id,
            }
        )


def _user_blocked(user: interfaces.User, blocker: interfaces.User) -> None:
    blocked_by_user = _get_blocked_user_ids(blocker)
    _check_blocks(user, blocked_by_user)


def _blocked_by_user(blocker: interfaces.User, user: interfaces.User) -> None:
    blocked_by_user = _get_blocked_user_ids(blocker)
    if user.user_id in blocked_by_user:
        raise jsonrpc.JSONRPCError(
            {
                "code": -1009,
                "message": "User '%d' was blocked by user '%d'. Need to unblock"
                % (user.user_id, blocker.user_id),
            }
        )


def _get_friend_waiter_to_add_ids(user: interfaces.User) -> List[int]:
    return [
        u["source_user_id"]
        for u in _database.friends_get_to_add_waiter_ids(user.user_id)
    ]


def _user_in_friend_waiters(
    source_user: interfaces.User, target_user: interfaces.User
) -> None:
    if source_user.user_id not in _get_friend_waiter_to_add_ids(target_user):
        raise jsonrpc.JSONRPCError(
            {
                "code": -1010,
                "message": "User '%d' not in your friend-waiters"
                % source_user.user_id,
            }
        )


def _get_friend_ids(user: interfaces.User) -> List[int]:
    return [
        u_i["target_user_id"]
        for u_i in _database.friends_get_all_ids_by_user_id(user.user_id)
    ]


def _user_in_friends(
    source_user: interfaces.User, target_user: interfaces.User
) -> None:
    if source_user.user_id not in _get_friend_ids(target_user):
        raise jsonrpc.JSONRPCError(
            {
                "code": -1011,
                "message": "User '%d' not in your friends"
                % source_user.user_id,
            }
        )


def _action_exists(action_id: int) -> None:
    result = _database.action_get(action_id)
    if not result:
        raise jsonrpc.JSONRPCError(
            {
                "code": -1012,
                "message": "Action id '%d' is unknown" % action_id,
            }
        )


def _get_action_by_id(action_id: int) -> interfaces.Action:
    _action_exists(action_id)
    return models.Action.create_from_database(_database, action_id)


@jsonrpc.Dispatcher.register(
    "user.create",
    [["first_name", "second_name", "birthday", "password", "phone", "email"]],
)
def user_create(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    params["password"] = get_hash(str(params["password"]))
    null_user = _database.user_get_id_by_email(params["email"])
    if null_user:
        raise jsonrpc.JSONRPCError(
            {
                "code": -1002,
                "message": "Email '%s' already used" % params["email"],
            }
        )
    null_user = _database.user_get_id_by_email(params["phone"])
    if null_user:
        raise jsonrpc.JSONRPCError(
            {
                "code": -1003,
                "message": "Phone number '%s' already used" % params["phone"],
            }
        )
    user = models.User.create_in_database(  # type: ignore
        _database,  # type: ignore
        **params,  # type: ignore
        role=constants.Roles.User,  # type: ignore
        status=constants.Status.Active,  # type: ignore
        points=0,  # type: ignore
    )  # type: ignore
    return jsonrpc.create_json_response(json, {"user_id": user.user_id})


@jsonrpc.Dispatcher.register("user.login", [["user_id", "password"]])
def user_login(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    user = _get_user_by_user_id(int(params["user_id"]))
    return jsonrpc.create_json_response(
        json,
        {
            "user_session": _user_login(user, params["password"]),
            "user_id": user.user_id,
        },
    )


@jsonrpc.Dispatcher.register("user.login_by_email", [["email", "password"]])
def user_login_by_email(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    user = _get_user_by_email(params["email"])
    return jsonrpc.create_json_response(
        json, {"user_session": _user_login(user, params["password"])}
    )


@jsonrpc.Dispatcher.register("user.get_short_data", [["user_session"]])
def user_get_short_data_by_id(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    user = _get_user_by_session(int(params["user_session"]))
    return jsonrpc.create_json_response(json, user.convert_to_json())


@jsonrpc.Dispatcher.register("user.delete", [["user_id", "user_session"]])
def delete_user(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    user = _get_user_by_session(int(params["user_session"]))
    _authentication(user, constants.Roles.Admin)
    _database.user_delete(int(params["user_id"]))
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register(
    "chat.create", [["user_session", "user_id", "chat_name"]]
)
def single_chat_create(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    from_user = _get_user_by_session(int(params["user_session"]))
    to_user = _get_user_by_user_id(int(params["user_id"]))
    _user_blocked(from_user, to_user)
    current_chat_id = _get_chat_id_by_user_ids(
        from_user.user_id, to_user.user_id
    )
    if current_chat_id:
        return jsonrpc.create_json_response(
            json, {"chat_id": current_chat_id[0]}
        )
    chat_id = _database.chat_create(
        from_user.user_id, params["chat_name"], to_user.user_id
    )[0]["chat_id"]
    return jsonrpc.create_json_response(json, {"chat_id": chat_id})


@jsonrpc.Dispatcher.register(
    "multi_chat.create", [["user_session", "user_ids", "chat_name"]]
)
def multi_chat_create(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    from_user = _get_user_by_session(int(params["user_session"]))
    for u_i in params["user_ids"]:
        _get_user_by_user_id(u_i)
    block_list = _get_blocked_user_ids_at(from_user)
    _check_blocks(from_user, block_list)
    chat_id = _database.chat_create(
        from_user.user_id, params["chat_name"], *params["user_ids"]
    )[0]["chat_id"]
    return jsonrpc.create_json_response(json, {"chat_id": chat_id})


# TODO: Delete from models
@jsonrpc.Dispatcher.register("chat.delete", [["user_session", "chat_id"]])
def single_chat_delete(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    chat_id = int(params["chat_id"])
    chat = _get_chat(chat_id)
    user = _get_user_by_session(int(params["user_session"]))
    _check_user_in_chat(user, chat)
    _database.single_chat_delete_by_user_id_and_chat_id(chat_id, user.user_id)
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register(
    "chat.send_message", [["user_session", "chat_id", "message"]]
)
def single_chat_send_message(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    from_user = _get_user_by_session(params["user_session"])
    chat = _get_chat(int(params["chat_id"]))
    _check_user_in_chat(from_user, chat)
    _database.singe_chat_send_message(
        chat.chat_id, from_user.user_id, params["message"]
    )
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register("chat.get_by_id", [["user_session", "chat_id"]])
def single_chat_get_by_chat_id(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    user = _get_user_by_session(int(params["user_session"]))
    chat = _get_chat(
        int(params["chat_id"]),
        params.get("message_limit"),
        params.get("time_from"),
        params.get("time_to"),
    )
    _check_user_in_chat(user, chat)
    return jsonrpc.create_json_response(json, chat.convert_to_json())


@jsonrpc.Dispatcher.register("chat.get_chat_list", [["user_session"]])
def single_chats_get_by_user_id(json: Dict[str, Any]) -> Dict[str, Any]:
    session = int(json["params"]["user_session"])
    user = _get_user_by_session(session)
    chats = []
    for c_i in _database.single_chat_ids_get_by_user_id(user.user_id):
        c = _database.single_chat_meta_info_get_by_chat_id(c_i["chat_id"])[0]
        chats.append(
            {
                "chat_id": c["chat_id"],
                "owner": c["owner"],
                "chat_name": c["chat_name"],
            }
        )
    return jsonrpc.create_json_response(json, chats)


@jsonrpc.Dispatcher.register("friends.get_friend_list", [["user_session"]])
def friends_get_friends_list(json: Dict[str, Any]) -> Dict[str, Any]:
    session = int(json["params"]["user_session"])
    user = _get_user_by_session(session)
    target_user_id = json["params"].get("user_id")
    if target_user_id is not None:
        target_user = _get_user_by_user_id(target_user_id)
        _blocked_by_user(target_user, user)
        user = target_user
    return jsonrpc.create_json_response(
        json,
        [
            models.User.create_from_database(
                _database, user_id=d["target_user_id"]
            ).convert_to_json()
            for d in _database.friends_get_all_ids_by_user_id(user.user_id)
        ],
    )


@jsonrpc.Dispatcher.register(
    "friends.send_request_to_add", [["user_session", "user_id"]]
)
def friends_send_request_to_add(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    source_user = _get_user_by_session(int(params["user_session"]))
    target_user = _get_user_by_user_id(int(params["user_id"]))
    if source_user.user_id in _get_friend_waiter_to_add_ids(target_user):
        return jsonrpc.create_json_response(json, None)
    _user_blocked(source_user, target_user)
    _blocked_by_user(source_user, target_user)
    if target_user.user_id in _get_friend_waiter_to_add_ids(source_user):
        _database.friends_add_to_friend(
            source_user.user_id, target_user.user_id
        )
    else:
        _database.friends_add_to_waiter(
            source_user.user_id, target_user.user_id
        )
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register(
    "friends.accept_request", [["user_session", "user_id"]]
)
def friends_accept_request_to_add(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    source_user = _get_user_by_session(int(params["user_session"]))
    target_user = _get_user_by_user_id(int(params["user_id"]))
    _user_in_friend_waiters(target_user, source_user)
    _database.friends_add_to_friend(source_user.user_id, target_user.user_id)
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register(
    "friends.decline_request", [["user_session", "user_id"]]
)
def friends_decline_request_to_add(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    source_user = _get_user_by_session(int(params["user_session"]))
    target_user = _get_user_by_user_id(int(params["user_id"]))
    _user_in_friend_waiters(target_user, source_user)
    _database.friends_delete_from_waiter(
        target_user.user_id, source_user.user_id
    )
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register("friends.delete", [["user_session", "user_id"]])
def friends_delete(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    source_user = _get_user_by_session(int(params["user_session"]))
    target_user = _get_user_by_user_id(int(params["user_id"]))
    _user_in_friends(target_user, source_user)
    _database.friends_delete(source_user.user_id, target_user.user_id)
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register(
    "friends.block_user", [["user_session", "user_id"]]
)
def friends_block_user(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    source_user = _get_user_by_session(int(params["user_session"]))
    target_user = _get_user_by_user_id(int(params["user_id"]))
    friends_list = _get_friend_ids(source_user)
    if target_user.user_id in friends_list:
        _database.friends_delete(source_user.user_id, target_user.user_id)
    waiters_list = _get_friend_waiter_to_add_ids(source_user)
    if target_user.user_id in waiters_list:
        _database.friends_delete_from_waiter(
            target_user.user_id, source_user.user_id
        )
    blocked = _get_blocked_user_ids(source_user)
    if target_user.user_id in blocked:
        return jsonrpc.create_json_response(json, None)
    _database.friends_block_user(source_user.user_id, target_user.user_id)
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register("friends.get_friend_requests", [["user_session"]])
def friends_get_friend_requests(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    user = _get_user_by_session(int(params["user_session"]))
    return jsonrpc.create_json_response(
        json,
        {
            "frined_requests": [
                models.User.create_from_database(
                    _database, u_i
                ).convert_to_json()
                for u_i in _get_friend_waiter_to_add_ids(user)
            ]
        },
    )


@jsonrpc.Dispatcher.register("friends.find", [["user_session"]])
def friends_find(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    simple_keys = {}
    for k, v in params.items():
        if k not in constants.ALLOWED_SEARCH_KEYS:
            continue
        simple_keys[k] = v
    difficult_keys = []
    for k, v in params.items():
        if k not in constants.ALLOWED_DIFFICULT_SEARCH_KEYS:
            continue
        for method in v:
            condition = constants.COMPARISON_SIGNS[method["method"]]
            data = method["value"]
            difficult_keys.append(
                {"key": k, "condition": condition, "data": data}
            )
    return jsonrpc.create_json_response(
        json,
        [
            models.User.create_from_database(
                _database, user_id=u_i["user_id"]
            ).convert_to_json()
            for u_i in _database.friends_find(simple_keys, difficult_keys)
        ],
    )


@jsonrpc.Dispatcher.register(
    "action.create",
    [
        [
            "user_session",
            "name",
            "description",
            "latitude",
            "longitude",
            "action_time",
        ]
    ],
)
def action_create(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    owner = _get_user_by_session(params["user_session"])
    data = {
        "name": params["name"],
        "latitude": params["latitude"],
        "longitude": params["longitude"],
        "owner": owner,
        "description": params["description"],
        "action_time": params["action_time"],
    }
    if owner.role >= constants.Roles.Admin:
        data["users"] = [
            _get_user_by_user_id(u_i) for u_i in params["user_ids"]
        ]
    else:
        data["users"] = []
    action = models.Action.create_in_database(_database, **data)
    return jsonrpc.create_json_response(json, action.convert_to_json())


@jsonrpc.Dispatcher.register("action.get", [["user_session", "action_id"]])
def action_get(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    _get_user_by_session(params["user_session"])
    _action_exists(params["action_id"])
    return jsonrpc.create_json_response(
        json, _get_action_by_id(params["action_id"]).convert_to_json()
    )


@jsonrpc.Dispatcher.register("user.get_actions", [["user_session"]])
def user_get_actions(json: Dict[str, Any]) -> Dict[str, Any]:
    user = _get_user_by_session(int(json["params"]["user_session"]))
    action_ids = _database.user_get_actions(user.user_id)
    return jsonrpc.create_json_response(
        json,
        [
            models.Action.create_from_database(
                _database, a_i["action_id"]
            ).convert_to_json()
            for a_i in action_ids
        ],
    )


@jsonrpc.Dispatcher.register(
    "user.add_to_action", [["user_session", "action_id"]]
)
def user_add_to_action(json: Dict[str, Any]) -> Dict[str, Any]:
    user = _get_user_by_session(int(json["params"]["user_session"]))
    action = _get_action_by_id(json["params"]["action_id"])
    action.add_user(_database, user)
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register(
    "user.leave_action", [["user_session", "action_id"]]
)
def user_leave_action(json: Dict[str, Any]) -> Dict[str, Any]:
    user = _get_user_by_session(int(json["params"]["user_session"]))
    action = _get_action_by_id(json["params"]["action_id"])
    action.delete_user(_database, user)
    return jsonrpc.create_json_response(json, None)


@jsonrpc.Dispatcher.register("user.leave_chat", [["user_session", "chat_id"]])
def user_leave_chat(json: Dict[str, Any]) -> Dict[str, Any]:
    user = _get_user_by_session(int(json["params"]["user_session"]))
    chat = _get_chat(chat_id=json["params"]["chat_id"], message_limit=0)
    chat.delete_user(_database, user)
    return jsonrpc.create_json_response(json, None)


# User session?
@jsonrpc.Dispatcher.register(
    "action.find", [["user_session", "latitude", "longitude", "r"]]
)
def action_find(json: Dict[str, Any]) -> Dict[str, Any]:
    params = json["params"]
    user = _get_user_by_session(int(params["user_session"]))
    result = [
        models.Action.create_from_database(
            _database, a_i["action_id"]
        ).convert_to_json()
        for a_i in _database.action_find(
            latitude=params["latitude"],
            longitude=params["longitude"],
            r=params["r"],
        )
    ]
    return jsonrpc.create_json_response(json, result)
