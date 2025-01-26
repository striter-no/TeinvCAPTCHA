import src.Analysis.gpt_source as gpt
import json as jn
import datetime as dat
import os
import csv

dat_convert = lambda date_str: dat.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

class Message:
    def __init__(
        self,
        data: dict,
        trust_level: float
    ) -> None:
        self.trust_level: float = trust_level
        self.text = ""
        self.id = -1
        self.date: (dat.datetime | None) = None
        self.redacted_time = None

        if trust_level == 0:
            pass
        elif trust_level == 0.1:
            self.text: str = data["text"]
            self.id: int = int(data["id"])
            self.date: (dat.datetime | None) = None if data["date"] == "None" else dat_convert(data["date"])
            self.redeacted_time: (dat.datetime | None) = None if data["redacted_time"] == "None" else dat_convert(data["redacted_time"])
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
    ) -> None:
        self.real_name: str = data["real_name"]
        self.username: str = data["username"]
        self.phone: str = data["phone"]
        self.is_premium: bool = data["is_premium"] == "True"
        self.join_date: (dat.datetime | None) = None if data["join_date"] == "None" else dat_convert(data["join_date"])
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

        self.last_seen_online: (dat.datetime | None) = None if data["last_seen_online"] == "None" else dat_convert(data["last_seen_online"])
    
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
        out += f"\n\tmessages:" + ("\n" + ("\n".join(["\t\t"+str(msg).replace("\t", "\t\t\t") for msg in self.messages])) if (len(self.messages) > 0) else "No messages provided by detector")
        return out

class PersonReport:
    def __init__(self, data: dict, person: Person) -> None:
        self.person: Person = person
        self.data: dict = data
    
    def __str__(self):
        out = "Person Report:"
        out += f"\n\tperson: \n{'-'*15}\n{self.person}\n{'-'*15}"
        out += f"\n\tlocal data: {self.data}"
        return out

class NamesDataBase:
    def __init__(self, path: str) -> None:

        names = set()
        surnames = set()

        with open(path) as dbf:
            reader = csv.reader(dbf)

            for rows in reader:
                names   .add(rows[1])
                surnames.add(rows[0])
        
        self.names = list(names)
        self.surnames = list(surnames)

class AnalysierConfig:
    def __init__(self) -> None:
        self.triger_procentage = 98
        self.max_realname_len = 30

class Analysier:
    def __init__(self, anl_chat_name: str, db: NamesDataBase, gpt_chat: gpt.Chat) -> None:
        self.gpt_chat = gpt_chat
        self.persons: list[Person] = []
        self.anl_chat: dict = jn.load(open(f"./reports/{anl_chat_name}.report.json"))
        self.anl_name: str = anl_chat_name
        self.config = AnalysierConfig()
        self.db = db

    def load_info(self):
        for num, person_data in self.anl_chat.items():
            self.persons.append(
                Person(person_data, self.anl_name)
            )

    def analysie_all(self):
        persons = []
        for person in self.persons:
            this_report = self.analysie_person(person)
            if this_report.data["UDI"][0] >= self.config.triger_procentage:
                
                if len(person.real_name) >= self.config.max_realname_len:
                    continue
                
                spl = person.real_name.split()
                name, surname = spl[0], ""
                if len(spl) > 1:
                    surname = spl[1]

                name = name.upper().strip()
                surname = surname.upper().strip()

                if surname == '-': surname = ''
                if name == '-': name = ''

                if len(name) == 0: name = None
                if len(surname) == 0: surname = None

                if not ((self.db.surnames.count(surname) != 0) or (self.db.names.count(name) != 0)):
                    # print(f"Name: {name} and surname: {surname} not in DB")
                    continue

                persons.append((person, this_report))
        
        return persons

    # UDI = userbot/dead/inactive account
    def analysie_person(self, person: Person):
        report = PersonReport({}, person)

        if person.trust_level == 1:
            report.data["UDI"] = (0, "False")
        elif person.trust_level == 0.5:
            report.data["UDI"] = (50, "Maybe")
        elif person.trust_level == 0.1:
            report.data["UDI"] = (70,  "Double check please, 70% True")
        elif person.trust_level == 0:
            report.data["UDI"] = (98,  "Ping him, 98% he is UDI")
        
        return report