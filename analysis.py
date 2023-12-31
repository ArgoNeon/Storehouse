import csv
import matplotlib.pyplot as plt

def save_mails(log_file_name, mail_file_name):
    log_file = open(log_file_name, mode="r")
    file_reader = csv.reader(log_file, delimiter = ";")
    
    mail_file = open(mail_file_name, mode="w")
    file_writer = csv.writer(mail_file, delimiter = ";", lineterminator="\r")

    for irow in file_reader:
        if (irow[3] == str(2)):
            file_writer.writerow(irow)
        if (irow[3] == str(3)):
            file_writer.writerow(irow)

def save_delivery_time(mail_file_name, delivery_time_file_name, number_of_robots):
    mail_file = open(mail_file_name, mode="r")
    file_reader = csv.reader(mail_file, delimiter = ";")

    delivery_time_file = open(delivery_time_file_name, mode="w")
    file_writer = csv.writer(delivery_time_file, delimiter = ";", lineterminator="\r")

    start_time  = []
    end_time    = []

    for i in range(number_of_robots):
        start_time.append([0, 0, 0])
        end_time.append([0, 0, 0])

    for irow in file_reader: 
        if (irow[3] == str(2)):
            mail_direction = int(irow[6])
            robot_id = int(irow[2])
            start_time[robot_id][mail_direction] = int(irow[1])
        if (irow[3] == str(3)):
            mail_direction = int(irow[6])
            robot_id = int(irow[2])
            end_time[robot_id][mail_direction] = int(irow[1])
            time = end_time[robot_id][mail_direction] - start_time[robot_id][mail_direction]
            row = []
            row.append(end_time[robot_id][mail_direction])
            row.append(mail_direction)
            row.append(robot_id)
            row.append(time)
            file_writer.writerow(row)

def create_graphic(delivery_time_file_name):
    plt.rc('xtick', labelsize=14) 
    plt.rc('ytick', labelsize=14)
    plt.rc('axes', labelsize=14)

    plt.figure(figsize=[16, 9])

    delivery_time_file = open(delivery_time_file_name, mode="r")
    file_reader = csv.reader(delivery_time_file, delimiter = ";")

    count                   = [0, 0, 0]
    sum_delivery_time       = [0, 0, 0]
    medium_delivery_time    = [[], [], []]
    time                    = [[], [], []]
    delivery_time           = [[], [], []]

    for irow in file_reader:
        count[int(irow[1])]             = count[int(irow[1])] + 1
        sum_delivery_time[int(irow[1])] = sum_delivery_time[int(irow[1])] + int(irow[3])

        medium_delivery_time[int(irow[1])].append(sum_delivery_time[int(irow[1])] / count[int(irow[1])])
        delivery_time[int(irow[1])].append(int(irow[3]))
        time[int(irow[1])].append(int(irow[0]))

    #print(count, medium_delivery_time)

    plt.plot(time[0], delivery_time[0], color='green')
    plt.plot(time[1], delivery_time[1], color='blue')
    plt.plot(time[2], delivery_time[2], color='red')
    plt.xlabel('t')
    plt.ylabel('T_del')

    plt.grid()
    plt.show()

    plt.figure(figsize=[16, 9])
    
    plt.plot(time[0], medium_delivery_time[0], color='green')
    plt.plot(time[1], medium_delivery_time[1], color='blue')
    plt.plot(time[2], medium_delivery_time[2], color='red')
    plt.xlabel('t')
    plt.ylabel('T_med')

    plt.grid()
    plt.show()

if __name__ == "__main__":
    number_of_robots = 8
    save_mails('model.csv', 'get_put.csv')
    save_delivery_time('get_put.csv', 'delivery_time.csv', number_of_robots)
    create_graphic('delivery_time.csv')