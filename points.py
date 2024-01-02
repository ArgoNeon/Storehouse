import random as rand
from coordinates import Coordinates
from mail import Mail

class InputPoint():
    def __init__(self, point_id, row, col, number_of_output_points, number_of_mails):
        self.__id = point_id
        self.__coordinates = Coordinates(row, col)
        self.__current_mail = None
        self.__number_of_mails = number_of_mails
        self.__mail_directions = range(number_of_output_points)

        if (self.__number_of_mails > 0):
            mail_direction = rand.choices(self.__mail_directions, weights=[85, 15, 5])
            self.__current_mail = Mail(mail_direction[0])
        else:
            self.__current_mail = None

    def getID(self):
        return self.__id

    def getCoordinates(self):
        return self.__coordinates.getCoordinates()

    def getNumberOfMails(self):
        return self.__number_of_mails

    def giveMail(self):
        mail = self.__current_mail
        self.__current_mail = None
        self.__number_of_mails = self.__number_of_mails - 1
        return mail

    def newMail(self):
        if (self.__number_of_mails > 0):
            mail_direction = rand.choices(self.__mail_directions)
            self.__current_mail = Mail(mail_direction[0])
        else:
            self.__current_mail = None

class Outputpoint():
    def __init__(self, mail_direction, row, col):
        self.__coordinates = Coordinates(row, col)
        self.__mail_direction = mail_direction
        self.__number_of_received_mails = 0

    def getCoordinates(self):
        return self.__coordinates.getCoordinates()

    def getMailDirection(self):
        return self.__mail_direction

    def getNumberOfReceivedMails(self):
        return self.__number_of_received_mails

    def receiveMail(self, mail):
        if (mail != None):
            if (mail.getMailDirection() == self.__mail_direction):
                self.__number_of_received_mails = self.__number_of_received_mails + 1