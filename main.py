import logging as log
import random as rand
import matplotlib.pyplot as plt

import xlsx_reader
from field import Field
from robot import Robot
from points import InputPoint, Outputpoint
from mail import Mail

class Model():
    def __init__(self, field_file_name, number_of_mails, robot_life_time, cell_life_time):
        log.basicConfig(level=log.INFO, filename="model.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
        
        log.info('Start reading data from field file.')
        field_data = xlsx_reader.read_field(field_file_name)
        log.info('Field file has been read.')

        self.start_number_of_mails = number_of_mails
        self.number_of_mails = number_of_mails
        self.number_of_delivered_mails = 0
        self.__timer = 0
        self.field = Field(field_file_name, cell_life_time)

        self.robots_list = []
        robots_data_list = self.field.getRobotsDataList()

        for i in range(self.field.getNumberOfRobots()):
            robot = Robot(i, robots_data_list[i].getRow(), robots_data_list[i].getCol(), 0, self.field.getNumberOfPheromones(), robot_life_time)
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
                                        mail_distribution_for_input_points[i])
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

    def getTick(self):
        return self.__timer

    def tick(self):
        self.__timer = self.__timer + 1

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
            #print('Stuck')
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
            ipheromone_value = robot.getPheromoneValue(i) - 1.0
            self.field.cellAddPheromone(row, col, i, ipheromone_value)

    def robotMove(self, robot):
        old_row, old_col = robot.getCoordinates()
        new_row, new_col = robot.getNewCoordinates()
        self.field.cellSetReserved(new_row, new_col)
        robot.stopHold()
        current_row, current_col = robot.Move()
        robot.startHold()
        self.field.cellSetRobot(current_row, current_col)
        self.field.cellRemoveRobot(old_row, old_col)
        self.field.cellRemoveReserved(new_row, new_col)
        self.robotAddPheromone(robot)

        return current_row, current_col

    def run(self):
        while (self.number_of_delivered_mails != self.start_number_of_mails):
            self.tick()
            log.info('Tick: ' + str(self.getTick()) + ' Number of mails: ' + str(self.number_of_mails) + ' Number of delivered mails: ' + str(self.number_of_delivered_mails))
            self.field.updateCellsPheromones()

            for irobot in self.robots_list:
                irobot_row, irobot_col = irobot.getCoordinates()
                irobot_direction = irobot.getDirection()
                irobot.updatePheromoneList()
                irobot.updateCurrentPheromon()

                self.robotCheckCellTypesAround(irobot)
                self.robotCheckPheromonesAround(irobot) 

                #print(irobot.getCurrentPheromoneAround())
                
                ipoint_type = self.field.getCellType(irobot_row, irobot_col) 
                ipoint_direction = self.field.getCellPointDirection(irobot_row, irobot_col)
                ipoint_mail_direction = self.field.getCellMailDirection(irobot_row, irobot_col)

                if (irobot.isDone()):
                    pass

                elif (irobot.isRotate()):
                    old_direction = irobot.getDirection()
                    new_direction = irobot.changeDirection()
                    log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col change direction from ' + str(old_direction) + ' to ' + str(new_direction))

                elif (not irobot.isHold()):
                    new_row, new_col = self.robotMove(irobot)
                    log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col move to ' + str(new_row) + ' row,' + str(new_col) + ' col')
                else:
                    if (ipoint_type == 'i'):
                        #print('Input point', irobot.getID())
                        if (not irobot.isMail()):
                            if (ipoint_direction != irobot_direction):
                                irobot.setNewDirection(ipoint_direction)
                                irobot.changeDirection()
                            else:
                                mail = self.field.giveCellMailForInputPoint(irobot_row, irobot_col)
                                #print("Mail: ", mail)

                                if (mail == None):
                                    #irobot.wellDone()
                                    #elf.field.cellRemoveRobot(irobot_row, irobot_col)
                                    new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                                    log.info('Robot on ' + str(irobot_row) +  ' row,' + str(irobot_col) + ' col choose new direction ' + str(irobot.getNewDirection()) + ' from direction ' + str(irobot.getDirection()))

                                    current_direction = irobot.getDirection()
                                    current_row, current_col = irobot.getCoordinates()

                                    if (new_direction != current_direction):
                                        old_direction = irobot.getDirection()
                                        new_direction = irobot.changeDirection()
                                        log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col change direction from ' + str(old_direction) + ' to ' + str(new_direction))
                                    elif ((new_row != current_row) or (new_col != current_col)):
                                        new_row, new_col = self.robotMove(irobot)
                                        log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col move to ' + str(new_row) + ' row,' + str(new_col) + ' col')
                                    else:
                                        pass
                                else:
                                    self.field.newCellMailForInputPoint(irobot_row, irobot_col)
                                    irobot.receiveMail(mail)
                                    self.number_of_mails = self.number_of_mails - 1
                                    log.info('Robot on ' + str(irobot_row) +  ' row,' + str(irobot_col) + ' get mail to ' + str(mail.getMailDirection()) + ' output point from input point')
                        else:
                            new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                            #xlsx_reader.write_field('current_field.xlsx', model.field.getCellsList())
                            log.info('Robot on ' + str(irobot_row) +  ' row,' + str(irobot_col) + ' col choose new direction ' + str(irobot.getNewDirection()) + ' from direction ' + str(irobot.getDirection()))

                            current_direction = irobot.getDirection()
                            current_row, current_col = irobot.getCoordinates()

                            if (new_direction != current_direction):
                                old_direction = irobot.getDirection()
                                new_direction = irobot.changeDirection()
                                log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col change direction from ' + str(old_direction) + ' to ' + str(new_direction))
                            elif ((new_row != current_row) or (new_col != current_col)):
                                new_row, new_col = self.robotMove(irobot)
                                log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col move to ' + str(new_row) + ' row,' + str(new_col) + ' col')
                            else:
                                pass
                    elif (ipoint_type == 'o'):
                        #print('Output point', irobot.getID())
                        if (irobot.isMail() and (irobot.getMailDirection() == self.field.getCellMailDirectionForOutputPoint(irobot_row, irobot_col))):
                            if (ipoint_direction != irobot_direction):
                                irobot.setNewDirection(ipoint_direction)
                                old_direction = irobot.getDirection()
                                new_direction = irobot.changeDirection()
                                log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col change direction from ' + str(old_direction) + ' to ' + str(new_direction))
                            else:
                                mail = irobot.putMail()
                                self.number_of_delivered_mails = self.number_of_delivered_mails + 1
                                log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' put mail to ' + str(mail.getMailDirection()) + ' output point')
                                self.field.receiveCellMailForOutputPoint(irobot_row, irobot_col, mail)
                        else:
                            new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                            #xlsx_reader.write_field('current_field.xlsx', model.field.getCellsList())
                            log.info('Robot on ' + str(irobot_row) +  ' row,' + str(irobot_col) + ' col choose new direction ' + str(irobot.getNewDirection()) + ' from direction ' + str(irobot.getDirection()))

                            current_direction = irobot.getDirection()
                            current_row, current_col = irobot.getCoordinates()

                            if (new_direction != current_direction):
                                old_direction = irobot.getDirection()
                                new_direction = irobot.changeDirection()
                                log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col change direction from ' + str(old_direction) + ' to ' + str(new_direction))
                            elif ((new_row != current_row) or (new_col != current_col)):
                                new_row, new_col = self.robotMove(irobot)
                                log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col move to ' + str(new_row) + ' row,' + str(new_col) + ' col')
                            else:
                                pass
                    else:
                        new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                        #xlsx_reader.write_field('current_field.xlsx', model.field.getCellsList())
                        log.info('Robot on ' + str(irobot_row) +  ' row,' + str(irobot_col) + ' col choose new direction ' + str(irobot.getNewDirection()) + ' from direction ' + str(irobot.getDirection()))

                        current_direction = irobot.getDirection()
                        current_row, current_col = irobot.getCoordinates()

                        if (new_direction != current_direction):
                            old_direction = irobot.getDirection()
                            new_direction = irobot.changeDirection()
                            log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col change direction from ' + str(old_direction) + ' to ' + str(new_direction))
                        elif ((new_row != current_row) or (new_col != current_col)):
                            new_row, new_col = self.robotMove(irobot)
                            log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col move to ' + str(new_row) + ' row,' + str(new_col) + ' col')
                        else:
                            pass

        return self.getTick()                        
