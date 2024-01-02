import logging as log
import random as rand
import matplotlib.pyplot as plt
import math

import csv
import csv_reader
import distribution as dist

from field import Field
from robot import Robot
from points import InputPoint, Outputpoint
from mail import Mail

class Model():
    def __init__(self, field_file_name, number_of_mails, mail_distribution, robot_life_time, cell_life_time):
        model_file = open('model.csv', mode="w")
        self.model_writer = csv.writer(model_file, delimiter = ";", lineterminator="\r")

        field_data = csv_reader.read_field(field_file_name)

        self.start_number_of_mails      = number_of_mails
        self.number_of_mails            = number_of_mails
        self.number_of_delivered_mails  = 0

        self.__timer        = 0
        self.__event_timer  = 0

        self.field = Field(field_file_name, cell_life_time)

        self.mails_list  = []
        self.robots_list = []
        robots_data_list = self.field.getRobotsDataList()

        for i in range(self.field.getNumberOfRobots()):
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

    def log_change_direction(self, robot):
        row = [ str(self.getEvent()),
                str(self.getTick()), 
                str(robot.getID()), 
                str(0), 
                str(robot.getRow()), 
                str(robot.getCol())]
        self.model_writer.writerow(row)

    def log_move(self, robot):
        row = [ str(self.getEvent()),
                str(self.getTick()),
                str(robot.getID()),
                str(1),
                str(robot.getRow()),
                str(robot.getCol())]
        self.model_writer.writerow(row)

    def log_get_mail(self, robot, mail):
        row = [ str(self.getEvent()),
                str(self.getTick()),
                str(robot.getID()),
                str(2),
                str(robot.getRow()),
                str(robot.getCol()),
                str(mail.getMailDirection())]
        self.model_writer.writerow(row)

    def log_put_mail(self, robot, mail):
        row = [ str(self.getEvent()),
                str(self.getTick()),
                str(robot.getID()),
                str(3),
                str(robot.getRow()),
                str(robot.getCol()),
                str(mail.getMailDirection())]
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

        if (opposite_robot_direction == 0):
            pheromone_value = self.field.getCellPheromoneValue(robot_row - 1, robot_col, current_pheromone)
            robot.updateCurrentPheromoneAround(0, 0.01 * pheromone_value)
        if (opposite_robot_direction == 1):
            pheromone_value = self.field.getCellPheromoneValue(robot_row, robot_col + 1, current_pheromone)
            robot.updateCurrentPheromoneAround(1, 0.01 * pheromone_value)
        if (opposite_robot_direction == 2):
            pheromone_value = self.field.getCellPheromoneValue(robot_row + 1, robot_col, current_pheromone)
            robot.updateCurrentPheromoneAround(2, 0.01 * pheromone_value)
        if (opposite_robot_direction == 3):
            pheromone_value = self.field.getCellPheromoneValue(robot_row, robot_col - 1, current_pheromone)
            robot.updateCurrentPheromoneAround(3, 0.01 * pheromone_value)

        if (self.field.cellIsReserved(robot_row - 1, robot_col)) or (self.field.cellIsRobot(robot_row - 1, robot_col)):
            robot.updateCurrentPheromoneAround(0, 0.0)
        if (self.field.cellIsReserved(robot_row, robot_col + 1)) or (self.field.cellIsRobot(robot_row, robot_col + 1)):
            robot.updateCurrentPheromoneAround(1, 0.0)
        if (self.field.cellIsReserved(robot_row + 1, robot_col)) or (self.field.cellIsRobot(robot_row + 1, robot_col)):
            robot.updateCurrentPheromoneAround(2, 0.0)
        if (self.field.cellIsReserved(robot_row, robot_col - 1)) or (self.field.cellIsRobot(robot_row, robot_col - 1)):
            robot.updateCurrentPheromoneAround(3, 0.0)

        if (robot.sumCurrentPheromoneAround() == 0.0):
            robot_row, robot_col = robot.getCoordinates()
            robot.startWait()

            return robot_direction, robot_row, robot_col
        else:
            robot.stopWait()
        
        new_direction, new_row, new_col = robot.chooseDirection()
        robot.setNewDirection(new_direction)
        robot.setNewCoordinates(new_row, new_col)
        self.field.cellSetReserved(new_row, new_col)

        if (robot.checkRotate()):
            robot.startRotate()
            robot.stopHold()
        
        return new_direction, new_row, new_col

    def robotAddPheromone(self, robot):
        row, col = robot.getCoordinates()
        current_pheromone = robot.getCurrentPheromone()
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

        return current_row, current_col

    def run(self):
        while (self.number_of_delivered_mails != self.start_number_of_mails):
            self.tick()
            self.field.updateCellsPheromones()

            for irobot in self.robots_list:
                irobot_row, irobot_col = irobot.getCoordinates()
                irobot_direction = irobot.getDirection()
                irobot.updatePheromoneList()
                irobot.updateCurrentPheromon()

                self.robotCheckCellTypesAround(irobot)
                self.robotCheckPheromonesAround(irobot) 
                
                ipoint_type = self.field.getCellType(irobot_row, irobot_col) 
                ipoint_direction = self.field.getCellPointDirection(irobot_row, irobot_col)

                if (irobot.isDone()):
                    pass

                elif (irobot.isRotate()):
                    old_direction = irobot.getDirection()
                    new_direction = irobot.changeDirection()
                    self.event()
                    self.log_change_direction(irobot)
                elif (not irobot.isHold()):
                    new_row, new_col = self.robotMove(irobot)
                    self.event()
                    self.log_move(irobot)
                else:
                    if (ipoint_type == 'i'):
                        irobot.changePheromoneListForInputPoint()
                        if (not irobot.isMail()):
                            if (ipoint_direction != irobot_direction):
                                irobot.setNewDirection(ipoint_direction)
                                irobot.changeDirection()
                            else:
                                mail = self.field.giveCellMailForInputPoint(irobot_row, irobot_col)

                                if (mail == None):
                                    new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                                    current_direction = irobot.getDirection()
                                    current_row, current_col = irobot.getCoordinates()

                                    if (new_direction != current_direction):
                                        old_direction = irobot.getDirection()
                                        new_direction = irobot.changeDirection()
                                        self.event()
                                        self.log_change_direction(irobot)
                                    elif ((new_row != current_row) or (new_col != current_col)):
                                        new_row, new_col = self.robotMove(irobot)
                                        self.event()
                                        self.log_move(irobot)
                                    else:
                                        pass
                                else:
                                    self.field.newCellMailForInputPoint(irobot_row, irobot_col)
                                    irobot.receiveMail(mail)
                                    self.mails_list.append(mail.getMailDirection())
                                    self.number_of_mails = self.number_of_mails - 1
                                    self.event()
                                    self.log_get_mail(irobot, mail)
                        else:
                            new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                            current_direction = irobot.getDirection()
                            current_row, current_col = irobot.getCoordinates()

                            if (new_direction != current_direction):
                                old_direction = irobot.getDirection()
                                new_direction = irobot.changeDirection()
                                self.event()
                                self.log_change_direction(irobot)
                            elif ((new_row != current_row) or (new_col != current_col)):
                                new_row, new_col = self.robotMove(irobot)
                                self.event()
                                self.log_move(irobot)
                            else:
                                pass
                    elif (ipoint_type == 'o'):
                        ipoint_mail_direction = self.field.getCellMailDirectionForOutputPoint(irobot_row, irobot_col)
                        irobot.changePheromoneListForOutputPoint(ipoint_mail_direction)
                        if (irobot.isMail() and (irobot.getMailDirection() == ipoint_mail_direction)):
                            if (ipoint_direction != irobot_direction):
                                irobot.setNewDirection(ipoint_direction)
                                old_direction = irobot.getDirection()
                                new_direction = irobot.changeDirection()
                                self.event()
                                self.log_change_direction(irobot)  
                            else:
                                mail = irobot.putMail()
                                self.number_of_delivered_mails = self.number_of_delivered_mails + 1
                                self.event()
                                self.log_put_mail(irobot, mail)   
                                self.field.receiveCellMailForOutputPoint(irobot_row, irobot_col, mail)
                        else:
                            new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                            current_direction = irobot.getDirection()
                            current_row, current_col = irobot.getCoordinates()

                            if (new_direction != current_direction):
                                old_direction = irobot.getDirection()
                                new_direction = irobot.changeDirection()
                                self.event()
                                self.log_change_direction(irobot)
                            elif ((new_row != current_row) or (new_col != current_col)):
                                new_row, new_col = self.robotMove(irobot)
                                self.event()
                                self.log_move(irobot)
                            else:
                                pass
                    else:
                        new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                        current_direction = irobot.getDirection()
                        current_row, current_col = irobot.getCoordinates()

                        if (new_direction != current_direction):
                            old_direction = irobot.getDirection()
                            new_direction = irobot.changeDirection()
                            self.event()
                            self.log_change_direction(irobot)        
                        elif ((new_row != current_row) or (new_col != current_col)):
                            new_row, new_col = self.robotMove(irobot)
                            self.event()
                            self.log_move(irobot)        
                        else:
                            pass

        csv_reader.write_mails(self.mails_list)
        return self.getTick(), len(self.robots_list), self.number_of_delivered_mails                        
