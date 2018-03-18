#!/usr/bin/env python

# Playing with time in Python

from datetime import datetime, date
import time
from enum import Enum # for MealType
import urllib.request # for downloading PDF
import PyPDF2 # for parsing PDF


class MealType(Enum):
    BLOCK = 1
    WEEK = 2

# MealPlan class
# NOTE: needs MealType to work
# plan_meals: # of meals in the meal plan
# cur_meals: # of current meals
# start_date: start date of school
# cur_date: current date
# plan_type: meal or block plan type
# target_meals: target number of meals to spend each day

class MealPlan:
    def __init__(self, plan_meals, cur_meals, start_date = None):
        BLOCK_PLANS = [210, 175]
        WEEK_PLANS = [19, 14, 10]

        # handle default start date
        if start_date is None:
            self.start_date = self.__default_start_date()
        else:
            # otherwise, set to given date
            self.start_date = start_date

        # initialize meals, start date
        self.cur_meals = cur_meals
        self.cur_date = datetime.now().date()
        
        # determine meal plan type
        # try:
        self._plan_type = self.__det_plan_type(plan_meals)
        # except NameError: # if MealType doesn't exist
        #     print("MealPlan needs MealType to work. Please import MealType.")
        #     exit()

        # determine target meals per day
        self._target_meals = self.__det_target_meals(plan_meals)
        
    def __det_plan_type(self, plan_meals):
        if plan_meals in BLOCK_PLANS:
            return MealType.BLOCK
        elif plan_meals in WEEK_PLANS:
            return MealType.WEEK
        else:
            # unsure if this is the right error format
            raise ValueError("Invalid block plan")

    def __det_target_meals(self, plan_meals):
        return self.cur_meals/plan_meals

    # default start date is August 28 of current year
    # this is correct for 2017
    def __default_start_date(self):
        start_date = date(int(datetime.now().year), 8, 28)
        return start_date

    # return starting year semester
    def __semester_start():
        # if the current date is before August, it's Spring
        # otherwise, it's fall
        
        if cur_date.month < 8:
            return cur_date.year-1
        else:
            return cur_date.year

    def __parse_calendar():
        # calendar URL
        cal_start = __semester_start()
        base_url = "http://www.edinboro.edu/directory/offices-services/records/academic-calendars/Academic-Calendar-{}-{}.pdf"
        cal_url = base_url.format(cal_start, cal_start % 2000 + 1) # i.e., 2017-18
        cal_html = None

        try:
            with urllib.request.urlopen(cal_url) as response:
                cal_html = response.read()
                
        except URLError:
            print("mealplan: No connection to %s" % cal_url)
            exit(-1)

        return cal_html

    
    @property
    def target_meals(self):
        return self._target_meals

    @property
    def plan_type(self):
        return self._plan_type
    
