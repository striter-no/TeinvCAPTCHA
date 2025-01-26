import src.Other.tg_utils as tgu
import src.Other.type_utils as tu
import src.Detector.detector as dtc

import pyrogram as tg

async def detection(
    message_text: str,
    message_chat: tg.types.Chat,
    message_id: int,

    host_client: tg.client.Client, 
    args: dict
):

    # Getting origin and target chat
    origin_chat = message_chat
    target_chat = await tgu.get_chat_by_id(
        args["chat_id"], 
        args["group_type"], 
        host_client
    )
    if target_chat is None:
        print("Error while fetching target chat")
        return {
            "members": {},
            "target_chat": None,
            "origin_chat": origin_chat
        }

    # Gaining members from target chat

    members = await dtc.detect(
        target_chat,
        host_client
    )

    return {
        "members": members,
        "target_chat": target_chat,
        "origin_chat": origin_chat
    }

async def download_avatars(
    host_client: tg.client.Client,
    detect_info: dict
):
    await dtc.load_photos(
        host_client, 
        detect_info["target_chat"], 
        detect_info["members"]
    )