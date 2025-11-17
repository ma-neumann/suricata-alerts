import json
import os

class SuricataAlertReader:
    def __init__(self, eve_path="/logs/eve.json"):
        self.eve_path = eve_path
        self._file = None
        self._inode = 0
        self._position = 0

    def _open_file(self):
        if not os.path.exists(self.eve_path):
            raise FileNotFoundError(f"EVE log not found at: {self.eve_path}")
        self._file = open(self.eve_path, "r", encoding="utf-8")
        self._file.seek(self._position)
        self._inode = os.stat(self.eve_path).st_ino

    def _rotated(self):
        try:
            if os.stat(self.eve_path).st_ino != self._inode:
                return True
        except FileNotFoundError:
            return False
        return False

    def get_new_alerts(self):
        if self._file is None:
            self._open_file()
        elif self._rotated():
            self._file.close()
            self._file = None
            self._position = 0
            self._open_file()
        else:
            self._file.seek(self._position)

        new_alerts = []
        while True:
            line = self._file.readline()
            if not line:
                break
            try:
                event = json.loads(line)
                if event["event_type"] == "alert":
                    new_alerts.append(event)
            except json.JSONDecodeError:
                continue

        self._position = self._file.tell()
        return new_alerts

    def close(self):
        if self._file:
            self._file.close()
            self._file = None
