import os
import json
import gdown

class Setup():
    def __init__(self) -> None:
        self.config = json.load(open("./config/config.json"))
    
    def model_downloader(self) -> None:
        if "best.pt" not in os.listdir("./storage"):
            gdown.download(self.config["model_url"], "./storage/best.pt", quiet=False)
            
    def setup_process(self) -> None:
        self.model_downloader()