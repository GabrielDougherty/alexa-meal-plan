#!/usr/bin/env python3

# Playing with time in Python
from datetime import datetime, date
import urllib.request  # for downloading PDF
from io import BytesIO  # for treating PDF as a file stream
import re  # regex for parsing PDF
from enum import Enum  # for MealType
import calendar
import PyPDF2  # for getting PDF into text


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
    def __init__(self, plan_meals, _cur_meals):
        plan_meals = int(plan_meals)
        self._cur_meals = int(_cur_meals)
        self._BLOCK_PLANS = [210, 175]
        self._WEEK_PLANS = [19, 14, 10]

        # initialize meals, start date
        self._cur_meals = _cur_meals

        # determine meal plan type
        # try:
        self._plan_type = self.__det_plan_type(plan_meals)
        # except NameError: # if MealType doesn't exist
        #     print("MealPlan needs MealType to work. Please import MealType.")

        # determine target meals per day
        self._target_meals = self.__det_target_meals()

    def __det_plan_type(self, plan_meals):
        if plan_meals in self._BLOCK_PLANS:
            return MealType.BLOCK
        elif plan_meals in self._WEEK_PLANS:
            return MealType.WEEK
        else:
            # unsure if this is the right error format
            raise ValueError(f"Invalid meal plan: {plan_meals}")

    def __det_target_meals(self):
        target = None
        parser = CalParser()
        rem = DaysRemaining(parser)

        if self._plan_type == MealType.BLOCK:
            target = self._cur_meals/rem.days_remaining_until(rem.semester_end)
        elif self._plan_type == MealType.WEEK:
            today = rem.cur_date

            sunday = today + (today.weekday() % calendar.SUNDAY).days
            target = rem.days_remaining_until(sunday)

        return target

    # get number of days remaining before last_day
    def __days_remaining(self, last_day):
        rem = DaysRemaining()
        return rem.days_remaining_until(last_day)

    @property
    def target_meals(self):
        return self._target_meals

    @property
    def plan_type(self):
        return self._plan_type

    @property
    def cur_meals(self):
        return self._cur_meals

class ICalParser:
    def __init__(self):
        pass
        # except NotImplementedError("This should be implemented")

    def gen_cal_txt(self):
        raise NotImplementedError("This should be implemented")

class CalParser(ICalParser):
    def __init__(self):
        self._cur_date = datetime.now().date()

    def gen_cal_txt(self) -> str:
        cal_txt = self.__parse_calendar()

        def filtered_cal_txt():
            filters = [
                r"\r|\n",  # newlines
                r"\s", ""  # spaces
            ]

            filtered = cal_txt
            for pattern in filters:
                filtered = re.sub(pattern, "", filtered)

            return filtered

        return filtered_cal_txt()

    def __parse_calendar(self):
        # calendar URL
        cal_start_yr = 2018  # TODO: change
        BASE_URL = "http://www.edinboro.edu/directory/offices-services/records/academic-calendars/Academic-Calendar-{}-{}.pdf"
        CAL_URL = "http://www.edinboro.edu/directory/offices-services/records/academic-calendars/Academic-Calendar-2018-19%20rev41818.pdf";
        # CAL_URL = BASE_URL.format(cal_start_yr, cal_start_yr % 2000 + 1)  # i.e., 2017-18

        try:
            with urllib.request.urlopen(CAL_URL, timeout=2) as response:
                # this whole method is fairly fragile because the formatting could change in their PDF

                cal_html = response.read()

                # used the example from https://automatetheboringstuff.com/chapter13/
                cal_reader = PyPDF2.PdfFileReader(BytesIO(cal_html))

                # breaks are marked by SpringBreak{Begins,Ends} and
                # ThanksGivingBreak{Begins,Ends}

                # print(cal_reader.getPage(0).extractText())
                cal_txt = cal_reader.getPage(0).extractText()

                return cal_txt

        except urllib.request.URLError:
            print("mealplan: No connection to %s" % CAL_URL)
            exit(-1)


class SemesterDates:
    def __init__(self, start_breaks, end_breaks, start_sem, end_sem):
        self._start_breaks = start_breaks
        self._end_breaks = end_breaks
        self._start_sem = start_sem
        self._end_sem = end_sem

    @property
    def start_breaks(self):
        return self._start_breaks

    @property
    def end_breaks(self):
        return self._end_breaks

    @property
    def start_sem(self):
        return self._start_sem

    @property
    def end_sem(self):
        return self._end_sem


