import xlsx_reader as rd
from coordinates import Coordinates
from cell import Cell

class Field():
    def __init__(self, field_file_name):
        field = rd.read_field(field_file_name)

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

        n_robots = 0
        n_input_points = 0
        n_output_points = 0

        self.__robots_data_list = []
        self.__input_points_data_list = []
        self.__output_points_data_list = []

        for i in range(max_row):
            for j in range(max_col):
                if (field[i][j] == 'r'):
                    n_robots = n_robots + 1
                    self.__robots_data_list.append(Coordinates(i, j))

                if (field[i][j] == 'i'):
                    n_input_points = n_input_points + 1
                    self.__input_points_data_list.append(Coordinates(i, j))

                if (field[i][j] == 'o'):
                    n_output_points = n_output_points + 1
                    self.__output_points_data_list.append(Coordinates(i, j))

        self.__number_of_robots = n_robots
        self.__number_of_input_points = n_input_points
        self.__number_of_output_points = n_output_points
        self.__number_of_pheromones = n_output_points + 1

        for i in range(max_row):
            row = []
            for j in range(max_col):
                cell = Cell(i, j, field[i][j], self.__number_of_pheromones)
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
        for icell in self.__cells_list:
            icell.updatePheromoneList()

    def getCellType(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getType()
            
    def changeCellType(self, cell_row, cell_col, cell_type):
        self.__cells_list[cell_row][cell_col].setType(cell_type)

    def cellAddPheromone(self, cell_row, cell_col, pheromone_id, pheromone_data):
        self.__cells_list[cell_row][cell_col].addPheromone(pheromone_id, pheromone_data)

    def getCellPheromoneList(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getPheromoneList()

    def getCellPheromone(self, cell_row, cell_col, number_of_pheromone):
        return self.__cells_list[cell_row][cell_col].getPheromone(number_of_pheromone)

    def getCellPointDirection(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getPointDirection()

    def getCellMailDirection(self, cell_row, cell_col):
        return self.__cells_list[cell_row][cell_col].getMailDirection()

    def setCellMailDirection(self, cell_row, cell_col, mail_direction):
        return self.__cells_list[cell_row][cell_col].setMailDirection(mail_direction)
