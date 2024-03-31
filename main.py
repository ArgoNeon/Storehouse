from model import Model
import math

if __name__ == "__main__":
    number_of_it        = 1
    number_of_robots  = 30
    number_of_mails     = 10000

    optimal_robot_life_time     = 6.0
    optimal_cell_life_time      = 800

    tick_sum    = 0
    tick_list   = []
    metric_list = [] 

    mail_distribution_1 = [33]
    mail_distribution_3_a = [33, 33, 33]
    mail_distribution_3_b = [85, 10, 5]

    for i in range(number_of_it):
        model = Model('field/field_b.csv', number_of_robots, number_of_mails, mail_distribution_3_a, optimal_robot_life_time, optimal_cell_life_time)
        tick, number_of_robots, number_of_delivered_mails, field = model.run()
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