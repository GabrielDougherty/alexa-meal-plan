#!/usr/bin/env python3

# Playing with time in Python
from datetime import datetime, date
import urllib.request 	# for downloading PDF
from io import BytesIO 	# for treating PDF as a file stream
import re 		# regex for parsing PDF
import time
from enum import Enum 	# for MealType
import PyPDF2 		# for getting PDF into text


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
    def __init__(self, plan_meals, cur_meals, start_date=None):
        plan_meals = int(plan_meals)
        cur_meals = int(cur_meals)
        self._BLOCK_PLANS = [210, 175]
        self._WEEK_PLANS = [19, 14, 10]

        # initialize meals, start date
        self.cur_meals = cur_meals

        # determine meal plan type
        # try:
        self._plan_type = self.__det_plan_type(plan_meals)
        # except NameError: # if MealType doesn't exist
        #     print("MealPlan needs MealType to work. Please import MealType.")
        #     exit()

        # determine target meals per day
        self._target_meals = self.__det_target_meals(plan_meals)

    def __det_plan_type(self, plan_meals):
        if plan_meals in self._BLOCK_PLANS:
            return MealType.BLOCK
        elif plan_meals in self._WEEK_PLANS:
            return MealType.WEEK
        else:
            # unsure if this is the right error format
            raise ValueError(f"Invalid meal plan: {plan_meals}")

    def __det_target_meals(self, plan_meals):
        return self.cur_meals/plan_meals

    @property
    def target_meals(self):
        return self._target_meals

    @property
    def plan_type(self):
        return self._plan_type


#----------Begin Date Handler class----------
class DateHandler:
    def __init__(self, start_date=None):
        self._cur_date = datetime.now().date()


        # handle default start date
        if start_date is None:
            self.start_date = self.__default_start_date()
        else:
            # otherwise, set to given date
            self.start_date = start_date
        

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

                return self.__build_dates(cal_txt, cal_start)

        except urllib.request.URLError:
            print("mealplan: No connection to %s" % cal_url)
            exit(-1)

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

    def __build_break_date(self, cal_txt, re_begin, re_end, semester_yr=None):
        # remove newlines
        cal_txt = re.sub(r"\r|\n", "", cal_txt)
        # remove spaces (they're unreliable when parsing)
        cal_txt = re.sub(r"\s", "", cal_txt)
        print('*' * 50, "\n\n")
        # print(cal_txt[:100])
        print(cal_txt)
        print('*' * 50, "\n\n")

        # only extract the month and number
        # try:

        # explicitly specify year in search if getting semest start and end dates
        if semester_yr:
            yr_re_end = str(semester_yr) + re_end
            print(yr_re_end, re_begin)
            # TODO fix bug here
            messy_date = re.search("{}.*.,.*?,{}".format(re_begin, \
                                    yr_re_end), cal_txt, re.DOTALL).group(0)
        else:
            print(re_end, re_begin)

            messy_date = re.search("{}.*?.,.*?,....{}".format(re_begin, \
                                    re_end), cal_txt, re.DOTALL).group(0)
#/ClassesBegin.*.,.*,....LaborDay
        # except AttributeError:
        #     print("build_break_date: building break with `{}` and `{}` failed".format(re_begin, re_end))
        #     return
        # exit(-1)
        # print('*' * 50, "\n\n")
        # print(messy_date)
        # print('*' * 50, "\n\n")

        right_offset = len(re_end)
        year_name = messy_date[(-4-right_offset):-right_offset]
        # print("year:",year)
        # print("re_end:",re_end)
        # print('*' * 50, "\n\n")

        messy_date = re.search(r",.*,", messy_date, re.DOTALL).group(0)

        # get the "November 2" between the commas, then split it by its space
        month_name = re.search(r"([a-z]|[A-Z])*", messy_date.split(',')[1]).group(0)
        day = re.search(r"\d+", messy_date).group(0)
        # print(messy_date.split(',')[1],"||||",month_name, day)
        # print(month_parts)
        month_number = datetime.strptime(month_name[:3], '%b').month

        return date(int(year_name), month_number, int(day))


    def __build_dates(self, cal_txt, cal_start):

        startDates = []
        endDates = []

        startBreaksArgs = [
            [ r"ThanksgivingBreakBegins(at)?\(?CloseofClasses\)?",
              "ThanksgivingBreakEnds" ],
            [ r"SpringBreakBegins(\(?CloseofClasses\)?)?",
              "SpringBreakEnds" ],
        ]

        endBreakArgs = [
            [ r"ThanksgivingBreakEnds\(?ClassesResume\-?8:00am\)?",
              "LastDayofClass" ],
            [ r"SpringBreakEnds\(?ClassesResume\-?8:00am\)?",
              "LastDaytoWithdraw" ],
        ]

        

        # build Thanksgiving break
        # The parentheses might not read correctly
        startDates.append( self.__build_break_date(cal_txt, \

        dates['thanksgivingBreak']['end'] = self.__build_break_date(cal_txt, \
              

        # build Spring break
        dates['springBreak']['start'] = self.__build_break_date(cal_txt, \
            
        dates['springBreak']['end'] = self.__build_break_date(cal_txt, \

        # build Fall semester start and end dates
        dates['fallSemester']['start'] = self.__build_break_date(cal_txt, r"ClassesBegin",
                                                                   r"LaborDay", cal_start)
        dates['fallSemester']['end'] = self.__build_break_date(cal_txt, r"EndofSemester",
                                                                 r"Commencement", cal_start)

        # build Spring semester start and end dates
        dates['springSemester']['start'] = self.__build_break_date(cal_txt, r"ClassesBegin",
                                                                 r"LastDaytoDrop", cal_start+1)
        dates['springSemester']['end'] = self.__build_break_date(cal_txt, r"EndofSemester",
                                                                 r"Commencement", cal_start+1)
        print(dates)
        return dates


    def __days_remaining(self):

        if self._plan_type == MealType.BLOCK:
            pass #TODO get all days remaining
        else if self._plan_type == MealType.WEEK:
            if 
    
