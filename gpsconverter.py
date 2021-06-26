class GPSConverter:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def lat_ref(self):
        if self.latitude >= 0:
            return "N"
        else:
            return "S"

    def lon_ref(self):
        if self.longitude >= 0:
            return "E"
        else:
            return "W"

    def to_dms(self, op: float):
        dd = abs(op)
        mnt, sec = divmod(dd * 3600, 60)
        deg, mnt = divmod(mnt, 60)
        return round(deg, 4), round(mnt, 4), round(sec, 4)

    def strlat(self):
        deg, mnt, sec = self.to_dms(self.latitude)
        deg = int(deg)
        mnt = int(mnt)
        sec, div = self.process_sec(sec)
        return "{0}/1,{1}/1,{2}/{3}".format(deg, mnt, sec, div)

    def strlon(self):
        deg, mnt, sec = self.to_dms(self.longitude)
        deg = int(deg)
        mnt = int(mnt)
        sec, div = self.process_sec(sec)
        return "{0}/1,{1}/1,{2}/{3}".format(deg, mnt, sec, div)

    def process_sec(self, sec):
        strsec = str(sec)
        if "." in strsec:
            seclen = len(strsec) - 2
        else:
            seclen = len(strsec) - 1
        divstr = str("1" + "0" * seclen)
        div = int(divstr)
        return int(sec * div), div
