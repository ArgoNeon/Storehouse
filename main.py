import logging as log

import xlsx_reader
from field import Field
from robot import Robot
from points import InputPoint, Outputpoint
from mail import Mail

class Model():
    def __init__(self, field_file_name, number_of_mails):
        log.basicConfig(level=log.INFO, filename="model.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
        
        log.info('Start reading data from field file.')
        field_data = xlsx_reader.read_field(field_file_name)
        log.info('Field file has been read.')

        self.start_number_of_mails = number_of_mails
        self.number_of_mails = number_of_mails
        self.number_of_delivered_mails = 0
        self.__timer = 0
        self.field = Field(field_file_name)

        self.robots_list = []
        robots_data_list = self.field.getRobotsDataList()

        for i in range(self.field.getNumberOfRobots()):
            robot = Robot(i, robots_data_list[i].getRow(), robots_data_list[i].getCol(), 0, self.field.getNumberOfPheromones())
            self.robots_list.append(robot)

        self.input_points_list = []
        input_points_data_list = self.field.getInputPointsDataList()

        for i in range(self.field.getNumberOfInputPoints()):
            input_point = InputPoint(i, input_points_data_list[i].getRow(),
                                        input_points_data_list[i].getCol(),
                                        self.field.getNumberOfOutputPoints(),
                                        number_of_mails)
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

        robot.updateCurrentPheromonesAround(self.field.getCellPheromone(robot_row - 1, robot_col, current_pheromone),
                                            self.field.getCellPheromone(robot_row, robot_col + 1, current_pheromone),
                                            self.field.getCellPheromone(robot_row + 1, robot_col, current_pheromone),
                                            self.field.getCellPheromone(robot_row, robot_col - 1, current_pheromone)) 

    def robotCheckCellTypesAround(self, robot):
        robot_row, robot_col = robot.getCoordinates()
        
        robot.updateCellTypesAround(self.field.getCellType(robot_row - 1, robot_col),
                                    self.field.getCellType(robot_row, robot_col + 1),
                                    self.field.getCellType(robot_row + 1, robot_col),
                                    self.field.getCellType(robot_row, robot_col - 1))

    def robotChooseDirection(self, robot):
        robot_row, robot_col = robot.getCoordinates()
        current_pheromone = robot.getCurrentPheromone()



        if (self.field.cellIsReserved(robot_row - 1, robot_col)) or (self.field.cellIsRobot(robot_row - 1, robot_col)):
            robot.updateCurrentPheromoneAround(0, 0.0)
        if (self.field.cellIsReserved(robot_row, robot_col + 1)) or (self.field.cellIsRobot(robot_row, robot_col + 1)):
            robot.updateCurrentPheromoneAround(1, 0.0)
        if (self.field.cellIsReserved(robot_row + 1, robot_col)) or (self.field.cellIsRobot(robot_row + 1, robot_col)):
            robot.updateCurrentPheromoneAround(2, 0.0)
        if (self.field.cellIsReserved(robot_row, robot_col - 1)) or (self.field.cellIsRobot(robot_row, robot_col - 1)):
            robot.updateCurrentPheromoneAround(3, 0.0)
        
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
        pheromone_value = robot.getPheromoneValue()
        #print('Add: ', current_pheromone, pheromone_value)
        self.field.cellAddPheromone(row, col, current_pheromone, pheromone_value)
        #print('Check: ', self.field.getCellPheromone(row, col, current_pheromone))

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
                        print('Input point', irobot.getID())
                        if (not irobot.isMail()):
                            if (ipoint_direction != irobot_direction):
                                irobot.setNewDirection(ipoint_direction)
                                irobot.changeDirection()
                            else:
                                mail = self.field.giveCellMailForInputPoint(irobot_row, irobot_col)
                                print("Mail: ", mail)

                                if (mail == None):
                                    irobot.wellDone()
                                    self.field.cellRemoveRobot(irobot_row, irobot_col)
                                else:
                                    self.field.newCellMailForInputPoint(irobot_row, irobot_col)
                                    irobot.setMail(mail)
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
                            else:
                                new_row, new_col = self.robotMove(irobot)
                                log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col move to ' + str(new_row) + ' row,' + str(new_col) + ' col')
                    elif (ipoint_type == 'o'):
                        print('Output point', irobot.getID())
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
                            else:
                                new_row, new_col = self.robotMove(irobot)
                                log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col move to ' + str(new_row) + ' row,' + str(new_col) + ' col')
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
                        else:
                            new_row, new_col = self.robotMove(irobot)
                            log.info('Robot on ' + str(irobot_row) + ' row,' + str(irobot_col) + ' col move to ' + str(new_row) + ' row,' + str(new_col) + ' col')

if __name__ == "__main__":
    model = Model('field.xlsx', 10)
    model.run()
    xlsx_reader.write_field('current_field.xlsx', model.field.getCellsList())