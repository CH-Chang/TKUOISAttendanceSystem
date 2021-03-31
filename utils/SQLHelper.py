from pysqlcipher3 import dbapi2 as sqlite


from configs.DBConfig import key

class SQLHelper:

    def __init__(self):
        self.__connectDB()
        self.__auth()
        self.__createBasicTable()
        self.__initDB()

    def __connectDB(self) -> None:
        try:
            self.db = sqlite.connect("./db/tku.db", check_same_thread=False)
        except sqlite.Error as e:
            self.__DBFailed(e)

    def __auth(self) -> None:
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute("PRAGMA foreign_keys=ON");
            self.cursor.execute(f"PRAGMA key='{key}'")
        except sqlite.Error as e:
            self.__DBFailed(e)

    def __createBasicTable(self) -> None:
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'sys' ('id' INTEGER PRIMARY KEY NOT NULL, 'pwd' VARCHAR(255) NOT NULL,'initDB' TINYINT(1) NOT NULL,'syncSchedule' DATE);")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'staff' ('id' INTEGER PRIMARY KEY NOT NULL,'stuNum' VARCHAR(255) NOT NULL,'name' VARCHAR(255) NOT NULL);")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'period' ('id' INTEGER PRIMARY KEY NOT NULL , 'name' VARCHAR(255) NOT NULL, 'start' DATE NOT NULL, 'end' DATE NOT NULL,'priority' INT NOT NULL);")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'room' ('id' INTEGER PRIMARY KEY NOT NULL, 'room' VARCHAR(255) NOT NULL);")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS `shift` (`id` INTEGER PRIMARY KEY NOT NULL,`name` VARCHAR(255) NOT NULL,`start` TIME NOT NULL,`end` TIME NOT NULL,`hour` DECIMAL(3,1) NOT NULL,`payhour` DECIMAL(3,1) NOT NULL);")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS `arrangement` (`id` INTEGER PRIMARY KEY NOT NULL, `staff` INT NOT NULL, `week` INT NOT NULL, `shift` INT NOT NULL, `room` INT NOT NULL, `period` INT NOT NULL, CONSTRAINT `fk_arrangement_staff_staff` FOREIGN KEY (`staff`) REFERENCES `staff` (`id`) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `fk_arrangement_period_period` FOREIGN KEY (`period`) REFERENCES `period` (`id`) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `fk_arrangement_shift_shift` FOREIGN KEY (`shift`) REFERENCES `shift` (`id`) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `fk_arrangement_room_rool` FOREIGN  KEY(`room`) REFERENCES `room` (`id`) ON DELETE CASCADE ON UPDATE CASCADE);")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS `schedule` (`id` INTEGER PRIMARY KEY NOT NULL , `staff` INT NOT NULL, `date` DATE NOT NULL, `shift` INT NOT NULL, `room` INT NOT NULL, `checkIn` DATETIME, `checkOut` DATETIME, CONSTRAINT `fk_schedule_staff_staff` FOREIGN KEY (`staff`) REFERENCES `staff` (`id`) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `fk_schedule_shift_shift` FOREIGN KEY (`shift`) REFERENCES `shift` (`id`) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `fk_schedule_room_room` FOREIGN KEY (`room`) REFERENCES `room` (`id`) ON DELETE CASCADE ON UPDATE CASCADE);")
        except sqlite.Error as e:
            self.__DBFailed(e)


    def __DBFailed(self, e:sqlite.Error) -> None:
        print(e)
        self.db = None

    def close(self):
        self.cursor.close()
        self.db.close()

    def __initDB(self):
        if not self.isDBInited():
            self.cursor.execute('INSERT INTO "shift" ("name", "start", "end" , "hour", "payhour") values ("早上班", "08:10:00", "12:10:00", 4.0, 4.0), ("中午班", "12:05:00", "14:05:00", 2.0, 2.0), ("下午班", "14:00:00", "18:00:00", 4.0, 4.0), ("晚上班", "17:45:00", "21:15:00", 3.5, 3.5), ("大夜班", "21:00:00", "08:30:00", 11.5, 14.0);')
            self.cursor.execute('INSERT INTO "period" ("name", "start", "end", "priority") values ("學期", "2020-01-01", "2020-12-31", 1), ("期中考", "2020-01-01", "2020-12-31", 2), ("期末考", "2020-01-01", "2020-12-31", 2), ("寒假", "2020-01-01", "2020-12-31", 2), ("暑假", "2020-01-01", "2020-12-31", 2);')
            self.cursor.execute('INSERT INTO "room" ("room") values ("B201"), ("B203"), ("B204"), ("B206"), ("B212"), ("B213"), ("E313"), ("E314");')
            self.cursor.execute('INSERT INTO "sys" ("pwd", "initDB") values ("H5zm2A8INu5/dXvvAaWxyk9lU6qPXdaigwRgR9LHpg8=", 1);')
            self.db.commit()






    def isDBFailed(self) -> bool:
        return self.db is None

    def isDBInited(self) -> bool:
        self.cursor.execute("SELECT * FROM sys;")
        result = self.cursor.fetchall()

        if len(result)==0:
            return False

        return True




    def getSyncSchedule(self) -> list:
        self.cursor.execute("SELECT syncSchedule FROM sys WHERE id=1 ORDER BY id ASC;")
        return self.cursor.fetchall()[0][0]

    def getPWD(self) -> str:
        self.cursor.execute("SELECT pwd FROM sys WHERE id=1;")
        return self.cursor.fetchall()[0][0]




    def getAllPeriod(self) -> list:
        self.cursor.execute("SELECT * FROM period ORDER BY id ASC;")
        return self.cursor.fetchall()

    def getPeriodById(self, id: int) -> list:
        self.cursor.execute(f'SELECT * FROM period WHERE id={id} ORDER BY id ASC;')
        return self.cursor.fetchall()

    def getPeriodNotVacation(self) -> list:
        self.cursor.execute("SELECT * FROM period WHERE priority!=3 ORDER BY id ASC;")
        return self.cursor.fetchall()

    def getPeriodVacation(self) -> list:
        self.cursor.execute(f'SELECT * FROM period WHERE priority=3 ORDER BY id ASC;')
        return self.cursor.fetchall()

    def getPeriodByName(self, name: str) -> list:
        self.cursor.execute(f'SELECT * FROM period WHERE name="{name}";')
        return self.cursor.fetchall()

    def getPeriodByDate(self, date: str) -> list:
        self.cursor.execute(f'SELECT * FROM period WHERE start<="{date}" AND "{date}"<=end ORDER BY priority DESC, id ASC;')
        return self.cursor.fetchall()



    def getArrangementByPeriodAndWeek(self, period: int, week: int) -> list:
        self.cursor.execute(f"SELECT * FROM arrangement WHERE period={period} AND week={week};")
        return self.cursor.fetchall()

    def getArrangementByPeriodAndShiftsAndWeek(self, period: int, shiftIds: list, week: int) -> list:
        self.cursor.execute(f'SELECT * FROM arrangement WHERE period={period} AND week={week} AND shift in ({",".join(str(shiftId) for shiftId in shiftIds)})')
        return self.cursor.fetchall()

    def getAllArrangementDetail(self) -> list:
        self.cursor.execute("SELECT A.id AS id, A.staff AS staffNum, ST.name AS staffName, A.week AS week, A.shift AS shiftId, SH.name as shiftName, A.room AS roomId, R.room AS roomName, A.period AS periodId, P.name as periodName FROM arrangement AS A LEFT JOIN staff AS ST ON ST.id=A.staff LEFT JOIN shift AS SH ON SH.id=A.shift LEFT JOIN room as R ON R.id=A.room LEFT JOIN period as P ON P.id=A.period ORDER BY A.period ASC, A.week ASC, A.shift ASC, A.room ASC;")
        return self.cursor.fetchall()

    def getArrangementDetailById(self, id: int) -> list:
        self.cursor.execute(f'SELECT A.id AS id, A.staff AS staffNum, ST.name AS staffName, A.week AS week, A.shift AS shiftId, SH.name as shiftName, A.room AS roomId, R.room AS roomName, A.period AS periodId, P.name as periodName FROM arrangement AS A LEFT JOIN staff AS ST ON ST.id=A.staff LEFT JOIN shift AS SH ON SH.id=A.shift LEFT JOIN room as R ON R.id=A.room LEFT JOIN period as P ON P.id=A.period WHERE A.id={id} ORDER BY A.period ASC, A.week ASC, A.shift ASC, A.room ASC;')
        return self.cursor.fetchall()

    def getAllShift(self) -> list:
        self.cursor.execute(f"SELECT * FROM shift ORDER BY start;")
        return self.cursor.fetchall()

    def getShiftByName(self, name: str) -> list:
        self.cursor.execute(f'SELECT * FROM shift WHERE name="{name}";')
        return self.cursor.fetchall()

    def getShiftById(self, shiftId: int) -> list:
        self.cursor.execute(f'SELECT * FROM shift WHERE id={shiftId};')
        return self.cursor.fetchall()


    def getAllRoom(self) -> list:
        self.cursor.execute(f'SELECT * FROM room;')
        return self.cursor.fetchall()

    def getRoomByName(self, name: str) -> list:
        self.cursor.execute(f'SELECT * FROM room WHERE room="{name}";')
        return self.cursor.fetchall()

    def getRoomById(self, id: int) -> list:
        self.cursor.execute(f'SELECT * FROM room WHERE id={id};')
        return self.cursor.fetchall()



    def getScheduleByDate(self, date: str) -> list:
        self.cursor.execute(f'SELECT * FROM schedule WHERE date="{date}" ORDER BY shift asc, room asc;')
        return self.cursor.fetchall()

    def getScheduleById(self, id: int) -> list:
        self.cursor.execute(f'SELECT * FROM schedule WHERE id={id};')
        return self.cursor.fetchall()

    def getScheduleYesCheckInNoCheckOutByDateAndShift(self, date: str, shift: int):
        self.cursor.execute(f'SELECT * FROM schedule WHERE date="{date}" AND shift={shift} AND checkIn IS NOT NULL AND checkOut IS NULL;')
        return self.cursor.fetchall()

    def getScheduleNoCheckInByDateAndShift(self, date: str, shift: int):
        self.cursor.execute(f'SELECT * FROM schedule WHERE date="{date}" AND shift={shift} AND checkIn IS NULL;')
        return self.cursor.fetchall()

    def getScheduleDetailWithShiftByDateInterval(self, start: str, end: str) -> list:
        self.cursor.execute(f'SELECT SC.id, SC.date, ST.id as staffNum, ST.name as staffName, SH.id as shiftId, SH.name as shiftName, SH.start as shiftStart, SH.end as shiftEnd, SH.hour as shiftHour, SH.payhour as shiftPayHour, R.id as roomId, R.room as roomName, SC.checkIn as checkIn, SC.checkOut as checkOut FROM schedule AS SC LEFT JOIN staff AS ST ON ST.id=SC.staff LEFT JOIN shift as SH ON SH.id=SC.shift LEFT JOIN room as R ON R.id=SC.room WHERE date>="{start}" and date<="{end}" ORDER BY SC.date ASC, SC.staff ASC, SC.shift ASC, SC.room ASC')
        return self.cursor.fetchall()

    def getScheduleDetailWithShiftById(self, id: int) -> list:
        self.cursor.execute(f'SELECT SC.id, SC.date, ST.id as staffNum, ST.name as staffName, SH.id as shiftId, SH.name as shiftName, SH.start as shiftStart, SH.end as shiftEnd, SH.hour as shiftHour, SH.payhour as shiftPayHour, R.id as roomId, R.room as roomName, SC.checkIn as checkIn, SC.checkOut as checkOut FROM schedule AS SC LEFT JOIN staff AS ST ON ST.id=SC.staff LEFT JOIN shift as SH ON SH.id=SC.shift LEFT JOIN room as R ON R.id=SC.room WHERE SC.id={id} ORDER BY SC.date ASC, SC.staff ASC, SC.shift ASC, SC.room ASC')
        return self.cursor.fetchall()

    def getScheduleDetailByDateInterval(self, start: str, end: str) -> list:
        self.cursor.execute(f'SELECT SC.id, SC.date, ST.id as staffNum, ST.name as staffName, SH.id as shiftId, SH.name as shiftName, R.id as roomId, R.room as roomName, SC.checkIn as checkIn, SC.checkOut as checkOut FROM schedule AS SC LEFT JOIN staff AS ST ON ST.id=SC.staff LEFT JOIN shift as SH ON SH.id=SC.shift LEFT JOIN room as R ON R.id=SC.room WHERE date>="{start}" and date<="{end}" ORDER BY SC.date ASC, SC.staff ASC, SC.shift ASC, SC.room ASC')
        return self.cursor.fetchall()

    def getScheduleDetailByDate(self, date: str) -> list:
        self.cursor.execute(f'SELECT SC.id, SC.staff AS staffId, ST.name AS staffName, SC.date, SC.shift AS shiftId, SH.name AS shiftName, SC.room AS roomId, R.room as roomName, SC.checkIn, SC.checkOut FROM schedule AS SC LEFT JOIN staff AS ST ON SC.staff=ST.id LEFT JOIN shift AS SH ON SC.shift=SH.id LEFT JOIN room AS R ON SC.room=R.id WHERE SC.date="{date}" ORDER BY SC.shift ASC, SC.room ASC;')
        return self.cursor.fetchall()

    def getScheduleDetailById(self, id: int) -> list:
        self.cursor.execute(f'SELECT SC.id, SC.staff AS staffId, ST.name AS staffName, SC.date, SC.shift AS shiftId, SH.name AS shiftName, SC.room AS roomId, R.room as roomName, SC.checkIn, SC.checkOut FROM schedule AS SC LEFT JOIN staff AS ST ON SC.staff=ST.id LEFT JOIN shift AS SH ON SC.shift=SH.id LEFT JOIN room AS R ON SC.room=R.id WHERE SC.id={id} ORDER BY SC.shift ASC, SC.room ASC;')
        return self.cursor.fetchall()

    def getCrossDayScheduleDetailByDate(self, date: str) -> list:
        self.cursor.execute(
            f'SELECT SC.id, SC.staff AS staffId, ST.name AS staffName, SC.date, SC.shift AS shiftId, SH.name AS shiftName, SC.room AS roomId, R.room as roomName, SC.checkIn, SC.checkOut FROM schedule AS SC LEFT JOIN staff AS ST ON SC.staff=ST.id LEFT JOIN shift AS SH ON SC.shift=SH.id LEFT JOIN room AS R ON SC.room=R.id WHERE SC.date="{date}" AND SH.start>SH.end ORDER BY SC.shift ASC, SC.room ASC;')
        return self.cursor.fetchall()


    def getAllStaff(self):
        self.cursor.execute("SELECT * FROM staff ORDER BY id ASC;")
        return self.cursor.fetchall()

    def getStaffById(self, id: int) -> list:
        self.cursor.execute(f'SELECT * FROM staff WHERE id={id};')
        return self.cursor.fetchall()



    def updateSyncSchedule(self, date: str) -> None:
        self.cursor.execute(f'UPDATE sys SET syncSchedule="{date}";')
        self.db.commit()

    def updatePWD(self, password):
        self.cursor.execute(f'UPDATE sys SET PWD="{password}";')
        self.db.commit()

    def updatePeriodStartAndEndById(self, start: str, end: str, id: int):
        self.cursor.execute(f'UPDATE period SET start="{start}", end="{end}" WHERE id={id};')
        self.db.commit()

    def updateScheduleCheckInById(self, datetime: str, id: int) -> None:
        self.cursor.execute(f'UPDATE schedule SET checkIn="{datetime}" WHERE id={id};')
        self.db.commit()

    def updateScheduleCheckOutById(self, datetime: str, id: int) -> None:
        self.cursor.execute(f'UPDATE schedule SET checkOut="{datetime}" WHERE id={id};')
        self.db.commit()

    def updateScheduleCheckInNullById(self, id: int) -> None:
        self.cursor.execute(f'UPDATE schedule SET checkIn=NULL WHERE id={id};')
        self.db.commit()

    def updateScheduleCheckOutNullById(self, id: int) -> None:
        self.cursor.execute(f'UPDATE schedule SET checkOut=NULL WHERE id={id};')
        self.db.commit()

    def updateScheduleById(self, staff: int, shift: int, room: int, id: int):
        self.cursor.execute(f'UPDATE schedule SET staff={staff}, shift={shift}, room={room} WHERE id={id};')
        self.db.commit()

    def updateStaffById(self, id: int,stuNum: str,name: str) -> None:
        self.cursor.execute(f'UPDATE staff SET stuNum="{stuNum}", name="{name}" WHERE id={id};')
        self.db.commit()

    def updatePeriodById(self, id: int, name: str, start: str, end: str) -> None:
        self.cursor.execute(f'UPDATE period SET name="{name}", start="{start}", end="{end}" WHERE id={id};')
        self.db.commit()

    def updateArrangementById(self, id: int, staff: int, week:int, shift: int, room: int, period: int) -> None:
        self.cursor.execute(f'UPDATE arrangement SET staff={staff}, week={week}, shift={shift}, room={room}, period={period} WHERE id={id};')
        self.db.commit()

    def updateShiftById(self, id: int, name: str, start: str, end: str, hour: float, payHour: float) -> None:
        self.cursor.execute(f'UPDATE shift SET name="{name}", start="{start}", end="{end}", hour={hour}, payhour={payHour} WHERE id={id};')
        self.db.commit()

    def updateRoomById(self, id: int, name: str) -> None:
        self.cursor.execute(f'UPDATE room SET room="{name}" WHERE id={id};')
        self.db.commit()






    def delAllStaff(self):
        self.cursor.execute(f'DELETE FROM staff;')
        self.db.commit()

    def delStaffById(self, id: int):
        self.cursor.execute(f'DELETE FROM staff WHERE id={id};')
        self.db.commit()


    def delArrangementByPeriod(self, period):
        self.cursor.execute(f'DELETE FROM arrangement WHERE period={period};')
        self.db.commit()

    def delArrangementById(self, id: int):
        self.cursor.execute(f'DELETE FROM arrangement WHERE id={id};')
        self.db.commit()



    def delScheduleByShiftsAndDate(self, shiftIds: list, date: str):
        self.cursor.execute(f'DELETE FROM schedule WHERE shift in ({",".join(str(shiftId) for shiftId in shiftIds)}) AND date="{date}";')
        self.db.commit()

    def delScheduleByDate(self, date: str):
        self.cursor.execute(f'DELETE FROM schedule WHERE date="{date}";')
        self.db.commit()

    def delScheduleById(self, id: int):
        self.cursor.execute(f'DELETE FROM schedule WHERE id={id};')
        self.db.commit()

    def delPeriodById(self, id: int) -> None:
        self.cursor.execute(f'DELETE FROM period WHERE id={id};')
        self.db.commit()

    def delShiftById(self, id: int) -> None:
        self.cursor.execute(f'DELETE FROM shift WHERE id={id};')
        self.db.commit()

    def delRoomById(self, id: int) -> None:
        self.cursor.execute(f'DELETE FROM room WHERE id={id};')
        self.db.commit()





    def newAllStaff(self, data: list):
        for item in data:
            self.cursor.execute(f'INSERT INTO staff (id, stuNum, name) values ({item[0]}, "{item[1]}", "{item[2]}");')
        self.db.commit()

    def newStaff(self, id: int, stuNum: str, name: str):
        self.cursor.execute(f'INSERT INTO staff (id, stuNum, name) VALUES ({id},"{stuNum}","{name}");')
        self.db.commit()




    def newArrangements(self, data: list):
        for item in data:
            self.cursor.execute(f'INSERT INTO arrangement (staff, week, shift, room, period) values ({item[0]},{item[1]},{item[2]},{item[3]},{item[4]})')
        self.db.commit()

    def newArrangement(self, staff: int, week:int, shift: int, room: int, period: int):
        self.cursor.execute(f'INSERT INTO arrangement (staff, week, shift, room, period) values ({staff},{week},{shift},{room},{period})')
        self.db.commit()






    def newSchedules(self, date: str,  arrangements: list):
        for arrangement in arrangements:
            self.cursor.execute(f'INSERT INTO schedule (staff, date, shift, room) values ({arrangement[1]},"{date}",{arrangement[3]}, {arrangement[4]});')
        self.db.commit()

    def newSchedule(self, date: str, staff: int, shift: int, room: int):
        self.cursor.execute(f'INSERT INTO schedule (staff, date, shift, room) VALUES ({staff},"{date}",{shift}, {room});')
        self.db.commit()



    def newPeriodVacation(self, name: str, start: str, end: str):
        self.cursor.execute(f'INSERT INTO period (name, start, end, priority) VALUES ("{name}", "{start}", "{end}", 3);')
        self.db.commit()

    def newShift(self, name: str, start: str, end: str, hour: float, payHour: float):
        self.cursor.execute(f'INSERT INTO shift (name, start, end, hour, payhour) VALUES ("{name}","{start}", "{end}", {hour}, {payHour});')
        self.db.commit()

    def newRoom(self, name: str):
        self.cursor.execute(f'INSERT INTO room (room) VALUES ("{name}");')
        self.db.commit()








