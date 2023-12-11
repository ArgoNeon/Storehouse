import logging as log

import xlsx_reader
from field import Field
from robot import Robot
from points import InputPoint, Outputpoint

class Model():
    def __init__(self, field_file_name, number_of_mails):
        log.basicConfig(level=log.INFO, filename="model.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
        
        log.info('Start reading data from field file.')
        field_data = xlsx_reader.read_field(field_file_name)
        log.info('Field file has been read.')

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
            self.input_points_list.append(input_point)

        self.output_points_list = []
        output_points_data_list = self.field.getOutputPointsDataList()

        for i in range(self.field.getNumberOfOutputPoints()):
            output_point = Outputpoint(i, output_points_data_list[i].getRow(),
                                          output_points_data_list[i].getCol())
            self.output_points_list.append(output_point)

    def getTick(self):
        return self.__timer

    def tick(self):
        self.__timer = self.__timer + 1

    def robotSearchPheromone(self, robot):
        robot_row, robot_col = robot.getCoordinates()

        robot.updateCurrentPheromonesAround(self.field.getCellPheromone(robot_row - 1, robot_col, current_pheromone),
                                            self.field.getCellPheromone(robot_row, robot_col + 1, current_pheromone),
                                            self.field.getCellPheromone(robot_row + 1, robot_col, current_pheromone),
                                            self.field.getCellPheromone(robot_row, robot_col - 1, current_pheromone)) 

    def robotSearchOutputPoint(self, robot):
        robot_row, robot_col = robot.getCoordinates()

    def robotChooseDirection(self, robot):
        robot_row, robot_col = robot.getCoordinates()
        robot_direction = robot.getDirection()
        point_direction = self.field.getCellType(robot_row, robot_col)
        point_type = self.field.getCellType(robot_row, robot_col)

        if (point_type == 'o'):
            
            if (point_direction != robot_direction):
                robot.setNewDirection(self.field.getCellPointDirection(robot_row, robot_col))
                robot.changeDirection()
            else:
                robot.putMail()
                self.robotAddPheromone(robot)
        elif (point_type == 'i'):
            
        else:
            if (self.field.cellIsReserved(robot_row - 1, robot_col)) or (self.field.cellIsRobot(robot_row - 1, robot_col)):
                robot.updateCurrentPheromoneAround(0, 0.0)
            if (self.field.cellIsReserved(robot_row, robot_col + 1)) or (self.field.cellIsRobot(robot_row - 1, robot_col)):
                robot.updateCurrentPheromoneAround(1, 0.0)
            if (self.field.cellIsReserved(robot_row + 1, robot_col)) or (self.field.cellIsRobot(robot_row - 1, robot_col)):
                robot.updateCurrentPheromoneAround(2, 0.0)
            if (self.field.cellIsReserved(robot_row, robot_col - 1)) or (self.field.cellIsRobot(robot_row - 1, robot_col)):
                robot.updateCurrentPheromoneAround(3, 0.0)
        
            new_direction, new_row, new_col = robot.chooseDirection()
            field.cellSetReserved(new_row, new_col)
        
        return new_direction, new_row, new_col

    def robotAddPheromone(self, robot):
        row, col = robot.getCoordinates()
        pheromone_id = robot.getCurrentPheromone()
        current_pheromone = robot.getCurrentPheromone()
        pheromone_value = robot.getPheromoneValue()
        self.field.addPheromone(row, col, current_pheromone, pheromone_value)

    def robotMove(self, robot):
        if (robot.getNewDirection() == robot.getDirection()):
            old_row, old_col = robot.getCoordinates()
            new_row, new_col = robot.getNewCoordinates()
            self.field.cellSetReserved(new_row, new_col)
            robot.startProcess()
            robot.Move()
            robot.startHold()
            current_row, current_col = robot.getCoordinates()
            self.field.cellSetRobot(current_row, current_col)
            self.field.cellRemoveRobot(old_row, old_col)
            self.robotAddPheromone(robot)
        else:
            robot.changeDirection()

    def run(self):
        while (self.number_of_delivered_mails != self.number_of_mails):
            self.field.updateCellsPheromones()

            for irobot in self.robots_list:
                irobot.updatePheromoneList() 
                if (irobot.isRotate()):
                    irobot.changeDirection()
                elif (not irobot.isHold()):
                    self.robotMove(robot)
                else:
                    irobot.updateCurrentPheromon()
                    self.robotSearchPheromone(irobot)

                    new_direction, new_row, new_col = self.robotChooseDirection(irobot)
                    irobot.setNewDirection(new_direction)
                    irobot.setNewCoordinates(new_row, new_col)
                    current_direction = irobot.getDirection()
                    current_row, current_col = irobot.getCoordinates()

                    if (new_direction != current_direction):
                        irobot.changeDirection()
                    elif ((new_row != current_row) or (new_col != current_col)):
                        self.robotMove(robot) 

if __name__ == "__main__":
    model = Model('field.xlsx', 10)
    model.run()