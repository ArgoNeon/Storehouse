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
                    cell_type = 'res'
                if (icell.isRobot()):
                    cell_type = 'r'
                row.append(cell_type)
            file_writer.writerow(row)

def write_mails(mails_list):
    with open('mails.csv', mode="w") as mails_file:
        file_writer = csv.writer(mails_file, delimiter = ";", lineterminator="\r")
        for mail in mails_list:
            file_writer.writerow(str(mail))