#!/usr/bin/python3

from datetime import datetime, date
import time
from enum import Enum


# Playing with time in Python

# const meal plans
BLOCK_PLANS = [210, 175]
WEEK_PLANS = [19, 14, 10]

# user's plan. will read from user later
USER_PLAN = 19


class Calendar:
    def __init__(self):
        self._cur_date = datetime.now().date()

    @property
    def cur_date(self):
        return self._cur_date

    @cur_date.setter
    def cur_date(self, value):
        self._cur_date = value

    # @cur_date.deleter
    # def cur_date(self):
    #     del self._x

class MealType(Enum):
    BLOCK = 1
    WEEK = 2


# MealPlan class
# plan_meals: # of meals in the meal plan
# cur_meals: # of current meals
# start_date: start date of school
# cur_date: current date
# plan_type: meal or block plan type
# target_meals: target number of meals to spend each day

class MealPlan:
    def __init__(self, plan_meals, cur_meals, start_date = None):
        if start_date is None:
            self.start_date = self.__default_start_date()
        else:
            self.start_date = start_date

        # initialize meals, start date
        self.cur_meals = cur_meals
        self.cur_date = datetime.now().date()
        
        # determine meal plan type
        self._plan_type = self.__det_plan_type(plan_meals)

        # determine target meals per day
        self._target_meals = self.__det_target_meals
        
    def __det_plan_type(self, plan_meals):
        if plan_meals in BLOCK_PLANS:
            return MealType.BLOCK
        elif plan_meals in WEEK_PLANS:
            return MealType.WEEK
        else:
            # unsure if this is the right error format
            raise ValueError("Invalid block plan")

    def __det_target_meals(self):
        return self.cur_meals/self.plan_meals

    # default start date is Fall 2017 start date (August 28, 2017)
    def __default_start_date(self):
        start_date = date(int(datetime.now().year), 8, 28)
        return start_date
        
    @property
    def target_meals(self):
        return self._target_meals

    @property
    def plan_type(self):
        return self._plan_type
    

def print_time():
    print("Current date: ", datetime.now().date())

def main():
    # print_time()
    # myCal = Calendar()
    # print(myCal.cur_date)
#    def __init__(self, plan_meals, cur_meals, start_date):
        
    myPlan = MealPlan(210, 120)

    try:
        badPlan = MealPlan(300, 23)
    except ValueError:
        print("Caught an error!!!!!!")
    
if __name__ == "__main__":
    main()
