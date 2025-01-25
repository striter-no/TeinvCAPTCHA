import src.gpt_source as gpt
import json as jn
import datetime as dat
import os

dat_convert = lambda date_str: dat.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

class Message:
    def __init__(
        self,
        data: dict,
        trust_level: float
    ):
        self.trust_level: float = trust_level
        self.text = ""
        self.id = -1
        self.date: dat.datetime = dat.datetime(0, 0, 0)
        self.redacted_time = dat.datetime(0, 0, 0)

        if trust_level == 0:
            pass
        elif trust_level == 0.1:
            self.text: str = data["text"]
            self.id: int = int(data["id"])
            self.date: dat.datetime = dat_convert(data["date"])
            self.redeacted_time: dat.datetime = dat_convert(data["redacted_time"])
        elif trust_level == 0.5:
            self.text = data["text"]
            self.redeacted_time = data["redacted_time"]
        else:
            pass
    
    def __str__(self):
        return "Message:" + \
            f"\n\ttrust_level: {self.trust_level}" + \
            f"\n\ttext: {self.text}" + \
            f"\n\tid: {self.id}" + \
            f"\n\tdate: {self.date}" + \
            f"\n\tredacted_time: {self.redacted_time}"

class Person:
    def __init__(
        self,
        data: dict,
        chat_name: str,
    ):
        self.real_name: str = data["real_name"]
        self.username: str = data["username"]
        self.phone: str = data["phone"]
        self.is_premium: bool = data["is_premium"] == "True"
        self.join_date: dat.datetime = dat_convert(data["join_date"])
        self.tg_uid: int = int(data["tg_uid"])
        self.photo: (str | None) = f"./reports/photos/{chat_name}/{self.tg_uid}.jpg" if os.path.exists(f"./reports/photos/{chat_name}/{self.tg_uid}.jpg") else None

        msg_analysis = data["msg_analysis"]

        self.trust_level: float = float(msg_analysis["trust_level"])
        self.messages_count: int = int(msg_analysis["count"])

        self.messages: list[Message] = []
        for num, message_data in msg_analysis["messages"].items():
            self.messages.append(
                Message(message_data, self.trust_level)
            )
        
        self.last_seen_online: dat.datetime = dat_convert(data["last_seen_online"])
    
    def __str__(self):
        out = "Person Info:"
        out += f"\n\treal_name: {self.real_name}"
        out += f"\n\tusername: {self.username}"
        out += f"\n\tphone: {self.phone}"
        out += f"\n\tis_premium: {self.is_premium}"
        out += f"\n\tjoin_date: {self.join_date}"
        out += f"\n\ttg_uid: {self.tg_uid}"
        out += f"\n\tphoto: {self.photo}"
        out += f"\n\ttrust_level: {self.trust_level}"
        out += f"\n\tmessages_count: {self.messages_count}"
        out += f"\n\tlast_seen_online: {self.last_seen_online}"
        out += f"\n\tmessages:\n" + "\n".join([str(msg).replace("\t", "\t\t") for msg in self.messages])
        return out

class Analysier:
    def __init__(self, anl_chat_name: str, gpt_chat: gpt.Chat):
        self.gpt_chat = gpt_chat
        self.persons: list[Person] = []
        self.anl_chat: dict = jn.load(open(f"./reports/{anl_chat_name}"))
        self.anl_name: str = anl_chat_name

    def load_info(self):
        for num, person_data in self.anl_chat.items():
            self.persons.append(
                Person(person_data, self.anl_name)
            )

    def analysie_all(self):
        for person in self.persons:
            self.analysie_person(person)

    def analysie_person(self, person: Person):
        print(str(person))