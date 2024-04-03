from model import Model
import math
import sys

if __name__ == "__main__":
    list_number_of_robots = []

    for param in sys.argv:
        if (param.isdigit()):
            if (int(param) > 0):
                list_number_of_robots.append(int(param))

    number_of_mails     = 10000

    optimal_robot_life_time     = 6.0
    optimal_cell_life_time      = 800

    tick_sum    = 0
    tick_list   = []
    metric_list = [] 

    mail_distribution_1 = [33]
    mail_distribution_3_a = [33, 33, 33]
    mail_distribution_3_b = [85, 10, 5]

    for number_of_robots in list_number_of_robots:
        model = Model('field/field_b.csv', 'data/', number_of_robots, number_of_mails, mail_distribution_3_a, optimal_robot_life_time, optimal_cell_life_time)
        tick, number_of_robots, number_of_delivered_mails, field = model.run()

        print('Number of ticks: ', tick)
        print('Number of robots: ', number_of_robots)
        print('Number of delivered mails: ', number_of_delivered_mails)

    print('Robot life time: ', optimal_robot_life_time)
    print('Cell life time: ', optimal_cell_life_time)