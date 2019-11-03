import pymysql

from BABY_ANALYSIS import BABY_ANALYSIS

dbServerName = "127.0.0.1"
dbUser = "samyibrahim"
dbPassword = "samizosan"
dbName = "IOT_SMART_BABY_MONITORING"
charSet = "utf8mb4"
cusrorType = pymysql.cursors.DictCursor

# Create a connection object
connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,
                                   db=dbName, charset=charSet, cursorclass=cusrorType)


# This was used the first time running the project to create the table, I do not think we need this anymore
# Notice: ALWAYS set Auto increment for id
def createBabyAnalysisTable():
    with connectionObject:
        cur = connectionObject.cursor()
        cur.execute("CREATE TABLE BABY_ANALYSIS (id int NOT NULL AUTO_INCREMENT, babyName varchar(255) NOT NULL, "
                    "babyAge int NOT NULL,"
                    "babyHeight int NOT NULL, babyWeight int NOT NULL, averageNumberOfWakeupsPerDay int NOT NULL, "
                    "averageWakeupTimesPerDay varchar(255) NOT NULL,"
                    "averageNumberOfFeedsPerDay int NOT NULL,  averageFeedTimesPerDay varchar(255) NOT NULL, "
                    "favouriteDayTimeCalmDownMethod int NOT NULL,"
                    "favouriteNightTimeCalmDownMethod int NOT NULL, preferredTemperature int NOT NULL,"
                    "CONSTRAINT BABY_ANALYSIS_pk PRIMARY KEY (id))")


# This method returns a BABY_ANALYSIS (table) object
def selectBabyAnalysisTableObject():
    my_objects = []
    with connectionObject:
        cur = connectionObject.cursor()
        cur.execute("SELECT * FROM BABY_ANALYSIS")
        rows = cur.fetchall()
        for row in rows:
            element1 = BABY_ANALYSIS(row["id"], row["babyName"], row["babyAge"], row["babyHeight"], row["babyWeight"],
                                     row["averageNumberOfWakeupsPerDay"], row["averageWakeupTimesPerDay"],
                                     row["averageNumberOfFeedsPerDay"], row["averageFeedTimesPerDay"],
                                     row["favouriteDayTimeCalmDownMethod"], row["favouriteNightTimeCalmDownMethod"],
                                     row["preferredTemperature"])
            my_objects.append(element1)
    return my_objects


def createTestTable():
    with connectionObject:
        cur = connectionObject.cursor()
        cur.execute("CREATE TABLE Test (ID int, firstname varchar(255), lastname varchar(255))")
        print("Create Successfull")


def insertTestTable():
    with connectionObject:
        cur = connectionObject.cursor()
        cur.execute("INSERT INTO Test (ID, firstname, lastname) VALUES(2, 'bob', 'jack')")
        print("Insert Successfull")

# Can insert into the Baby Analysis Table by passing all the requested values
def insertToBabyAnalysisTable(babyName, babyAge, babyHeight, babyWeight, averageNumberOfWakeupsPerDay,
                              averageWakeupTimesPerDay, averageNumberOfFeedsPerDay, averageFeedTimesPerDay,
                              favouriteDayTimeCalmDownMethod, favouriteNightTimeCalmDownMethod, preferredTemperature):
    with connectionObject:
        cur = connectionObject.cursor()
        query = "INSERT INTO BABY_ANALYSIS (babyName, babyAge, babyHeight, babyWeight, " \
                "averageNumberOfWakeupsPerDay, averageWakeupTimesPerDay, averageNumberOfFeedsPerDay, " \
                "averageFeedTimesPerDay, favouriteDayTimeCalmDownMethod, favouriteNightTimeCalmDownMethod, " \
                "preferredTemperature) VALUES('" + babyName + "', " + babyAge + ", " + babyHeight + ", " + babyWeight + \
                ", " + \
                averageNumberOfWakeupsPerDay + ", '" + averageWakeupTimesPerDay + "', " + averageNumberOfFeedsPerDay + \
                ", '" + averageFeedTimesPerDay + "', " + favouriteDayTimeCalmDownMethod + ", " + \
                favouriteNightTimeCalmDownMethod + ", " + preferredTemperature + ")"
        cur.execute(query)
        print("Insert Successfull")


def selectOneValue(tableName, element):
    with connectionObject:
        cur = connectionObject.cursor()
        cur.execute("SELECT * FROM {}".format(tableName))
        rows = cur.fetchall()
        for row in rows:
            print(row["id"], row[element])


def runVoidQuery(query):
    with connectionObject:
        cur = connectionObject.cursor()
        cur.execute(query)

# Main method here simply prints the database values
if __name__ == '__main__':
    # query = "ALTER TABLE BABY_ANALYSIS AUTO_INCREMENT=1"
    # runVoidQuery(query)
    # insertToBabyAnalysisTable()
    insertToBabyAnalysisTable("TESTBABY", "2", "12", "29", "2", "1,9", "5", "1,5,8", "2", "5", "26")

    # Testing:
    my_obj = selectBabyAnalysisTableObject()
    for obj in my_obj:
        print(obj.id)
        print(obj.babyName)