if __name__ == "__main__":
    number_of_it        = 1
    number_of_mails     = 100

    optimal_robot_life_time     = 7
    optimal_cell_life_time      = 2400

    tick_sum    = 0
    tick_list   = []
    metric_list = [] 

    mail_distribution = [85, 15, 5]

    for i in range(number_of_it):
        model = Model('field_b.csv', number_of_mails, mail_distribution, optimal_robot_life_time, optimal_cell_life_time)
        tick, number_of_robots, number_of_delivered_mails = model.run()
        tick_sum = tick_sum + tick
        tick_list.append(tick)
        metric = tick * number_of_robots / number_of_delivered_mails
        metric_list.append(metric)

    medium_tick = tick_sum / number_of_it
    metric_value = medium_tick * number_of_robots / number_of_delivered_mails

    for i in range(number_of_it):
        square_sum = (metric_list[i] - metric_value)**2

    dispertion = math.sqrt(square_sum / number_of_it)

    print('Medium number of ticks: ', medium_tick)
    print('Number of robots: ', number_of_robots)
    print('Number of delivered mails: ', number_of_delivered_mails)

    print('Metric value: ', metric_value)
    #print('Dispertion: ', dispertion)

    print('Robot life time: ', optimal_robot_life_time)
    print('Cell life time: ', optimal_cell_life_time)