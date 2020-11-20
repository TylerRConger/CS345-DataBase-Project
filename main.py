# Database python code
# CS 345 Final Project
# Written by Tyler Conger
# Due 11/19/2020

# imports
import sqlite3
from sqlite3 import Error
from random import randint
import math

# Global Values
FIRST_NAME = "FN"
LAST_NAME = "LN"
LEVEL = "LEVEL"
OFFENSES = "OFFENSES"
ID_NUM = "ID"

# create a function to open the database
# param: filePath - filePath of the database
# return: A connection to the database object
def connectToDB(filePath):

    # try and connect
    try:
        # connect with the provided file information
        con = sqlite3.connect(filePath)

    # print if we get an error
    except Error as e:
        print(e)

    return con

# function to close an opened database
# param: con - connection to the database
def closeTheDB(con):
    # if it was opened close it
    if con:
        con.close

# original creation for the database
# param: curs - cursor object of the database
def dataBaseInteraction(curs):
    curs.execute("""CREATE TABLE staff (
                    first text,
                    last text,
                    level text,
                    offenses integer,
                    id text
                    )""")
    curs.execute("""CREATE TABLE payscale (
                    position text,
                    pay float,
                    payType text,
                    bonus integer,
                    level integer
                    )""")

# Add a position to the payscale database
# param: con - connection to the database
# param: curs - cursor object of the database
# param: position - the name of the position
# param: pay - the amount the position gets paid, yearly
# param: payType - The way the position is paid, cash, check, credit
def addPosition(con, cursor, position, pay, payType, level):
    bonus = generateBonus(pay)
    cursor.execute("INSERT INTO payscale VALUES ('"+position+"', "+str(pay)+", '"+payType+"', " + str(bonus)+", "+str(level)+")")
    con.commit

# Generate a christmas bonus off the pay scale
# param: pay - The yearly pay of an position
# return: the christmas bonus calculation
def generateBonus(pay):
    return math.floor(pay * .03)

# Add a  staff member to the database
# param: con - connection to the database
# param: curs - cursor object of the database
# param: first - first name as a string of the staff member
# param: last - last name as a string of the staff member
def addAStaff(con, cursor, first, last):
    id = generateID(cursor)
    cursor.execute("INSERT INTO staff VALUES ('" + first + "', '"+last+"','0', '0', "+str(id)+")")
    con.commit()

# Get a staff member from the database
# param: curs - cursor object of the database
# param: id - staff member's id number
# return: a list of all staff with the given id, should only ever be one
def getAStaffByID(cursor,id):
    cursor.execute("SELECT * FROM staff WHERE id='"+str(id)+"'")
    return cursor.fetchall()

# Get a staff member from the database by last name (LN)
# param: curs - cursor object of the database
# param: last - last name as a string of the staff member
# return: a list of all staff with the given last name
def getAllStaffByLN(cursor,last):
    cursor.execute("SELECT * FROM staff WHERE last='"+last+"'")
    return cursor.fetchall()

# Get a staff member from the database by first name (FN)
# param: curs - cursor object of the database
# param: first - first name as a string of the staff member
# return: a list of all staff with the given first name
def getAllStaffByFN(cursor,first):
    cursor.execute("SELECT * FROM staff WHERE first='" + first + "'")
    return cursor.fetchall()

def getAllStaff(cursor):
    cursor.execute("SELECT * FROM staff")
    return cursor.fetchall()


def getAllPositions(cursor):
    cursor.execute("SELECT * FROM payscale")
    return cursor.fetchall()


# Remove a staff from the database by ID
# param: cursor - cursor object of the database
# param: id - staff member's id number
def removeAStaff(con, cursor, id):
    cursor.execute("DELETE FROM staff WHERE id='"+str(id)+"'")
    con.commit

# Generate an ID for a new staff member
# param: cursor - cursor object of the database
# return: a newly generated unique ID number
def generateID(cursor):
    # get all of the staff in the DB
    cursor.execute("SELECT * FROM staff")
    allStaff = cursor.fetchall()

    listOfIDs = []

    # get all the already taken IDs
    for i in range(len(allStaff)):
        listOfIDs.append(allStaff[i][4])

    # generate a new ID and make sure it doesn't already exsist
    ID = randint(1000, 9999)
    while ID in listOfIDs:
        ID = randint(1000, 9999)
    # return new ID
    return ID

# Get a staff's ID number by passing the first and last name
# param: con - connection to the database
# param: curs - cursor object of the database
# param: first - first name as a string of the staff member
# return: A given staff's id number, if it does not exsist or there are multiple staff under this name return -1
def getAStaffIDByName(cursor, first, last):
    firstNameSimilars = getAllStaffByFN(cursor, first)
    lastNameSimilars = getAllStaffByLN(cursor, last)
    commons = listIntersection(firstNameSimilars, lastNameSimilars)
    if len(commons) == 1:
        return commons[0][4]
    else:
        return -1

# A function to get the intersection of two lists
# param: list1 - The first list for intersection comparison
# param: list2 - The second list for intersection comparison
# return: A new list that contains only the intersection between the two lists
def listIntersection(list1, list2):
    return list(set(list1) & set(list2))

# Set the first name of someone with their ID used for updating data
# param: con - connection to the database
# param: curs - cursor object of the database
# param: newFirst - This staff's new first name
# param: ID - This staff's ID number
def setFN(con, cursor, newFirst, ID):
    cursor.execute("UPDATE staff SET first='"+newFirst+"' WHERE id="+ID)
    con.commit()

