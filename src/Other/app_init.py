import pyrogram as tg
import json as jn

class Configs:
    def __init__(
            self,
            pathToTGConfig: str,
            pathToAppConfig: str
    ):
        self.tg_config = jn.load(open(pathToTGConfig))
        self.app_config = jn.load(open(pathToAppConfig))
        
        self.api_id = self.tg_config["api_id"]
        self.api_hash = self.tg_config["api_hash"]
        self.YOUR_ID = self.tg_config["your_id"]

        self.app_name = self.app_config["app_name"]
        self.working_dir = self.app_config["working_dir"]
        self.reports_dir = self.app_config["reports_dir"]

class App:
    def __init__(self, configs: Configs):
        self.config = configs
        self.app = tg.client.Client(
            name=self.config.app_name,
            api_id=self.config.api_id,
            api_hash=self.config.api_hash,
            workdir=self.config.working_dir
        )

    def get_client(self):
        return self.app

    def run(self):
        self.app.run()