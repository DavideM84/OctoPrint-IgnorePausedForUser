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
        self.historySize = 10 if self.historySize < 1 or self.historySize > 1000 else self.historySize
        self.job = None

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
        id = self.job["id"]
        self.logger.info(f"History > Stop job id: '{id}'")
        self.job["endedAt"] = datetime.now().isoformat()
        self.job["state"] = "cancelled" if cancelled else "done"
        self.updateJob()
        self.job = None

    def UpdateCount(self, count):
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
        if self.job != None:
            data = self.readHistory()
            currSize = len(data["jobs"])
            if (currSize >= self.historySize):
                data["jobs"].clear()
            data["jobs"].append(self.job)
            self.writeHistory(data)

    def updateJob(self):
        if self.job != None:
            data = self.readHistory()
            for job in data["jobs"]:
                if job["id"] == self.job["id"]:
                    self.copyObject(self.job, job)
                    self.writeHistory(data)
                    break

    def readHistory(self):
        if not os.path.exists(self.historyFile):
            self.writeHistory({ "jobs": [] })
        with open(self.historyFile, "r") as f:
            data = json.load(f)
        return data

    def writeHistory(self, data):
        with open(self.historyFile, "w") as f:
            json.dump(data, f)

    def copyObject(self, src, dest):
        dest["endedAt"] = src["endedAt"]
        dest["state"] = src["state"]
        dest["pauses"] = src["pauses"]
        #dest["startedAt"] = src["startedAt"]
        #dest["gcode"] = src["gcode"]
        #dest["size"] = src["size"]
        #dest["origin"] = src["origin"]
        #dest["user"] = src["user"]