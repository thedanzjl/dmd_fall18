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
def select_3_2(year, month, day):
    """
    Company management wants to get a statistics on the efficiency of
    charging stations utilization. Given a date, compute how many sockets
    were occupied each hour.
    """
    date = MyDate(year, month, day)
    occupied = db.query('''SELECT usage_time, charging_time_amount FROM cars_charged 
                           WHERE date(usage_time)="{}"'''.format(str(date)))
    hours = dict()
    for hour in range(24):
        hours_occupied = '{:02}h-{:02}h'.format(hour, hour + 1)
        hours[hours_occupied] = 0
        for socket in occupied:
            duration = socket[1]
            h = int(socket[0][11:13])
            m = int(socket[0][14:16])
            if (h == hour) or (h == hour - 1 and m + duration >= 60):
                hours[hours_occupied] += 1

    out = ''
    for key, value in hours.items():
        out += str(key) + ': ' + str(value) + '\n'
    return(out)

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
    pass


@intro
def select_3_5():
    """
    The department of development has requested the following statistics:
    - Average distance a car has to travel per day to customer’s order location
    - Average trip duration
    Given a date as an input, compute the statistics above.
    """
    average_distance = db.query('''
        WITH cars_traveled_stats AS (
        SELECT c.carid, SUM(r.distance) AS traveled_total, 
        julianday(r.end_ride_time) - julianday(r.start_ride_time) AS days_traveled
        FROM cars AS c
        JOIN
        rides AS r ON r.carid = c.carid
        GROUP BY c.carid
    )
    SELECT cts.carid, cts.traveled_total / cts.days_traveled AS aver_traveled_per_day FROM cars_traveled_stats AS cts;
    ''')

    average_trip_duration = db.query('''
    SELECT sum(julianday(r.end_ride_time) - julianday(r.start_ride_time)) / count(r.rid) AS aver_trip_dur_days
    FROM rides AS r;
    ''')

    return average_distance, average_trip_duration


@intro
def select_3_6():
    """
    In order to accommodate traveling demand, the company decided to
    distribute cars according to demand locations. Your task is to
    compute top-3 most popular pick-up locations and travel destination
    for each time of day: morning (7am-10am), afternoon (12am-2pm) and evening (5pm-7pm).
    """
    places = db.query('''SELECT *
    FROM(
    SELECT * FROM(SELECT DISTINCT source_location AS morning_pick_up
                    FROM rides 
                    WHERE time(start_ride_time) BETWEEN 7 AND 10
                    GROUP BY source_location 
                    ORDER BY count(source_location) DESC
                    LIMIT 3)
    UNION
    SELECT * FROM(SELECT DISTINCT source_location AS afternoon_pick_up
                    FROM rides 
                    WHERE time(start_ride_time) BETWEEN 12 AND 14
                    GROUP BY source_location 
                    ORDER BY count(source_location) DESC
                    LIMIT 3)
    UNION
    SELECT * FROM(SELECT DISTINCT source_location AS evening_pick_up
                    FROM rides 
                    WHERE time(start_ride_time) BETWEEN 17 AND 19
                    GROUP BY source_location 
                    ORDER BY count(source_location) DESC
                    LIMIT 3)
    UNION
    SELECT * FROM(SELECT DISTINCT source_location AS morning_destination
                    FROM rides 
                    WHERE time(end_ride_time) BETWEEN 7 AND 10
                    GROUP BY destination
                    ORDER BY count(destination) DESC
                    LIMIT 3)
    UNION
    SELECT * FROM(SELECT DISTINCT source_location AS afternoon_destination
                    FROM rides 
                    WHERE time(end_ride_time) BETWEEN 12 AND 14
                    GROUP BY destination
                    ORDER BY count(destination) DESC
                    LIMIT 3)
    UNION
    SELECT * FROM(SELECT DISTINCT source_location AS evening_destination
                    FROM rides 
                    WHERE time(end_ride_time) BETWEEN 17 AND 19
                    GROUP BY destination
                    ORDER BY count(destination) DESC
                    LIMIT 3))
      ;''')
    return places


@intro
def select_3_7():
    """
    Despite the wise management, the company is going through hard times
    and can’t afford anymore to maintain the current amount of self-driving
    cars. The management decided to stop using 10% of all self-driving cars,
    which take least amount of orders for the last 3 months.
    """
    cars_ten = db.query('''
    WITH cars_stats AS(SELECT c.carid, COUNT(c.carid) AS times_used, row_number() over(ORDER BY COUNT(c.carid) asc) 
    AS row_num, tc.total_cars FROM cars AS c LEFT 
    JOIN rides AS r ON c.carid = r.carid CROSS 
    JOIN(
    SELECT COUNT(cr.carid) AS total_cars
    FROM cars AS cr) AS tc
    GROUP BY c.carid)
    SELECT cs.carid, cs.times_used
    FROM cars_stats as cs
    WHERE (cs.row_num / cs.total_cars) * 100 <= 10
''')

    return cars_ten


@intro
def select_3_8(year, month, day):
    """
    The company management decided to participate in the research on “does customer
    location of residence depend on how many charging station the self-driving cars
    was using the same day”. Now you as DB developer need to provide this data.
    You’ve decided to collect the data for each day within one month and then sum them up.

    input: year, month, day
    """

    date = MyDate(year, month, day)
    datemax = MyDate(date.y, date.m+1, date.d)

    within_month = db.query('''select cid, count(cid) from (select carid, cid from (select * from (((select usage_time, 
    carid from cars_charged) natural join (select start_ride_time, carid, cid from rides where 
    date(start_ride_time)>"{}" and date(start_ride_time)<"{}")))) where date(usage_time) = date(start_ride_time)) 
    group by cid
'''.format(str(date),str(datemax)))

    out = 'customer id, amount:'
    for i in within_month:
        out += '\n' + str(i[0]) + ', ' + str(i[1])
    return out


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
    select_3_2(2018, 11, 16)
    select_3_3()
    select_3_4()
    select_3_5()
    select_3_6()
    select_3_7()
    select_3_8(2018, 10, 1)
    select_3_9()
    select_3_10()
