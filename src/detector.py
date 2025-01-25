import pyrogram as tg
import json as jn
import time
import os
import src.type_utils as tu

async def detect_user_messages(
        host_client: tg.client.Client,
        chat_id: int,
        user_id: int,
        limit_msgs: int = 5,
        up_limit: int = 50
):
    trust = 0
    msgs = []
    while True:
        try:
            msg_count = await host_client.search_messages_count(
                chat_id=chat_id,  # ID чата
                from_user=user_id  # ID пользователя
            )
            break
        except tg.errors.exceptions.flood_420.FloodWait as wait_err:
                wait_time = wait_err.value
                print(f"Необходимо подождать {wait_time} секунд.")
                time.sleep(wait_time)

    if msg_count in [0, 1]:  
        pass
    elif msg_count <= limit_msgs:
        coroutine = host_client.search_messages(
            chat_id=chat_id,  # ID чата
            from_user=user_id,  # ID пользователя
            limit=2
        )

        while True:
            try:
                async for msg in coroutine:
                    msg: tg.types.Message = msg
                    
                    if msg.text is None:
                        msgs.append({
                            "text": msg.text,
                            "id": msg.id,
                            "date": msg.date,
                            "redacted_time": msg.edit_date
                        })
                    else:
                        msgs.append({
                            "text": None,
                            "id": msg.id,
                            "date": msg.date,
                            "redacted_time": msg.edit_date
                        })
                break
            except tg.errors.exceptions.flood_420.FloodWait as wait_err:
                wait_time = wait_err.value
                print(f"Необходимо подождать {wait_time} секунд.")
                time.sleep(wait_time)  # Ждем указанное время

        trust = 0.1

    elif msg_count <= up_limit:
        
        coroutine = host_client.search_messages(
            chat_id=chat_id,  # ID чата
            from_user=user_id,  # ID пользователя
        )

        while True:
            try:
                async for msg in coroutine:
                    msg: tg.types.Message = msg
                    if msg.text is None:
                        msgs.append({
                            "text": None,
                            "redacted_time": msg.edit_date
                        })
                    else:
                        msgs.append({
                            "text": msg.text[:100],
                            "redacted_time": msg.edit_date
                        })
                break
            except tg.errors.exceptions.flood_420.FloodWait as wait_err:
                wait_time = wait_err.value
                print(f"Необходимо подождать {wait_time} секунд.")
                time.sleep(wait_time)
        
        trust = 0.5

    elif msg_count >= up_limit:
        trust = 1

    return {
        "count": msg_count, 
        "messages": msgs, 
        "trust_level": trust
    }

async def get_channel_id(
        client: tg.client.Client,
        username: str
):
    try:
        # Получение информации о чате
        chat = await client.get_chat(username)
        # Извлечение ID канала
        channel_id = chat.id
        return channel_id
    except Exception as e:
        print(f"Error while extracting channel: {e}")

async def full_user_info(
        user: tg.types.User,
        chat: tg.types.Chat,
        member: tg.types.ChatMember,
        host_client: tg.client.Client
):
    while True:
        try:
            full_user: tg.raw.types.user_full.UserFull = (await host_client.invoke(tg.raw.functions.users.GetFullUser(
                id=await host_client.resolve_peer(user.id)
            ))).full_user

            break  # Выход из цикла, если запрос успешен

        except tg.errors.exceptions.flood_420.FloodWait as wait_err:
            wait_time = wait_err.value
            print(f"Необходимо подождать {wait_time} секунд.")
            time.sleep(wait_time)  # Ждем указанное время

    ruser = await host_client.get_users(user.username)

    return {
        "fullname": " ".join([str(tu.null_wrapper(user.first_name)), str(tu.null_wrapper(user.last_name))]).strip(),
        "username": user.username,
        "phone": user.phone_number,
        "photo": tu.null_wrapper(user.photo).__dict__,
        "bio": full_user.about,
        "real_photo": ruser.photo,
        "is_premium": user.is_premium,
        "join_date": str(member.joined_date),
        "tg_uid": user.id,
        "is_bot": user.is_bot,
        "msg_analysis": await detect_user_messages(host_client, chat.id, user.id),
        "last_seen_online": user.last_online_date.date
        # "chat_id": await get_channel_id(host_client, user.username),
    }

async def plain_user_info(
        user: tg.types.User,
        chat: tg.types.Chat,
        member: tg.types.ChatMember,
        host_client: tg.client.Client
):
    
    photo = tu.null_wrapper(user.photo)
    if isinstance(photo, tu.EmptyClass):
        photo = None
        photo_info = None
    else:
        photo_info = photo.__dict__
    
    ruser = await host_client.get_users(user.id)

    return {
        "real_name": " ".join([
            str(tu.null_wrapper(user.first_name)), 
            str(tu.null_wrapper(user.last_name ))
        ]).strip(),
        "username": user.username,
        "phone": user.phone_number,
        "photo": photo_info,
        "real_photo": ruser.photo,
        "is_premium": user.is_premium,
        "join_date": str(member.joined_date),
        "tg_uid": user.id,
        "msg_analysis": await detect_user_messages(host_client, chat.id, user.id),
        "last_seen_online": str(user.last_online_date)
        # "channel": await get_channel_id(host_client, user.username),
    }

async def detect(
    chat: tg.types.Chat,
    host_client: tg.client.Client
) -> dict:
    chat_id = chat.id
    members = dict()

    count, max_count = 0, await host_client.get_chat_members_count(chat_id)
    with open(f"./reports/{chat.title.replace(' ', '_')}.report.json", "w") as f:
        f.write('{\n')
        async for member in chat.get_members():
            print(f"\r[{count+1}/{max_count}] AnalysingㅤmemberㅤID:ㅤ{member.user.id}ㅤusername:ㅤ{member.user.username}", end="") # {'ㅤ'*10}
            
            user = member.user
            sleep_time = 5
            while True:
                try:
                    members[user.id] = await plain_user_info(
                        user,
                        chat,
                        member,
                        host_client
                    )
                    f.write(tu.json_str({count: members[user.id]}, indent_size=4, start_indent=1, indent=0, exclude_keys=["real_photo", "_client"], no_start_letter=True) + (',\n' if count != max_count-1 else '\n'))
                    break
                except Exception as ex:
                    print(f"\n[Error] [Sleep for {sleep_time}s] Unknown exception: {str(ex)}")
                    time.sleep(sleep_time)
                    sleep_time *= 1.5

            count += 1
        f.write('\r}')

    # with open("report.json", "w") as f:
    #     f.write(tu.json_str(members, indent_size=4, exclude_keys=["real_photo"]))

    return members

async def load_photos(
        client: tg.Client,
        chat: tg.types.Chat,
        members
):
    os.makedirs("./reports/photos", exist_ok=True)
    os.makedirs(f"./reports/photos/{chat.title.replace(' ', '_')}", exist_ok=True)
    for user_id, user_info in members.items():
        if user_info["photo"]:
            try:
                await client.download_media(
                    user_info["real_photo"].small_file_id, 
                    file_name=f"./reports/photos/{chat.title.replace(' ', '_')}/{user_id}.jpg"
                )
            except:
                pass