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

tg_config = jn.load(open('./tg-config.json'))
api_id = tg_config["api_id"]
api_hash = tg_config["api_hash"]

app = tg.Client(
    name="myUser",

    api_id=api_id, 
    api_hash=api_hash
)

async def get_chat_by_id(
        chat_id: int,
        client: tg.client.Client
):
    try:
        chat = await client.get_chat(int("-100"+str(chat_id)))
        return chat
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

@app.on_message()
async def callback(client: tg.client.Client, message: tg.types.Message):
    # if message.text and message.chat.id==5243956136:
    # print(f"\rnew message from {message.chat.id}: {message.text}", end="")

    if message.text and message.from_user and message.from_user.id == 5243956136:
        spl_txt = message.text.split()
        if spl_txt[0] != "!anl":
            return

        origin_chat = message.chat
        target_chat = await get_chat_by_id(int(spl_txt[1]), app)
        user = message.from_user
        
        await client.delete_messages(
            origin_chat.id, 
            message.id
        )

        # print(f"Chat ID: {message.chat.id} ({message.chat.type})\n\tContent: {str(message.text[:100]).strip()}")
        
        # json_print(await dtc.full_user_info(chat, user, client), indent_size=4)
        print("Gaining members... ", end = "")
        members = await dtc.detect(target_chat, app)
        print("Ok!")
        print("Gaining user photos... ", end = "")
        if len(list(members.keys())) < 500:
            await dtc.load_photos(app, target_chat, members)
            print("Ok!")
        else:
            print("Stopped due ennormous amount of data.")

def json_print(data, indent_size=4, indent=0):
    print('{')
    for k, v in data.items():
        print(f"{' '*(indent_size*(indent+1))}"+str(k)+': ', end='')
        if isinstance(v, dict):
            json_print(v, indent_size=indent_size, indent=indent+2)
        else:
            # print(f"Not a dict, it is {type(v)}")
            print(str(v))
    
    print(f"{' '*(indent_size*max(indent-1, 0))}"+'}')

def main():
    app.run()

if __name__ == "__main__":
    
    # Хата: -1001853540825
    # Хата: XXXX1853540825

    main()