# Set the last name of someone with their ID used for updating data
# param: con - connection to the database
# param: curs - cursor object of the database
# param: newLast - This staff's new first name
# param: ID - This staff's ID number
def setLN(con, cursor, newLast, ID):
    cursor.execute("UPDATE staff SET last='"+newLast+"' WHERE id="+ID)
    con.commit()

# Set the level of someone with their ID used for updating data
# param: con - connection to the database
# param: curs - cursor object of the database
# param: newLevel - This staff's new level
# param: ID - This staff's ID number
def setLevel(con, cursor, newLevel, ID):
    cursor.execute("UPDATE staff SET level='"+str(newLevel)+"' WHERE id="+str(ID))
    con.commit()

# Set the number of offenses of someone with their ID used for updating data
# param: con - connection to the database
# param: curs - cursor object of the database
# param: newOffenses - This staff's new offenses total
# param: ID - This staff's ID number
def setOffenses(con, cursor, newOffenses, ID):
    cursor.execute("UPDATE staff SET offenses='"+str(newOffenses)+"' WHERE id="+str(ID))
    con.commit()

# increase an employee's level by one
# param: con - connection to the database
# param: curs - cursor object of the database
# param: ID - This staff's ID number
def increaseLevel (con, cursor, ID):
    employee = getAStaffByID(cursor, ID)
    currentLevel = int(employee[0][2])
    currentLevel += 1
    setLevel(con, cursor, currentLevel, ID)

# increase an employee's offenses by one
# param: con - connection to the database
# param: curs - cursor object of the database
# param: ID - This staff's ID number
def increaseOffenses (con, cursor, ID):
    employee = getAStaffByID(cursor, ID)
    currentOffenses = int(employee[0][3])
    currentOffenses += 1
    setOffenses(con, cursor, currentOffenses, ID)


def getPay(cursor, ID):
    level = getLevel(cursor, ID)
    allPositions = getAllPositions(cursor)

    for i in range(len(allPositions)):
        if int(level) == int(allPositions[i][4]):
            return int(allPositions[i][1])
    return -1


def getPayType(cursor, ID):
    level = getLevel(cursor, ID)
    allPositions = getAllPositions(cursor)

    for i in range(len(allPositions)):
        if int(level) == int(allPositions[i][4]):
            return int(allPositions[i][2])
    return "Not Valid"

def getChristmasBonus(cursor, ID):
    level = getLevel(cursor, ID)
    allPositions = getAllPositions(cursor)

    for i in range(len(allPositions)):
        if int(level) == int(allPositions[i][4]):
            return int(allPositions[i][3])
    return -1

def getLevel(cursor, ID):
    level = getAStaffByID(cursor, ID)[0][2]
    return level

def getOffenses(cursor, ID):
    offenses = getAStaffByID(cursor, ID)[0][3]
    return offenses


# main function
if __name__ == '__main__':
    # pass in our DB file and get a connection back
    conn = connectToDB(r"C:\Users\Tyler\PycharmProjects\databasesFinalProj\myDatabase.db")

    # get a cursor object based off the connection
    curs = conn.cursor()

    # create the initial table in the database
    # only do this interaction once, the first time
    dataBaseInteraction(curs)

    # add some staff members
    addAStaff(conn, curs, "Tyler", "Conger")
    addAStaff(conn, curs, "Lynne", "Conger")
    addAStaff(conn, curs, "Joe", "Fredrickson")
    addAStaff(conn, curs, "Bryan", "Beard")
    addAStaff(conn, curs, "Alex", "Guerino")
    addAStaff(conn, curs, "Beera", "Eka")
    addAStaff(conn, curs, "John", "Fauchs")
    addAStaff(conn, curs, "Jake", "Mann")
    addAStaff(conn, curs, "Ted", "Hart-Davis")

    # add some positions
    addPosition(conn, curs, "Intern", 10000, "cash", 0)
    addPosition(conn, curs, "Part-Time", 25000, "check", 1)
    addPosition(conn, curs, "Full-Time", 40000, "check", 2)
    addPosition(conn, curs, "Manager", 60000, "check", 3)
    addPosition(conn, curs, "CEO", 100000, "stock-options", 4)

    print("All staff ending with Eka" + str(getAllStaffByLN(curs,"Eka")))

    print("Changing Beera Eka's first and last names")

    setFN(conn, curs, "Joe", getAStaffIDByName(curs,"Beera", "Eka"))
    setLN(conn, curs, "Smith", getAStaffIDByName(curs,"Joe", "Eka"))

    print("All staff ending with Eka" + str(getAllStaffByLN(curs,"Eka")))

    print("Tyler Conger's info: " + str(getAStaffByID(curs, getAStaffIDByName(curs, "Tyler", "Conger"))))

    print("Increases offenses and level")

    increaseLevel(conn, curs, getAStaffIDByName(curs, "Tyler", "Conger"))
    increaseOffenses(conn, curs, getAStaffIDByName(curs, "Tyler", "Conger"))

    print("Tyler Conger's info: " + str(getAStaffByID(curs, getAStaffIDByName(curs, "Tyler", "Conger"))))

    print("Tyler Conger, gets paid: "+ str(getPay(curs,getAStaffIDByName(curs,"Tyler","Conger"))))





    # close the open database with a function
    closeTheDB(conn)