class BreakBuilder:
    _dates: SemesterDates

    def __init__(self, cal_txt, cal_start):
        self._cal_txt = cal_txt
        self._dates = self.__build_dates(cal_start)

    def __build_break_date(self, re_begin, re_end, semester_yr=None):
        # remove newlines

        messy_date = ""

        # only extract the month and number
        try:
            # explicitly specify year in search if getting semest start and end dates
            if semester_yr:
                yr_re_end = str(semester_yr) + re_end
                # print(yr_re_end, re_begin)
                # TODO fix bug here
                messy_date = re.search("{}.*.,.*?,{}".format(re_begin,
                                                             yr_re_end), self._cal_txt, re.DOTALL).group(0)
            else:
                # print(re_end, re_begin)

                messy_date = re.search("{}.*?.,.*?,....{}".format(re_begin,
                                                                  re_end), self._cal_txt, re.DOTALL).group(0)
            # /ClassesBegin.*.,.*,....LaborDay
        except AttributeError as err:
            print("build_break_date: building break with `{}` and `{}` failed".format(re_begin, re_end))
            print(err)
            print(f"cal_txt {self._cal_txt}")
            exit(-1)

        right_offset = len(re_end)
        year_name = messy_date[(-4 - right_offset):-right_offset]
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

    def __build_dates(self, cal_start):

        start_breaks = []
        end_breaks = []
        start_sem = []
        end_sem = []

        start_breaks_args = [
            # thanksgiving break
            [r"ThanksgivingBreakBegins(at)?\(?CloseofClasses\)?",
             "ThanksgivingBreakEnds"],
            # spring break
            [r"SpringBreakBegins(\(?CloseofClasses\)?)?",
             "SpringBreakEnds"],
        ]

        end_break_args = [
            # thanksgiving break
            [r"ThanksgivingBreakEnds\(?ClassesResume\-?8:00am\)?",
             "LastDayofClass"],
            # spring break
            [r"SpringBreakEnds\(?ClassesResume\-?8:00am\)?",
             "LastDaytoWithdraw"],
        ]

        start_sem_args = [
            # fall semester
            [f"FallSemester{cal_start}", r"LaborDay", cal_start],
            [f"SpringSemester{cal_start + 1}ClassesBegin", r"LastDaytoDrop", cal_start + 1],
        ]

        end_sem_args = [
            [r"EndofSemester", r"Commencement", cal_start],
            [r"EndofSemester", r"Commencement", cal_start + 1],
        ]

        def append_built_date(dates, args):
            for arg in args:
                dates.append(self. __build_break_date(*arg))  # unpacks args

        append_built_date(start_breaks, start_breaks_args)
        append_built_date(end_breaks, end_break_args)
        append_built_date(start_sem, start_sem_args)
        append_built_date(end_sem, end_sem_args)

        return SemesterDates(start_breaks, end_breaks, start_sem, end_sem)

    @property
    def built_dates(self):
        return self._dates


class DaysRemaining:
    def __init__(self, parser, cal_start=None):  # TODO: parametrize classes as interfaces
        self._cur_date = datetime.now().date()
        self._cal_start = cal_start or self.__semester_start()

        parser = parser
        self._cal_txt = parser.gen_cal_txt()

        builder = BreakBuilder(self._cal_txt, self._cal_start)
        self._semester_end = builder.built_dates.end_sem

    # return starting year semester
    def __semester_start(self):
        # if the current date is before August, it's Spring
        # otherwise, it's fall

        if self._cur_date.month < 8:
            return self._cur_date.year - 1
        else:
            return self._cur_date.year

    def __is_fall(self) -> bool:
        return self._cur_date.year == self.cur_date.year

    # default start date is August 28 of current year
    # this is correct for 2017
    def __default_start_date(self):
        start_date = date(int(datetime.now().year), 8, 28)
        return start_date

    # returns val <= 0 if invalid range
    def days_remaining_until(self, till_date):
        remaining = 0

        breakbuilder = BreakBuilder(self._cal_txt, self._cal_start)
        dates = breakbuilder.built_dates

        print(dates.start_sem, 5 * '*', self._cur_date, 5 * '*', dates.end_sem)

        sem_index = 0 if self.__is_fall() else 1

        if dates.start_sem[sem_index] <= self._cur_date <= dates.end_sem[sem_index]:
            remaining = (till_date - self._cur_date).days + 1
            for start, end in zip(dates.start_breaks, dates.end_breaks):
                remaining -= self.__date_intersection(start, end, self._cur_date, till_date)

                if remaining <= 0:
                    return remaining

        return remaining

    def __days_between(self, day1, day2):
        return (day1-day2).days

    # see: https://stackoverflow.com/a/9044111/2303560
    def __date_intersection(self, start1, end1, start2, end2):
        latest_start = max(start1, start2)
        earliest_end = max(end1, end2)

        delta = (earliest_end - latest_start).days + 1
        overlap = max(0, delta)

        return overlap

    @property
    def semester_end(self):
        return self._semester_end

    @property
    def cur_date(self):
        return self._cur_date
