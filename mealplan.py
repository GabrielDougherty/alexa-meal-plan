#!/usr/bin/env python

# Playing with time in Python
from datetime import datetime, date
import urllib.request # for downloading PDF
import PyPDF2 # for getting PDF into text
from io import BytesIO # for treating PDF as a file stream
import re # regex for parsing PDF
import time
from enum import Enum # for MealType


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

        # initialize meals, start date
        self.cur_meals = cur_meals
        self._cur_date = datetime.now().date()

        self._breaks = self.__parse_calendar()
        print(self._breaks)

        # handle default start date
        if start_date is None:
            self.start_date = self.__default_start_date()
        else:
            # otherwise, set to given date
            self.start_date = start_date

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
    def __semester_start(self):
        # if the current date is before August, it's Spring
        # otherwise, it's fall
        
        if self._cur_date.month < 8:
            return self._cur_date.year-1
        else:
            return self._cur_date.year

    def __build_break_date(self, cal_txt, re_begin, re_end, yr_offset=0):
        # remove newlines
        cal_txt = re.sub(r"\r|\n", "", cal_txt)
        # print(cal_txt[:100])

        # only extract the month and number
        try:
            messy_thanks = re.search("{}.*.,.*,....{}".format(re_begin, re_end), \
                                     cal_txt, re.DOTALL).group(0)
        except AttributeError:
            print("build_break_date: building break with `{}` and `{}` failed".format(re_begin, re_end))
            return
        # exit(-1)
        # print(messy_thanks)

        messy_thanks = re.search(r",.*,", messy_thanks, re.DOTALL).group(0)

        # get the "November 2" between the commas, then split it by its space
        month_name = re.search(r"([a-z]|[A-Z])*", messy_thanks.split(',')[1]).group(0)
        day = re.search(r"\d+", messy_thanks).group(0)
        # print(messy_thanks.split(',')[1],"||||",month_name, day)
        # print(month_parts)
        month_number = datetime.strptime(month_name[:3], '%b').month

        return date(cal_start+yr_offset, month_number, int(day))


    def __build_breaks(self, cal_txt, cal_start):
        breaks = {
            'thanksgiving': {},
            'spring': {}
        }


        # build Thanksgiving break
        # The parentheses might not read correctly
        breaks['thanksgiving']['start'] = self.__build_break_date(cal_txt, \
                            "ThanksgivingBreakBegins\(?CloseofClasses\)?", "ThanksgivingBreakEnds")
        breaks['thanksgiving']['end'] = self.__build_break_date(cal_txt, \
                            "ThanksgivingBreakEnds\(?ClassesResume8:00am\)?", "LastDayofClass")

        # build Spring break
        breaks['spring']['start'] = self.__build_break_date(cal_txt, "SpringBreakBegins\(?CloseofClasses\)?", "SpringBreakEnds", 1)
        breaks['spring']['end'] = self.__build_break_date(cal_txt, \
                                                 "SpringBreakEnds\(?ClassesResume8:00am\)?", "LastDaytoWithdraw", 1)

        # print(breaks)
        return breaks

    def __parse_calendar(self):
        # calendar URL
        cal_start = self.__semester_start()
        base_url = "http://www.edinboro.edu/directory/offices-services/records/academic-calendars/Academic-Calendar-{}-{}.pdf"
        cal_url = base_url.format(cal_start, cal_start % 2000 + 1) # i.e., 2017-18

        # dumb... have to hardcode their custom URL. Likely will happen again
        if cal_start == 2017:
            cal_url = "http://www.edinboro.edu/directory/offices-services/records/academic-calendars/Academic-Calendar-2017-18-2.pdf"
            
        try:
            with urllib.request.urlopen(cal_url, timeout=2) as response:
                # this whole method is fairly fragile because the formatting could change in their PDF
                
                cal_html = response.read()

                # used the example from https://automatetheboringstuff.com/chapter13/
                calReader = PyPDF2.PdfFileReader(BytesIO(cal_html))

                # breaks are marked by SpringBreak{Begins,Ends} and
                # ThanksGivingBreak{Begins,Ends}

                # print(calReader.getPage(0).extractText())
                cal_txt = calReader.getPage(0).extractText()

                return self.__build_breaks(cal_txt, cal_start)
        
        except urllib.request.URLError:
            print("mealplan: No connection to %s" % cal_url)
            exit(-1)

    @property
    def target_meals(self):
        return self._target_meals

    @property
    def plan_type(self):
        return self._plan_type
    
