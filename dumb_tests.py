#!/usr/bin/python3

import calendar_stuff


def dumb_tests():
    # myCal = Calendar()
    # print(myCal.cur_date)
#    def __init__(self, plan_meals, cur_meals, start_date):
        
    myPlan = calendar_stuff.MealPlan(210, 120)

    try:
        badPlan = calendar_stuff.MealPlan(300, 23)
    except ValueError:
        print("Caught an error!!!!!!")
    
#if __name__ == "__main__":
dumb_tests()
