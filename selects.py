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
def select_3_3(year, month, day):
    """
    Company management considers using price increasing coefficients.
    They need to gather statistics for one week on how many cars are busy
    (% to the total amount of taxis) during the morning (7AM - 10 AM),
    afternoon (12AM - 2PM) and evening (5PM - 7PM) time.
    """
    date_given = MyDate(year, month, day)
    amount_morning = db.query(('''
    SELECT
    CAST(count(distinct carid) AS REAL) / (SELECT count() FROM cars) * 100
    AS percentage FROM rides
    WHERE CAST(strftime('%H', start_ride_time) AS INTEGER) >= 7 
    AND CAST(strftime('%H', start_ride_time) AS INTEGER) < 10
    AND DATE(start_ride_time) >= DATE('{}')
    AND DATE(start_ride_time) < DATE('{}', '+7 days');
    ''').format(date_given, date_given))

    amount_afternoon = db.query(('''
    SELECT
    CAST(count(DISTINCT carid) AS REAL) / (SELECT count() FROM cars) * 100 
    AS percentage FROM rides
    WHERE CAST(strftime('%H', start_ride_time) AS INTEGER) >= 12 
    AND CAST(strftime('%H', start_ride_time) AS INTEGER) < 14
    AND DATE(start_ride_time) >= DATE('{}')
    AND DATE(start_ride_time) < DATE('{}', '+7 days');
    ''').format(date_given, date_given))

    amount_evening = db.query(('''
    SELECT
    CAST(count(DISTINCT carid) AS REAL) / (SELECT count() FROM cars) * 100 
    AS percentage FROM rides
    WHERE CAST(strftime('%H', start_ride_time) AS INTEGER) >= 17 
    AND CAST(strftime('%H', start_ride_time) AS INTEGER) < 19
    AND DATE(start_ride_time) >= DATE('{}')
    AND DATE(start_ride_time) < DATE('{}', '+7 days');
    ''').format(date_given, date_given))

    return amount_morning, amount_afternoon, amount_evening


@intro
def select_3_4(cid):
    """
    A customer claims that he was charged twice for the trip, but he
    can’t say exactly what day it happened (he deleted notification from
    his phone and he is too lazy to ask the bank), so you need to check all
    his payments for the last month to be be sure that nothing was doubled.
    """

    a = db.query('''
SELECT cid,
       abs(num_of_payments_this_month - num_of_rides_this_month) AS delta
FROM
  (SELECT count(ptm) AS num_of_payments_this_month,
          cid
   FROM
     (SELECT date(paytime) AS ptm,
             cid,
             payid
      FROM payments
      WHERE date(paytime) BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')
        AND cid = '{}'))
NATURAL JOIN
  (SELECT count(ert) AS num_of_rides_this_month,
          cid
   FROM
     (SELECT date(end_ride_time) AS ert,
             cid
      FROM rides
      WHERE date(end_ride_time) BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')
        AND cid ='{}'))'''.format(cid,cid))

    out = ''
    if len(a)!=0:
        if a[0][1] != 0:
            out+='there is a problem with transactions of customer with id ' + str(a[0][0])
        else:
            out+='there are no problems with transactions of customer with id ' + str(a[0][0])

    return out


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
    morning_pick_up = db.query('''
    SELECT DISTINCT source_location AS morning_pick_up
                    FROM rides 
                    WHERE CAST(strftime('%H', start_ride_time) AS INTEGER)>= 7 
                    AND CAST(strftime('%H', start_ride_time) AS INTEGER) <10
                    GROUP BY source_location 
                    ORDER BY count(source_location) DESC
                    LIMIT 3;
                    ''')

    afternoon_pick_up = db.query('''
    SELECT DISTINCT source_location AS afternoon_pick_up
                    FROM rides 
                    WHERE CAST(strftime('%H', start_ride_time) AS INTEGER)>= 12 
                    AND CAST(strftime('%H', start_ride_time) AS INTEGER) <14
                    GROUP BY source_location 
                    ORDER BY count(source_location) DESC
                    LIMIT 3;
                    ''')
    evening_pick_up = db.query('''
    SELECT DISTINCT source_location AS evening_pick_up
                    FROM rides 
                    WHERE CAST(strftime('%H', start_ride_time) AS INTEGER)>= 17 
                    AND CAST(strftime('%H', start_ride_time) AS INTEGER) <19
                    GROUP BY source_location 
                    ORDER BY count(source_location) DESC
                    LIMIT 3;
                    ''')
    morning_destination = db.query('''
    SELECT DISTINCT source_location AS morning_destination
                    FROM rides 
                    WHERE CAST(strftime('%H', end_ride_time) AS INTEGER)>= 7 
                    AND CAST(strftime('%H', end_ride_time) AS INTEGER) <10
                    GROUP BY destination
                    ORDER BY count(destination) DESC
                    LIMIT 3;
                    ''')
    afternoon_destination = db.query('''
    SELECT DISTINCT source_location AS afternoon_destination
                    FROM rides 
                    WHERE CAST(strftime('%H', end_ride_time) AS INTEGER)>= 12 
                    AND CAST(strftime('%H', end_ride_time) AS INTEGER) <14
                    GROUP BY destination
                    ORDER BY count(destination) DESC
                    LIMIT 3;
                    ''')
    evening_destination = db.query('''
    SELECT DISTINCT source_location AS evening_destination
                    FROM rides 
                    WHERE CAST(strftime('%H', end_ride_time) AS INTEGER)>= 17 
                    AND CAST(strftime('%H', end_ride_time) AS INTEGER) <19
                    GROUP BY destination
                    ORDER BY count(destination) DESC
                    LIMIT 3;
                    ''')
    return morning_pick_up, afternoon_pick_up, evening_pick_up, morning_destination, afternoon_destination, evening_destination


