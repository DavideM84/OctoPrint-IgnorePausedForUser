import os, json, uuid, logging
from datetime import datetime

class History:
    
    def __init__(self, logger, pluginDataFolder, historySize = 10):
        self.logger = logger
        self.historyFile = f"{pluginDataFolder}/history.dat"
        if isinstance(historySize, str):
            self.historySize = int(historySize) if historySize.isdigit() else 10
        else:
            self.historySize = historySize
        self.historySize = 3 if self.historySize < 1 or self.historySize > 10 else self.historySize
        self.job = None

    def GetAll(self):
        data = { "jobs": [] }
        if os.path.exists(self.historyFile):
            with open(self.historyFile, "r") as f:
                data = json.load(f)
        return data

    def StartJob(self, payload):
        id = str(uuid.uuid4())
        self.logger.info(f"History > Start job id: '{id}'")
        self.job = {
            "id": id,
            "startedAt": datetime.now().isoformat(),
            "endedAt": "",
            "gcode": payload["name"],
            "size": payload["size"],
            "origin": payload["origin"],
            "user": payload["user"],
            "state": "printing",
            "pauses": 0
        }
        self.addJob()

    def StopJob(self, cancelled):
        if self.job is not None:
            id = self.job["id"]
            self.logger.info(f"History > Stop job id: '{id}'")
            self.job["endedAt"] = datetime.now().isoformat()
            self.job["state"] = "cancelled" if cancelled else "done"
            self.updateJob()
            self.job = None

    def UpdateCount(self, count):
        if self.job is not None:
            id = self.job["id"]
            self.logger.info(f"History > Update job id: '{id}' count: {count}")
            self.job["pauses"] = count
            self.updateJob()

    def ClearHistory(self):
        self.logger.info(f"History > Clear")
        if os.path.exists(self.historyFile):
            os.remove(self.historyFile)

    #####

    def addJob(self):
        if self.job is not None:
            if not os.path.exists(self.historyFile):
                with open(self.historyFile, "w") as f:    
                    json.dump({ "jobs": [] }, f)    

            with open(self.historyFile, "r+") as f:
                data = json.load(f)
                currSize = len(data["jobs"])
                if (currSize >= self.historySize):
                    data["jobs"].clear()
                data["jobs"].append(self.job)
                f.seek(0)
                json.dump(data, f)
                f.truncate()

    def updateJob(self):
        if self.job is not None:
            with open(self.historyFile, "r+") as f:
                data = json.load(f)
                for job in data["jobs"]:
                    if job["id"] == self.job["id"]:
                        job["endedAt"] = self.job["endedAt"]
                        job["state"] = self.job["state"]
                        job["pauses"] = self.job["pauses"]
                        f.seek(0)
                        json.dump(data, f)
                        f.truncate()
                        break
 