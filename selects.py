"""
This file releases 2.3 goal in the assignment: Implement select queries
"""
from datetime import datetime
from interface import *
db = Database('db.sqlite')


@intro
def select_3_1():
    """A customer claims she forgot her bag in a car and asks to help.
    She was using cars several times this day, but she believes the right
    car was red and its plate starts with “AN”. Find all possible cars
    that match the description."""
    return db.query('''SELECT carid FROM cars WHERE color="Red" and substr(plate, 1, 2)="AN"''')


@intro
def select_3_2():
    """
    Company management wants to get a statistics on the efficiency of
    charging stations utilization. Given a date, compute how many sockets
    were occupied each hour.
    """
    date = MyDate(2018, 11, 8)
    occupied = db.query('''SELECT usage_time, charging_time_amount FROM cars_charged 
                           WHERE date(usage_time)="{}"'''.format(str(date)))
    hours = dict()
    for hour in range(24):
        hours_occupied = '{:02}h-{:02}h'.format(hour, hour+1)
        hours[hours_occupied] = 0
        for socket in occupied:
            duration = socket[1]
            h = int(socket[0][11:13])
            m = int(socket[0][14:16])
            if (h == hour) or (h == hour - 1 and m + duration >= 60):
                hours[hours_occupied] += 1

    return hours


@intro
def select_3_3():
    """
    Company management considers using price increasing coefficients.
    They need to gather statistics for one week on how many cars are busy
    (% to the total amount of taxis) during the morning (7AM - 10 AM),
    afternoon (12AM - 2PM) and evening (5PM - 7PM) time.
    """
    pass


@intro
def select_3_4():
    """
    A customer claims that he was charged twice for the trip, but he
    can’t say exactly what day it happened (he deleted notification from
    his phone and he is too lazy to ask the bank), so you need to check all
    his payments for the last month to be be sure that nothing was doubled.
    """
    # cid = 7  # consider customer
    #     # pays_of_user = db.query('''SELECT paytime, amount FROM payments WHERE cid={}'''.format(cid))
    #     # for i, pay1 in enumerate(pays_of_user):
    #     #     for j, pay2 in enumerate(pays_of_user):
    #     #         if i != j and pay1[0] == pay1[0] and pay2[0] == pay2[0]:
    #     #             return 'User paid twice at ' + pay1[0]
    #     # return 'User paid only once'


@intro
def select_3_5():
    """
    The department of development has requested the following statistics:
    - Average distance a car has to travel per day to customer’s order location
    - Average trip duration
    Given a date as an input, compute the statistics above.
    """
    pass


@intro
def select_3_6():
    """
    In order to accommodate traveling demand, the company decided to
    distribute cars according to demand locations. Your task is to
    compute top-3 most popular pick-up locations and travel destination
    for each time of day: morning (7am-10am), afternoon (12am-2pm) and evening (5pm-7pm).
    """
    pass


@intro
def select_3_7():
    """
    Despite the wise management, the company is going through hard times
    and can’t afford anymore to maintain the current amount of self-driving
    cars. The management decided to stop using 10% of all self-driving cars,
    which take least amount of orders for the last 3 months.
    """
    pass


@intro
def select_3_8():
    """
    The company management decided to participate in the research on “does customer
    location of residence depend on how many charging station the self-driving cars
    was using the same day”. Now you as DB developer need to provide this data.
    You’ve decided to collect the data for each day within one month and then sum them up.
    """
    pass


@intro
def select_3_9():
    """
    The company management decided to optimize repair costs by buying parts in bulks
    from providers for every workshop. Help them decide which parts are used the
    most every week by every workshop and compute the necessary amount of parts to order.
    """
    pass


@intro
def select_3_10():
    """
    The company management decided to cut costs by getting rid of the most expensive
    car to maintain. Find out which car type has had the highest average (per day)
    cost of repairs and charging (combined).
    """
    pass


if __name__ == '__main__':
    select_3_1()
    select_3_2()
    select_3_3()
    select_3_4()
    select_3_5()
    select_3_6()
    select_3_7()
    select_3_8()
    select_3_9()
    select_3_10()