@intro
def select_3_7():
    """
    Despite the wise management, the company is going through hard times
    and can’t afford anymore to maintain the current amount of self-driving
    cars. The management decided to stop using 10% of all self-driving cars,
    which take least amount of orders for the last 3 months.
    """
    cars_ten = db.query('''
    WITH cars_stats AS(
    SELECT c.carid, count(c.carid) as times_used, tc.total_cars
    FROM cars AS c
    LEFT JOIN rides AS r ON c.carid = r.carid
    CROSS JOIN (
              SELECT count(cr.carid) AS total_cars
              FROM cars AS cr) AS tc
    GROUP BY c.carid), numbered_cars AS(
    SELECT cs.carid, cs.times_used, cs.total_cars, ( select count(ics.carid)
           FROM cars_stats AS ics
           WHERE ics.carid <= cs.carid) AS row_num
    FROM cars_stats AS cs)
    SELECT cs.carid, cs.times_used
    FROM numbered_cars AS cs
    limit (select count() from cars)/10;
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

    within_month = db.query('''
SELECT cid,
       count(cid)
FROM
  (SELECT carid,
          cid
   FROM (
           (SELECT usage_time,
                   carid
            FROM cars_charged)
         NATURAL JOIN
           (SELECT start_ride_time,
                   carid,
                   cid
            FROM rides
            WHERE date(start_ride_time)>"{}"
              AND date(start_ride_time)<"{}"))
   WHERE date(usage_time) = date(start_ride_time))
GROUP BY cid'''.format(str(date),str(datemax)))

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
    # our workshops sell parts (and install them), so we will find the best selling part per week in each workshop
    a = db.query('''
SELECT wid,
       cpid,
       max((cast(AVG AS float)/COUNT)) AS AVG
FROM
  (SELECT wid,
          cpid,
          count(cpid) AS COUNT,
          sum(amnt) AS AVG
   FROM
     (SELECT wid,
             cpid,
             max(amnt) AS amnt,
             week
      FROM
        (SELECT wid,
                cpid,
                sum(amount) AS amnt,
                strftime('%W', selltime) AS week
         FROM workshops_sell_car_parts
         GROUP BY wid,
                  week,
                  cpid)
      GROUP BY wid,
               week)
   GROUP BY wid,
            cpid)
GROUP BY wid
''')
    out = 'workshop id, carpart id, avegare number per week\n'
    for i in a:
        out+=str(i[0]) + ', ' + str(i[1]) + ', ' + str(i[2]) + '\n'

    return out


@intro
def select_3_10():
    """
    The company management decided to cut costs by getting rid of the most expensive
    car to maintain. Find out which car type has had the highest average (per day)
    cost of repairs and charging (combined).
    """

    a = db.query('''
SELECT ctid,
       max(SUM)
FROM
  (SELECT sum(charge_exp_per_day + cast(ifnull(repair_exp_per_day, 0) AS float))/count(ctid) AS SUM,
          ctid
   FROM
     (SELECT *
      FROM
        (SELECT carid,
                cast(sum(sp) AS float)/count(days) AS charge_exp_per_day from
           (SELECT carid, sum(price) AS sp, date(usage_time) AS days
            FROM cars_charged
            GROUP BY date(usage_time), carid
            ORDER BY carid)
         GROUP BY carid) AS t2
      LEFT JOIN
        (SELECT carid,
                cast(sum(sp) AS float)/count(days) AS repair_exp_per_day from
           (SELECT carid, sum(price) AS sp, date(date_of_repair) AS days
            FROM cars_repaired
            GROUP BY date(date_of_repair), carid
            ORDER BY carid)
         GROUP BY carid) AS t1 ON t1.carid = t2.carid
      UNION ALL SELECT * from
        (SELECT carid, cast(sum(sp) AS float)/count(days) AS repair_exp_per_day from
           (SELECT carid, sum(price) AS sp, date(date_of_repair) AS days
            FROM cars_repaired
            GROUP BY date(date_of_repair), carid
            ORDER BY carid)
         GROUP BY carid) AS t1
      LEFT JOIN
        (SELECT carid,
                cast(sum(sp) AS float)/count(days) AS charge_exp_per_day from
           (SELECT carid, sum(price) AS sp, date(usage_time) AS days
            FROM cars_charged
            GROUP BY date(usage_time), carid
            ORDER BY carid)
         GROUP BY carid) AS t2 ON t1.carid = t2.carid
      WHERE t2.carid IS NULL )
   NATURAL JOIN cars
   GROUP BY ctid)''')

    out = 'cartype, average expenses per day \n'
    for i in a:
        out+=str(i[0]) + ', ' + str(i[1]) + '\n'

    return out

if __name__ == '__main__':
    select_3_1()
    select_3_2(2018, 11, 16)
    select_3_3(2018, 11, 16)
    select_3_4(1)
    select_3_5()
    select_3_6()
    select_3_7()
    select_3_8(2018, 10, 1)
    select_3_9()
    select_3_10()
