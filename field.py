import csv_reader
from coordinates import Coordinates
from cell import Cell

class Field():
    def __init__(self, field_file_name, life_time):
        self.__cell_life_time = life_time
        
        field = csv_reader.read_field(field_file_name)

        max_row = len(field)
        max_col = 0

        for irow in field:
            if (len(irow) > max_col):
                max_col = len(irow)

        self.__min_row = 0
        self.__min_col = 0
        self.__max_row = max_row - 1
        self.__max_col = max_col - 1

        self.__cells_list = []

        n_robots        = 0
        n_input_points  = 0
        n_output_points = 0

        self.__input_points_data_list   = []
        self.__output_points_data_list  = []

        for i in range(max_row):
            for j in range(max_col):
                if (field[i][j] == 'T'):
                    n_input_points = n_input_points + 1
                    self.__input_points_data_list.append(Coordinates(i, j))

                if (field[i][j] == 'Y'):
                    n_output_points = n_output_points + 1
                    self.__output_points_data_list.append(Coordinates(i, j))

        self.__number_of_robots         = n_robots
        self.__number_of_input_points   = n_input_points
        self.__number_of_output_points  = n_output_points
        self.__number_of_pheromones     = n_output_points + 1

        for i in range(max_row):
            row = []
            for j in range(max_col):
                cell = Cell(i, j, field[i][j], self.__number_of_pheromones, self.__cell_life_time)
                row.append(cell)
            self.__cells_list.append(row)

    def getNumberOfPheromones(self):
        return self.__number_of_pheromones

    def getMaxRow(self):
        return self.__max_row

    def getMaxCol(self):
        return self.__max_col

    def getNumberOfRobots(self):
        return self.__number_of_robots

    def getNumberOfInputPoints(self):
        return self.__number_of_input_points

    def getNumberOfOutputPoints(self):
        return self.__number_of_output_points

    def getRobotsDataList(self):
        return self.__robots_data_list

    def getInputPointsDataList(self):
        return self.__input_points_data_list

    def getOutputPointsDataList(self):
        return self.__output_points_data_list

    def getCellsList(self):
        return self.__cells_list  

    def cellIsReserved(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].isReserved()

    def cellIsRobot(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].isRobot()

    def cellSetReserved(self, cell_row, cell_col):
        self.__cells_list[cell_row][cell_col].setReserved()

    def cellSetRobot(self, cell_row, cell_col):
        self.__cells_list[cell_row][cell_col].setRobot()

    def cellRemoveReserved(self, cell_row, cell_col):
        self.__cells_list[cell_row][cell_col].removeReserved()

    def cellRemoveRobot(self, cell_row, cell_col):
        self.__cells_list[cell_row][cell_col].removeRobot()

    def updateCellsPheromones(self):
        for irow in self.__cells_list:
            for icell in irow:
                icell.updatePheromoneList()

    def getCellType(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getType()
            
    def changeCellType(self, cell_row, cell_col, cell_type):
        self.__cells_list[cell_row][cell_col].setType(cell_type)

    def cellAddPheromone(self, cell_row, cell_col, pheromone_id, pheromone_data):
        self.__cells_list[cell_row][cell_col].addPheromone(pheromone_id, pheromone_data)

    def getCellPheromoneList(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getPheromoneList()

    def getCellPheromoneValue(self, cell_row, cell_col, number_of_pheromone):
        return self.__cells_list[cell_row][cell_col].getPheromone(number_of_pheromone)

    def getCellPointDirection(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getPointDirection()

    def setCellMailDirection(self, cell_row, cell_col, mail_direction):
        self.__cells_list[cell_row][cell_col].setMailDirection(mail_direction)


    def giveCellMailForInputPoint(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].giveMailForInputPoint()

    def receiveCellMailForOutputPoint(self, cell_row, cell_col, mail):
        self.__cells_list[cell_row][cell_col].receiveMailForOutputPoint(mail)

    def setCellInputPoint(self, cell_row, cell_col, input_point):
        self.__cells_list[cell_row][cell_col].setInputPoint(input_point)

    def setCellOutputPoint(self, cell_row, cell_col, output_point):
        self.__cells_list[cell_row][cell_col].setOutputPoint(output_point)

    def getCellMailDirectionForOutputPoint(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getMailDirectionForOutputPoint()

    def getCellNumberOfReceivedMailsForOutputPoint(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getNumberOfReceivedMailsForOutputPoint()

    def getCellNumberOfMailsForInputPoint(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getNumberOfMailsForInputPoint()

    def newCellMailForInputPoint(self, cell_row, cell_col):
        self.__cells_list[cell_row][cell_col].newMailForInputPoint()

    def getCellOutputPointMailDirection(self, cell_row, cell_col):
        self.__cells_list[cell_row][cell_col].getOutputPointMailDirection()