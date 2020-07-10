import requests


if __name__ == "__main__":
    addr = "http://127.0.0.1:8000"
    # addr = "http://81.91.176.31:9989"
    print("Create user")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.create",
            "params": {
                "first_name": "APITest",
                "second_name": "Карпов",
                "birthday": 1278831449,
                "email": "lion@migra.net",
                "phone": "89111653243",
                "password": "кул",
            },
        },
    )
    print(response)
    print(response.content)
    user_id = response.json()["result"]["user_id"]
    print("Try to login (incorrect password)")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.login",
            "params": {"user_id": user_id, "password": "фикус"},
        },
    )
    print(response)
    print(response.content)
    print("Try to login (Correct password)")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.login",
            "params": {"user_id": user_id, "password": "кул"},
        },
    )
    print(response)
    print(response.content)
    user_session = response.json()["result"]["user_session"]
    print("Get short info")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.get_short_data",
            "params": {"user_session": user_session},
        },
    )
    print(response)
    print(response.content)
    # user_id = 4
    print("Delete user (Incorrect session)")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.delete",
            "params": {"user_id": user_id, "user_session": user_session},
        },
    )
    print(response)
    print(response.content)

    # chat
    print("Create single chat")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "chat.create",
            "params": {
                "user_session": user_session,
                "user_id": 1,
                "chat_name": "1",
            },
        },
    )
    print(response)
    print(response.content)

    print("Re-create this single chat")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.create",
            "params": {
                "user_session": user_session,
                "user_id": 1,
                "chat_name": "2",
            },
        },
    )
    print(response)
    print(response.content)
    chat_id = response.json()["result"]["chat_id"]
    print("Create other single chat")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.create",
            "params": {
                "user_session": user_session,
                "user_id": 2,
                "chat_name": "3",
            },
        },
    )
    print(response)
    print(response.content)
    print("Send message to chat %d" % chat_id)
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.send_message",
            "params": {
                "user_session": user_session,
                "chat_id": chat_id,
                "message": "Hello, world!",
            },
        },
    )
    print("Send message to chat %d" % chat_id)
    print(response)
    print(response.content)
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.send_message",
            "params": {
                "user_session": user_session,
                "chat_id": chat_id,
                "message": "Hello, world1!",
            },
        },
    )
    print(response)
    print(response.content)
    print("Get single chat with chat_id  %d" % chat_id)
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.get_by_id",
            "params": {"user_session": user_session, "chat_id": chat_id,},
        },
    )
    print(response)
    print(response.content)
    print("Get single chat with 1 messages")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.get_by_id",
            "params": {
                "user_session": user_session,
                "chat_id": chat_id,
                "message_limit": 1,
            },
        },
    )
    print(response)
    print(response.content)
    print("Get single chat with 0 messages")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.get_by_id",
            "params": {
                "user_session": user_session,
                "chat_id": chat_id,
                "message_limit": 0,
            },
        },
    )
    print(response)
    print(response.content)
    print("Get single chat with 0 messages by time_to")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.get_by_id",
            "params": {
                "user_session": user_session,
                "chat_id": chat_id,
                "time_to": 1,
            },
        },
    )
    print(response)
    print(response.content)
    print("Get single chat with 2 messages by time_from")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.get_by_id",
            "params": {
                "user_session": user_session,
                "chat_id": chat_id,
                "time_from": 1,
            },
        },
    )
    print(response)
    print(response.content)
    print("Get single chat with 0 messages by time_from and time_to")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.get_by_id",
            "params": {
                "user_session": user_session,
                "chat_id": chat_id,
                "time_from": 1,
                "time_to": 2,
            },
        },
    )
    print(response)
    print(response.content)

    print("Create multi-chat")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "multi_chat.create",
            "params": {
                "user_session": user_session,
                "user_ids": [1, 2, 3],
                "chat_name": "212",
            },
        },
    )
    print(response)
    print(response.content)

    print("Create multi-chat N2")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "multi_chat.create",
            "params": {
                "user_session": user_session,
                "user_ids": [1, 2, 3],
                "chat_name": "212",
            },
        },
    )
    print(response)
    print(response.content)

    print("Get all chats")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.get_chat_list",
            "params": {"user_session": user_session},
        },
    )
    print(response)
    print(response.content)
    # Delete chat
    print("Delete single chat with chat id %d" % chat_id)
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.delete",
            "params": {"user_session": user_session, "chat_id": chat_id},
        },
    )
    print(response)
    print(response.content)
    # Friends
    print("Admin friends")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "friends.get_friend_list",
            "params": {"user_session": user_session, "user_id": 1},
        },
    )
    print(response)
    print(response.content)
    print("Login by admin")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.login_by_email",
            "params": {"email": "test01@migra.net", "password": "админ"},
        },
    )
    print(response)
    print(response.content)
    admin_session = response.json()["result"]["user_session"]
    print("Send request to 1")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.send_request_to_add",
            "params": {"user_session": user_session, "user_id": 1},
        },
    )
    print(response)
    print(response.content)
    print("Try to decline by not 1")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.decline_request",
            "params": {"user_session": user_session, "user_id": 1},
        },
    )
    print(response)
    print(response.content)

    print("Decline by admin")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.decline_request",
            "params": {"user_session": admin_session, "user_id": user_id},
        },
    )
    print(response)
    print(response.content)
    print("Send request to 1")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.send_request_to_add",
            "params": {"user_session": user_session, "user_id": 1},
        },
    )
    print(response)
    print(response.content)
    print("Get friends list")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.get_friend_list",
            "params": {"user_session": user_session},
        },
    )
    print(response)
    print(response.content)
    print("Accept")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.accept_request",
            "params": {"user_session": admin_session, "user_id": user_id},
        },
    )
    print(response)
    print(response.content)
    print("Get friends list")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.get_friend_list",
            "params": {"user_session": user_session},
        },
    )
    print(response)
    print(response.content)
    print("Delete from friends")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.delete",
            "params": {"user_session": user_session, "user_id": 1},
        },
    )
    print(response)
    print(response.content)

    print("Get friends list")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.get_friend_list",
            "params": {"user_session": user_session},
        },
    )
    print(response)
    print(response.content)

    print("Send request to 1")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.send_request_to_add",
            "params": {"user_session": user_session, "user_id": 1},
        },
    )
    print(response)
    print(response.content)

    print("Accept")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.accept_request",
            "params": {"user_session": admin_session, "user_id": user_id},
        },
    )
    print(response)
    print(response.content)

    print("Friends find (Kirill)")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.find",
            "params": {"user_session": admin_session, "first_name": "Kirill"},
        },
    )
    print(response)
    print(response.content)

    print("Friends find with time (all)")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.find",
            "params": {
                "user_session": admin_session,
                "birthday": [{"method": "le", "value": 1594277653}],
            },
        },
    )
    print(response)
    print(response.content)

    print("Friends find (All)")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.find",
            "params": {
                "user_session": admin_session,
                "birthday": [
                    {"method": "le", "value": 1594277653},
                    {"method": "ge", "value": 1},
                ],
            },
        },
    )
    print(response)
    print(response.content)

    print("Friends find (Null)")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.find",
            "params": {
                "user_session": admin_session,
                "birthday": [
                    {"method": "le", "value": 1594277653},
                    {"method": "ge", "value": 1594277652},
                ],
            },
        },
    )
    print(response)
    print(response.content)

    print("Block other user")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.block_user",
            "params": {"user_session": admin_session, "user_id": user_id},
        },
    )
    print(response)
    print(response.content)

    print("Create other single chat")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "chat.create",
            "params": {
                "user_session": user_session,
                "user_id": 1,
                "chat_name": "1",
            },
        },
    )
    print(response)
    print(response.content)

    print("Get friends list")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "friends.get_friend_list",
            "params": {"user_session": user_session},
        },
    )
    print(response)
    print(response.content)

    print("Create action")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "action.create",
            "params": {
                "user_session": user_session,
                "name": "Urraa",
                "latitude": 1,
                "longitude": 2,
                "user_ids": [1, 2, 3],
                "description": "Hello",
                "action_time": 12,
            },
        },
    )
    print(response)
    print(response.content)
    action_id = response.json()["result"]["action_id"]

    print("Get action")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "action.get",
            "params": {"user_session": user_session, "action_id": action_id,},
        },
    )
    print(response)
    print(response.content)

    print("Admin login")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.login",
            "params": {"user_id": 1, "password": "админ"},
        },
    )
    print(response)
    print(response.content)
    print("Login by email")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.login_by_email",
            "params": {"email": "test01@migra.net", "password": "админ"},
        },
    )
    print(response)
    print(response.content)
    print("Delete user by admin")
    admin_session = response.json()["result"]["user_session"]
    print("Get admin actions")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.get_actions",
            "params": {"user_session": admin_session},
        },
    )
    print(response)
    print(response.content)

    print("Create action")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 778,
            "method": "action.create",
            "params": {
                "user_session": admin_session,
                "name": "Ur",
                "latitude": 1,
                "longitude": 2,
                "user_ids": [2],
                "description": "Hello",
                "action_time": 12,
            },
        },
    )
    print(response)
    print(response.content)
    admin_action_id = response.json()["result"]["action_id"]

    print("Add user to action")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.add_to_action",
            "params": {
                "action_id": admin_action_id,
                "user_session": user_session,
            },
        },
    )
    print(response)
    print(response.content)

    print("Get user actions")
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.get_actions",
            "params": {"user_session": user_session},
        },
    )
    print(response)
    print(response.content)

    # admin_session =
    response = requests.post(
        addr,
        json={
            "jsonrpc": "2.0",
            "id": 777,
            "method": "user.delete",
            "params": {"user_id": user_id, "user_session": admin_session},
        },
    )
    print(response)
    print(response.content)
