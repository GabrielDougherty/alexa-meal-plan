#!/usr/bin/python3

import datetime
import time
import enum


# Playing with time in Python

# const meal plans
BLOCK_PLANS = [210, 175]
WEEK_PLANS = [19, 14, 10]

# user's plan. will read from user later
USER_PLAN = 19


class Calendar:
    def __init__(self):
        self._cur_date = datetime.datetime.now().date()

    @property
    def cur_date(self):
        return self._cur_date

    @cur_date.setter
    def cur_date(self, value):
        self._cur_date = value

    @cur_date.deleter
    def cur_date(self):
        del self._x

class MealType(Enum):
    BLOCK = 1
    WEEK = 2

class MealPlan:
    def __init__(self, num_meals, start_date):
        self.num_meals = num_meals
        self.start_date = start_date

        # determine plan type
        if num_meals in BLOCK_PLANS:
            self.plan_type = MealType.BLOCK
        else if plan in WEEK_PLANS:
            self.plan_name = MealType.WEEK
        else:
            raise NameError("Invalid block plan")

    

def print_time():
    print("Current date: ", datetime.datetime.now().date())

def main():
    print_time()
    myCal = Calendar()
    print(myCal.cur_date)

if __name__ == "__main__":
    main()
