from utils.SQLHelper import SQLHelper
from datetime import datetime, timedelta

class ShiftHelper:

    def __init__(self):
        self.initSQL()

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def getShiftByTime(self, time):

        time = datetime.strptime(time, "%H:%M:%S")

        shifts = self.SQLHelper.getAllShift()

        for shift in shifts:
            start = datetime.strptime(f"{shift[2]}", "%H:%M:%S")
            end = datetime.strptime(f"{shift[3]}", "%H:%M:%S")
            if start>end:
                end += timedelta(days=1)
            if start <= time <= end:
                return shift



    def getShiftStatus(self, shiftId, date , checkIn, checkOut):

        now = datetime.now()

        try:
            checkIn = datetime.strptime(checkIn, "%Y-%m-%d %H:%M:%S")
        except:
            checkIn = None
        try:
            checkOut = datetime.strptime(checkOut, "%Y-%m-%d %H:%M:%S")
        except:
            checkOut = None

        shift = self.SQLHelper.getShiftById(shiftId)

        shouldCheckIn = datetime.strptime(f'{date} {shift[0][2]}', "%Y-%m-%d %H:%M:%S")
        shouldCheckOut = datetime.strptime(f'{date} {shift[0][3]}', "%Y-%m-%d %H:%M:%S")


        if shouldCheckIn>shouldCheckOut:
            shouldCheckOut+=timedelta(days=1)


        if now<shouldCheckIn:
            if not checkIn is None and not checkOut is None:
                return "早退"
            elif not checkIn is None:
                return "執行中"
            else:
                return "未執行"
        elif shouldCheckIn<=now<shouldCheckOut:
            if checkIn is None:
                return "已遲到未執行"
            elif checkIn>=shouldCheckIn and checkOut is None:
                return "已遲到執行中"
            elif checkOut is None:
                return "執行中"
            elif checkIn>=shouldCheckIn and checkOut<shouldCheckOut:
                return "遲到早退"
            elif checkIn>=shouldCheckIn and checkOut>=shouldCheckOut:
                return "遲到"
            elif checkIn<shouldCheckIn and checkOut<shouldCheckOut:
                return "早退"
        else:
            if checkIn is None and checkOut is None:
                return "曠班"
            elif checkOut is None:
                return "未簽退"
            elif checkIn>=shouldCheckIn and checkOut<shouldCheckOut:
                return "遲到早退"
            elif checkIn>=shouldCheckIn:
                return "遲到"
            elif checkOut<shouldCheckOut:
                return "早退"
            elif checkIn<shouldCheckIn and checkOut>=shouldCheckOut:
                return "準時"








