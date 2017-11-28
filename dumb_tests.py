#!/usr/bin/python3

import calendar_stuff


def dumb_tests():
    # myCal = Calendar()
    # print(myCal.cur_date)
#    def __init__(self, plan_meals, cur_meals, start_date):
        
    myPlan = calendar_stuff.MealPlan(210, 120)

    print("Testing error handling with plan parsing")
    try:
        badPlan = calendar_stuff.MealPlan(300, 23)
    except ValueError:
        print("This should have been caught.")

# uncomment this line for running as regular executable
#if __name__ == "__main__":
dumb_tests()
