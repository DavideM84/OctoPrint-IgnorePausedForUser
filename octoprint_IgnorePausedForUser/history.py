import os, json, uuid
from datetime import datetime

class History:
    
    def __init__(self, pluginDataFolder):
        self.dataFolder = pluginDataFolder
        self.job = None

    def StartJob(self, payload):
        self.job = {
            "id": str(uuid.uuid4()),
            "startedAt": datetime.now(),
            "endedAt": None,
            "user": payload.user,
            "gcode": payload.name,
            "size": payload.size,
            "state": "printing",
            "pauses": 0
        }
        self.addJob()

    def StopJob(self, cancelled):
        self.job.endedAt = datetime.now()
        if cancelled:
            self.job.state = "cancelled"
        else:
            self.job.state = "done"
        self.updateJob()

    def UpdateCount(self, count):
        self.job.pauses = count
        self.updateJob()


    def addJob(self):
        data = self.readFromFile()
        data.jobs.append(self.job)
        self.writeToFile(data)

    def updateJob(self):
        data = self.readFromFile()
        for job in data["jobs"]:
            if job["id"] == self.job["id"]:
                job = self.job
                self.writeToFile(data)
                break

    def readFromFile(self):
        dataFile = self.dataFolder + "\\history.dat"
        if os.path.exists(dataFile):
            with open(dataFile, "r") as f:
                data = json.load(f)
        else:
            data = { "jobs": [] }
        return data

    def writeToFile(self, data):
        dataFile = self.dataFolder + "\\history.dat"
        with open(dataFile, "w") as f:
            json.dump(data, f)