if __name__ == "__main__":
    '''it = 5
    number_of_mails = 100
    medium_robot_life = 10
    max_robot_life_time = 20
    medium_cell_life = 500
    max_cell_life_time = 1000

    x_robot = []
    y_robot = []

    x_cell = []
    y_cell = []

    for i in range(100, max_cell_life_time, 150):
        x_cell.append(i)
        summ = 0
        for icount in range(it):
            model = Model('field.xlsx', number_of_mails, medium_robot_life, i)
            tick = model.run()
            summ = summ + tick
        summ = summ / it
        y_cell.append(summ)

    for i in range(1, max_robot_life_time, 4):
        x_robot.append(i)
        summ = 0
        for icount in range(it):
            model = Model('field.xlsx', number_of_mails, i, medium_cell_life)
            tick = model.run()
            summ = summ + tick
        summ = summ / it
        y_robot.append(summ) 

    plt.figure(figsize=[16, 9])
    plt.plot(x_cell, y_cell, color="green")
    plt.show()

    plt.figure(figsize=[16, 9])
    plt.plot(x_robot, y_robot, color="green")
    plt.show()'''
    number_of_mails = 100
    optimal_robot_life_time = 5
    optimal_cell_life_time = 300
    model = Model('field.xlsx', number_of_mails, optimal_robot_life_time, optimal_cell_life_time)
    tick = model.run()
    xlsx_reader.write_field('current_field.xlsx', model.field.getCellsList())
    print('Number of ticks: ', tick)
    print('Number of mails: ', number_of_mails)
    print('Robot life time: ', optimal_robot_life_time)
    print('Cell life time: ', optimal_cell_life_time)