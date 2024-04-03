import csv
from cell import Cell

def read_field(field_file_name):
    with open(field_file_name, mode="r") as field_file:
        file_reader = csv.reader(field_file, delimiter = ";")

        field = []
        for irow in file_reader:
            row = []
            for icell in range(len(irow)):
                row.append(irow[icell])
            field.append(row)    
    return field

def write_field(field_file_name, field_data):
    with open(field_file_name, mode="w") as field_file:
        file_writer = csv.writer(field_file, delimiter = ";", lineterminator="\r")
        for irow in field_data:
            row = []
            for icell in irow:
                cell_type = icell.getType()
                if (icell.isReserved()):
                    cell_type = 'RES'
                if (icell.isRobot()):
                    cell_type = 'ROB'
                row.append(cell_type)
            file_writer.writerow(row)

def read_pheromone_map(pheromone_file_0, pheromone_file_1, field):
    pheromone_map_0 = open(pheromone_file_0, mode="w")
    file_writer_0 = csv.writer(pheromone_map_0, delimiter = ";", lineterminator="\r")
    pheromone_map_1 = open(pheromone_file_1, mode="w")
    file_writer_1 = csv.writer(pheromone_map_1, delimiter = ";", lineterminator="\r")
    count_row = 0

    for irow in field.getCellsList():
        row_0 = []
        row_1 = []
        
        count_col = 0
        for icell in irow:
            row = icell.getRow()
            col = icell.getCol()

            if (count_col != 0) and (count_col != 10):
                row_0.append(field.getCellPheromoneValue(row, col, 0))
                row_1.append(field.getCellPheromoneValue(row, col, 1))

            count_col = count_col + 1

        if (count_row != 0) and (count_row != 10):
            file_writer_0.writerow(row_0)
            file_writer_1.writerow(row_1)

        count_row = count_row + 1