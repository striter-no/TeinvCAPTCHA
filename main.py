'''
Version: Beta 1
- Real name
- Username (@...)
- Premium Status
- Join Date (for group)
- Telegram User UID
- Messages analysis:
   - Count
   - Messages (if count is beneath 50)
   - Trust level:
      - 0: Probably Bot or Dead account
      - 0.5: Take a close look
      - 1: Probably real user
- Last seen online date

Version: Beta 2
- Now can analysie group without printing something into it


'''

import asyncio

import pyrogram as tg
import json as jn
import src.detector as dtc
import src.archiver as arch

tg_config = jn.load(open('./tg-config.json'))
api_id = tg_config["api_id"]
api_hash = tg_config["api_hash"]

YOUR_ID = tg_config["your_id"]
AVATAR_TRESHHOLD = 1000

app = tg.Client(
    name="TeinvCAPTCHA agent: beta 2",
    api_id=api_id, 
    api_hash=api_hash
)

async def get_chat_by_id(
        chat_id: int,
        chat_type: str,
        client: tg.client.Client
):
    try:
        oid = ""
        if chat_type == "group":
            oid = "-"
        elif chat_type == "supergroup":
            oid = "-100"
        
        chat = await client.get_chat(oid+str(chat_id))
        return chat
    except Exception as e:
        print(f"[Error][While fetching chat by ID]: {e}")
        return None

def get_arguments(text: str):
    splitted = list(map(lambda x:x.strip(), text.replace("\n", "").strip().split()))

    cmd = splitted[0]
    arguments = dict()

    for arg in splitted[1:]:
        arg = arg[2:]
        if arg.count('=') != 0:
            eq_splitted = arg.split('=')
            arguments[eq_splitted[0]] = " ".join(eq_splitted[1:])
        else:
            arguments[arg] = True
    
    return {
        "command": cmd,
        "arguments": arguments
    }

@app.on_message()
async def callback(client: tg.client.Client, message: tg.types.Message):
    # print(f"\rnew message from {message.chat.id}: {message.text}", end="\n")

    if message.text and message.from_user and message.from_user.id == YOUR_ID:
        
        args = get_arguments(message.text)
        
        if args["command"] != "!anl":
            return

        group_type = args["arguments"]["group_type"]
        chat_id = args["arguments"]["chat_id"]

        origin_chat = message.chat
        target_chat = await get_chat_by_id(int(chat_id), group_type, app)
        
        await client.delete_messages(
            origin_chat.id, 
            message.id
        )

        print("Gaining members... ", end = "")
        members = await dtc.detect(target_chat, app)
        print("Ok!")

        print("Gaining user photos... ", end = "")
        
        if len(list(members.keys())) < AVATAR_TRESHHOLD:
            await dtc.load_photos(app, target_chat, members)
            print("Ok!")
        else:
            await dtc.load_photos(app, target_chat, members[:AVATAR_TRESHHOLD])
            print("Stopped on treshhold due ennormous amount of data.")
        
        print("Archiving report...")
        arch.archive_report(
            target_chat.title.replace(' ', '_')
        )
        print("Ok!")

        if args["arguments"]["send_back"]:
            await app.send_document(
                YOUR_ID,
                open(f"./reports/archives/{target_chat.title.replace(' ', '_')}.zip", "rb"),
                file_name=f"{target_chat.title.replace(' ', '_')}.zip",
            )



def main():
    app.run()

if __name__ == "__main__":
    main()