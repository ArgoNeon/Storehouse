import random as rand
import numpy as np
import matplotlib.pyplot as plt
import math

import csv
import csv_reader
import distribution as dist

from heatmap import save_fig 
from field import Field
from robot import Robot
from coordinates import Coordinates
from points import InputPoint, Outputpoint
from mail import Mail
from cell import Cell

class Model():
    def __init__(self, field_file_name, data_folder, number_of_robots, number_of_mails, mail_distribution, robot_life_time, cell_life_time):
        file_name = data_folder + 'model_for_' + str(number_of_robots) + '_robots.txt'
        model_file = open(file_name, mode="w")
        self.model_writer = csv.writer(model_file, delimiter = " ", lineterminator="\r")

        field_data = csv_reader.read_field(field_file_name)

        self.start_number_of_mails      = number_of_mails
        self.number_of_mails            = number_of_mails
        self.number_of_delivered_mails  = 0

        self.__timer        = 0
        self.__event_timer  = 0

        self.field = Field(field_file_name, cell_life_time)

        self.mails_list  = []
        self.robots_list = []
        robots_data_list = []

        nrobots = number_of_robots

        for i in range(self.field.getMaxRow()):
            row = []
            for j in range(self.field.getMaxCol()):
                cell_type = self.field.getCellType(i, j)
                if ((cell_type == 'G') and (nrobots > 0 )):
                    nrobots = nrobots - 1
                    self.field.cellSetRobot(i, j)
                    robots_data_list.append(Coordinates(i, j))

        for i in range(number_of_robots):
            robot = Robot(i,    robots_data_list[i].getRow(), 
                                robots_data_list[i].getCol(), 
                                0, self.field.getNumberOfPheromones(), 
                                robot_life_time)
            self.robots_list.append(robot)

        self.input_points_list = []
        input_points_data_list = self.field.getInputPointsDataList()

        choose_input_points = rand.choices(range(self.field.getNumberOfInputPoints()), k = number_of_mails)
        
        mail_distribution_for_input_points = []

        for i in range(self.field.getNumberOfInputPoints()):
            mail_distribution_for_input_points.append(0)

        for i in range(len(choose_input_points)):
            mail_distribution_for_input_points[choose_input_points[i]] = mail_distribution_for_input_points[choose_input_points[i]] + 1

        for i in range(self.field.getNumberOfInputPoints()):
            input_point = InputPoint(i, input_points_data_list[i].getRow(),
                                        input_points_data_list[i].getCol(),
                                        self.field.getNumberOfOutputPoints(),
                                        mail_distribution_for_input_points[i],
                                        mail_distribution)
            self.field.setCellInputPoint(   input_points_data_list[i].getRow(),
                                            input_points_data_list[i].getCol(),
                                            input_point)
            self.input_points_list.append(input_point)

        self.output_points_list = []
        output_points_data_list = self.field.getOutputPointsDataList()

        for i in range(self.field.getNumberOfOutputPoints()):
            output_point = Outputpoint(i, output_points_data_list[i].getRow(),
                                          output_points_data_list[i].getCol())
            self.field.setCellOutputPoint(  output_points_data_list[i].getRow(),
                                            output_points_data_list[i].getCol(),
                                            output_point)                              
            self.output_points_list.append(output_point)

    def log_change_direction(self, robot, rotation):
        rotation_direction = 'R'

        if (rotation != 0):

            self.event()

            if (rotation == 1):
                rotation_direction = 'RCCW'

            if (rotation == 2):
                rotation_direction = 'RCW'
            
            row = [ str(self.getEvent()),
                    str(self.getTick()), 
                    str(robot.getID()), 
                    rotation_direction, 
                    str(robot.getCol()),
                    str(robot.getRow())]
            self.model_writer.writerow(row)

    def log_move(self, robot):
        move_forward = 'MF'

        self.event()

        row = [ str(self.getEvent()),
                str(self.getTick()),
                str(robot.getID()),
                move_forward,
                str(robot.getOldCol()),
                str(robot.getOldRow()),
                str(robot.getCol()),
                str(robot.getRow())]
        self.model_writer.writerow(row)

    def log_get_mail(self, robot, mail):
        load_mail = 'L'

        self.event()

        row = [ str(self.getEvent()),
                str(self.getTick()),
                str(robot.getID()),
                load_mail,
                str(robot.getCol()),
                str(robot.getRow()),
                str(mail.getMailDirection())]
        self.model_writer.writerow(row)

    def log_put_mail(self, robot, mail):
        unload_mail = 'UL'

        self.event()

        row = [ str(self.getEvent()),
                str(self.getTick()),
                str(robot.getID()),
                unload_mail,
                str(robot.getCol()),
                str(robot.getRow()),
                str(mail.getMailDirection())]
        self.model_writer.writerow(row)

    def log_wait(self, robot):
        wait = 'W'

        self.event()

        row = [ str(self.getEvent()),
                str(self.getTick()),
                str(robot.getID()),
                wait,
                str(robot.getCol()),
                str(robot.getRow())]
        self.model_writer.writerow(row)

    def getTick(self):
        return self.__timer

    def tick(self):
        self.__timer = self.__timer + 1

    def getEvent(self):
        return self.__event_timer

    def event(self):
        self.__event_timer = self.__event_timer + 1

    def robotCheckPheromonesAround(self, robot):
        robot_row, robot_col = robot.getCoordinates()
        current_pheromone = robot.getCurrentPheromone()

        robot.updateCurrentPheromonesAround(self.field.getCellPheromoneValue(robot_row - 1, robot_col, current_pheromone),
                                            self.field.getCellPheromoneValue(robot_row, robot_col + 1, current_pheromone),
                                            self.field.getCellPheromoneValue(robot_row + 1, robot_col, current_pheromone),
                                            self.field.getCellPheromoneValue(robot_row, robot_col - 1, current_pheromone)) 

    def robotCheckCellTypesAround(self, robot):
        robot_row, robot_col = robot.getCoordinates()
        
        robot.updateCellTypesAround(self.field.getCellType(robot_row - 1, robot_col),
                                    self.field.getCellType(robot_row, robot_col + 1),
                                    self.field.getCellType(robot_row + 1, robot_col),
                                    self.field.getCellType(robot_row, robot_col - 1))

    def robotChooseDirection(self, robot):
        robot_row, robot_col = robot.getCoordinates()
        robot_direction = robot.getDirection()
        current_pheromone = robot.getCurrentPheromone()
        opposite_robot_direction  = (robot_direction + 2) % 4
        opposite_direction_attraction = 0.1
        current_direction_attraction = 1.0

        if (opposite_robot_direction == 0):
            pheromone_value = self.field.getCellPheromoneValue(robot_row - 1, robot_col, current_pheromone)
            robot.updateCurrentPheromoneAround(0, opposite_direction_attraction * pheromone_value)
        if (opposite_robot_direction == 1):
            pheromone_value = self.field.getCellPheromoneValue(robot_row, robot_col + 1, current_pheromone)
            robot.updateCurrentPheromoneAround(1, opposite_direction_attraction * pheromone_value)
        if (opposite_robot_direction == 2):
            pheromone_value = self.field.getCellPheromoneValue(robot_row + 1, robot_col, current_pheromone)
            robot.updateCurrentPheromoneAround(2, opposite_direction_attraction * pheromone_value)
        if (opposite_robot_direction == 3):
            pheromone_value = self.field.getCellPheromoneValue(robot_row, robot_col - 1, current_pheromone)
            robot.updateCurrentPheromoneAround(3, opposite_direction_attraction * pheromone_value)

        if (robot_direction == 0):
            pheromone_value = self.field.getCellPheromoneValue(robot_row - 1, robot_col, current_pheromone)
            robot.updateCurrentPheromoneAround(0, current_direction_attraction * pheromone_value)
        if (robot_direction == 1):
            pheromone_value = self.field.getCellPheromoneValue(robot_row, robot_col + 1, current_pheromone)
            robot.updateCurrentPheromoneAround(1, current_direction_attraction * pheromone_value)
        if (robot_direction == 2):
            pheromone_value = self.field.getCellPheromoneValue(robot_row + 1, robot_col, current_pheromone)
            robot.updateCurrentPheromoneAround(2, current_direction_attraction * pheromone_value)
        if (robot_direction == 3):
            pheromone_value = self.field.getCellPheromoneValue(robot_row, robot_col - 1, current_pheromone)
            robot.updateCurrentPheromoneAround(3, current_direction_attraction * pheromone_value)

        if (self.field.cellIsReserved(robot_row - 1, robot_col)) or (self.field.cellIsRobot(robot_row - 1, robot_col)):
            robot.updateCurrentPheromoneAround(0, 0.0)
        if (self.field.cellIsReserved(robot_row, robot_col + 1)) or (self.field.cellIsRobot(robot_row, robot_col + 1)):
            robot.updateCurrentPheromoneAround(1, 0.0)
        if (self.field.cellIsReserved(robot_row + 1, robot_col)) or (self.field.cellIsRobot(robot_row + 1, robot_col)):
            robot.updateCurrentPheromoneAround(2, 0.0)
        if (self.field.cellIsReserved(robot_row, robot_col - 1)) or (self.field.cellIsRobot(robot_row, robot_col - 1)):
            robot.updateCurrentPheromoneAround(3, 0.0)

        if (robot.sumCurrentPheromoneAround() == 0.0):
            robot.startWait()
            robot_row, robot_col = robot.getCoordinates()
            self.log_wait(robot)

            return robot_direction, robot_row, robot_col
        
        robot.stopWait()

        new_direction, new_row, new_col = robot.chooseDirection()
        robot.setNewDirection(new_direction)
        robot.setNewCoordinates(new_row, new_col)

        return new_direction, new_row, new_col

    def robotChangeDirection(self, robot):
        rotation = 0

        robot_direction = robot.getDirection()
        new_direction = robot.getNewDirection()

        while (robot_direction != new_direction):
            rotation = robot.changeDirection()
            robot_direction = robot.getDirection()
            self.log_change_direction(robot, rotation)
        
        return rotation

    def robotAddPheromone(self, robot):
        row, col                    = robot.getCoordinates()
        for i in range(robot.getNumberOfPheromone()):
            ipheromone_value = robot.getPheromoneValue(i)
            self.field.cellAddPheromone(row, col, i, ipheromone_value)

    def robotMove(self, robot):
        old_row, old_col = robot.getCoordinates()
        new_row, new_col = robot.getNewCoordinates()
        self.field.cellSetReserved(new_row, new_col)
        self.robotAddPheromone(robot)
        robot.stopHold()
        current_row, current_col = robot.Move()
        robot.startHold()
        self.field.cellSetRobot(current_row, current_col)
        self.field.cellRemoveRobot(old_row, old_col)
        self.field.cellRemoveReserved(new_row, new_col)

        self.log_move(robot) 

        return current_row, current_col

    def run(self):
        while (self.number_of_delivered_mails != self.start_number_of_mails):
            self.tick()

            self.field.updateCellsPheromones()

            for irobot in self.robots_list:
                irobot_row, irobot_col = irobot.getCoordinates()
                irobot_direction = irobot.getDirection()
                irobot.updatePheromoneList()

                self.robotCheckCellTypesAround(irobot)
                self.robotCheckPheromonesAround(irobot) 
                
                ipoint_type = self.field.getCellType(irobot_row, irobot_col) 
                ipoint_direction = self.field.getCellPointDirection(irobot_row, irobot_col)

                if (ipoint_type == 'G'):
                    new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                    rotation = self.robotChangeDirection(irobot)
                    current_row, current_col = irobot.getCoordinates()
      
                    if ((new_row != current_row) or (new_col != current_col)):
                        new_row, new_col = self.robotMove(irobot)      
                
                elif (ipoint_type == 'T'):
                    if (irobot_direction != ipoint_direction):
                        irobot.setNewDirection(ipoint_direction)
                        rotation = self.robotChangeDirection(irobot)

                    irobot.changePheromoneListForInputPoint()
                    if (not irobot.isMail()):
                        mail = self.field.giveCellMailForInputPoint(irobot_row, irobot_col)

                        if (mail == None):
                            new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                            rotation = self.robotChangeDirection(irobot)
                            current_row, current_col = irobot.getCoordinates()
                            
                            if ((new_row != current_row) or (new_col != current_col)):
                                new_row, new_col = self.robotMove(irobot)
                        else:
                            self.field.newCellMailForInputPoint(irobot_row, irobot_col)
                            irobot.receiveMail(mail)
                            self.mails_list.append(mail.getMailDirection())
                            self.number_of_mails = self.number_of_mails - 1
                            self.log_get_mail(irobot, mail)
                    else:
                        new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                        rotation = self.robotChangeDirection(irobot)
                        current_row, current_col = irobot.getCoordinates()

                        if ((new_row != current_row) or (new_col != current_col)):
                            new_row, new_col = self.robotMove(irobot)

                elif (ipoint_type == 'Y'):
                    ipoint_mail_direction = self.field.getCellMailDirectionForOutputPoint(irobot_row, irobot_col)
                    irobot.changePheromoneListForOutputPoint(ipoint_mail_direction)
                    if (irobot.isMail() and (irobot.getMailDirection() == ipoint_mail_direction)):
                        if (irobot_direction != ipoint_direction):
                            irobot.setNewDirection(ipoint_direction)
                            rotation = self.robotChangeDirection(irobot)

                        mail = irobot.putMail()
                        self.number_of_delivered_mails = self.number_of_delivered_mails + 1
                        self.log_put_mail(irobot, mail)   
                        self.field.receiveCellMailForOutputPoint(irobot_row, irobot_col, mail)
                    else:
                        new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                        rotation = self.robotChangeDirection(irobot)
                        current_row, current_col = irobot.getCoordinates()
                        
                        if ((new_row != current_row) or (new_col != current_col)):
                            new_row, new_col = self.robotMove(irobot)

        return self.getTick(), len(self.robots_list), self.number_of_delivered_mails, self.field