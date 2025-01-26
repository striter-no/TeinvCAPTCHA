import pyrogram as tg
import src.Main.arguments as argsm
import src.Main.detection_call as dtc
import src.Other.app_init as init
import src.Other.archiver as arch
import src.Detector.detector as raw_dtc

configs = init.Configs(
    "./configs/tg-config.json",
    "./configs/app-config.json"
)

app = init.App(configs)
host_client = app.get_client()

@host_client.on_message()
async def callback(client: tg.client.Client, message: tg.types.Message):
    if not (message.text) or not (message.from_user) or not (message.from_user.id == configs.YOUR_ID): return

    arguments = message.text
    cmd, args = \
        argsm.get_arguments(arguments)["command"], \
        argsm.get_arguments(arguments)["arguments"]
    
    if cmd != "!anl": return

    if not argsm.check_arg(args, "no_delete"):
        await client.delete_messages(
            message.chat.id, 
            message.id
        )

    detect_info = await dtc.detection(
        message.text,
        message.chat,
        message.id,
        host_client,
        args
    )

    if detect_info["target_chat"] == None:
        print("detection failed due unable to get target chat")
        return

    await dtc.download_avatars(
        host_client,
        detect_info
    )
    
    chat_hash = raw_dtc.get_chat_name(
        detect_info["target_chat"]
    )[0]

    arch.archive_report(chat_hash)

    if argsm.check_arg(args, "send_back"):
        await host_client.send_document(
            configs.YOUR_ID,
            open(f"./reports/archives/{chat_hash}.zip", "rb"),
            file_name=f"{chat_hash}.zip",
        )

if __name__ == "__main__":
    app.run()