import pyrogram as tg
import src.Other.type_utils as tu

async def get_chat_by_id(
        chat_id: (int | str),
        chat_type: str,
        client: tg.client.Client
):

    oid = ""
    if chat_type == "group":
        oid = "-"
    elif chat_type == "supergroup":
        oid = "-100"
    
    if isinstance(chat_id, str) and tu.isnum(chat_id):
        chat_id = int(chat_id)

    print(f"Getting chat ID... ({oid}{chat_id})")
    # print(await client.resolve_peer(chat_id))

    chat = None
    try:
        chat = await client.get_chat(oid+str(chat_id))
    except Exception as e:
        print(f"[Error][While fetching chat by ID]: {e}")

    if chat == None:
        print(f"Chat not found.")

    return chat