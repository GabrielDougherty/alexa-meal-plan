#!/usr/bin/env python3

import unittest
import sys

sys.path.append("..")

import mealplan

class TestParser(mealplan.ICalParser):
    def init(self, cal_start):
        pass

    def gen_cal_txt(self):
        return "FallSemester2018ClassesBeginMonday,August27,2018LaborDay(NoClasses)Monday,September3," \
              "2018LastDaytoDrop-Add4:30pmatHamiltonHallTuesday,September4,201811:59pmusingS.C.O.T.S.Tuesday," \
              "September4,2018ReadingDay(NoClasses)Tuesday,October9,2018LastDaytoWithdraw(" \
              "11:59pmusingS.C.O.T.S.)Friday,November2,2108ThanksgivingBreakBegins(CloseofClasses)Tuesday,November20," \
              "2018ThanksgivingBreakEnds(ClassesResume-8:00am)Monday,November26,2018LastDayofClassFriday,December7," \
              "2018FinalExamPeriodBeginsMonday,December10,2018EndofSemesterFriday,December14," \
              "2018CommencementSaturday,December15,2018SpringSemester2019ClassesBeginMonday,January14," \
              "2019MartinLutherKingDay(NoClasses)Monday,January21,2019LastdaytoDrop-Add4:30pmatHamiltonHallTuesday," \
              "January22,201911:59pmusingS.C.O.T.S.Tuesday,January22,2019SpringBreakBegins(CloseofClasses)Saturday," \
              "March2,2019SpringBreakEnds(ClassesResume-8:00am)Monday,March11,2019LastDaytoWithdraw(" \
              "11:59pmusingS.C.O.T.S.)Friday,March29,2019LastDayofClassMonday,April29," \
              "2019FinalExamPeriodBeginsTuesday,April30,2019EndofSemesterFriday,May3,2019CommencementSaturday,May4," \
              "2019Pleasenote:Alldatesaboveareasof4/18/2018Note:Fall2018PartofTermA(" \
              "35classdays)First7.5weeksStartDate:August27,2018LastDaytoDrop-AddŒAugust29," \
              "2018LastDaytoWithdrawŒSeptember27,20184:30pmatHamiltonHall11:59pmusingSCOTSEndDate:October16," \
              "2018Spring2019PartofTermA(35classdays)First7.5weeksStartDate:January14," \
              "2019LastDaytoDrop-AddŒJanuary16,2019LastDaytoWithdrawŒFebruary14," \
              "20194:30pmatHamiltonHall11:59pmusingSCOTSEndDate:March11,2019Fall2018PartofTermB(" \
              "35classdays)Last7.5weeksStartDate:October17,2018LastDaytoDrop-AddŒOctober19," \
              "2018LastDaytoWithdrawŒNovember18,20184:30pmatHamiltonHall11:59pmusingSCOTSEndDate:December7," \
              "2018Spring2019PartofTermB(35classdays)Last7.5weeksStartDate:March12,2019LastDaytoDrop-AddŒMarch14," \
              "2019LastDaytoWithdrawŒApril11,20194:30pmatHamiltonHall11:59pmusingSCOTSEndDate:April29,2019 "

def simple_tests():
    # myCal = Calendar()
    # print(myCal.cur_date)
    #    def __init__(self, plan_meals, cur_meals, start_date):

    my_plan = mealplan.MealPlan(210, 120)

    print("Testing error handling with plan parsing")
    try:
        badPlan = mealplan.MealPlan(300, 23)
    except ValueError:
        print("This should have been caught.")


class TestCalParser(unittest.TestCase):

    def test_parse_cal(self):
        test_parser = mealplan.CalParser(cal_start=2018)
        txt = test_parser.gen_cal_txt()


class TestBreakBuilder(unittest.TestCase):

    def test_build_breaks(self):
        txt = "FallSemester2018ClassesBeginMonday,August27,2018LaborDay(NoClasses)Monday,September3," \
              "2018LastDaytoDrop-Add4:30pmatHamiltonHallTuesday,September4,201811:59pmusingS.C.O.T.S.Tuesday," \
              "September4,2018ReadingDay(NoClasses)Tuesday,October9,2018LastDaytoWithdraw(" \
              "11:59pmusingS.C.O.T.S.)Friday,November2,2108ThanksgivingBreakBegins(CloseofClasses)Tuesday,November20," \
              "2018ThanksgivingBreakEnds(ClassesResume-8:00am)Monday,November26,2018LastDayofClassFriday,December7," \
              "2018FinalExamPeriodBeginsMonday,December10,2018EndofSemesterFriday,December14," \
              "2018CommencementSaturday,December15,2018SpringSemester2019ClassesBeginMonday,January14," \
              "2019MartinLutherKingDay(NoClasses)Monday,January21,2019LastdaytoDrop-Add4:30pmatHamiltonHallTuesday," \
              "January22,201911:59pmusingS.C.O.T.S.Tuesday,January22,2019SpringBreakBegins(CloseofClasses)Saturday," \
              "March2,2019SpringBreakEnds(ClassesResume-8:00am)Monday,March11,2019LastDaytoWithdraw(" \
              "11:59pmusingS.C.O.T.S.)Friday,March29,2019LastDayofClassMonday,April29," \
              "2019FinalExamPeriodBeginsTuesday,April30,2019EndofSemesterFriday,May3,2019CommencementSaturday,May4," \
              "2019Pleasenote:Alldatesaboveareasof4/18/2018Note:Fall2018PartofTermA(" \
              "35classdays)First7.5weeksStartDate:August27,2018LastDaytoDrop-AddŒAugust29," \
              "2018LastDaytoWithdrawŒSeptember27,20184:30pmatHamiltonHall11:59pmusingSCOTSEndDate:October16," \
              "2018Spring2019PartofTermA(35classdays)First7.5weeksStartDate:January14," \
              "2019LastDaytoDrop-AddŒJanuary16,2019LastDaytoWithdrawŒFebruary14," \
              "20194:30pmatHamiltonHall11:59pmusingSCOTSEndDate:March11,2019Fall2018PartofTermB(" \
              "35classdays)Last7.5weeksStartDate:October17,2018LastDaytoDrop-AddŒOctober19," \
              "2018LastDaytoWithdrawŒNovember18,20184:30pmatHamiltonHall11:59pmusingSCOTSEndDate:December7," \
              "2018Spring2019PartofTermB(35classdays)Last7.5weeksStartDate:March12,2019LastDaytoDrop-AddŒMarch14," \
              "2019LastDaytoWithdrawŒApril11,20194:30pmatHamiltonHall11:59pmusingSCOTSEndDate:April29,2019 "
        builder = mealplan.BreakBuilder(txt, 2018)

        dates = builder.built_dates

        self.assertNotEqual(dates.start_sem, [])
        self.assertNotEqual(dates.end_sem, [])
        self.assertNotEqual(dates.end_breaks, [])
        self.assertNotEqual(dates.start_breaks, [])

class TestDaysRemaining(unittest.TestCase):

    def test_days_remaining(self):
        rem = mealplan.DaysRemaining(cal_start=2018)

        days_rem = rem.days_remaining_until(rem.semester_end)

        self.assertNotEqual(None, days_rem)


# uncomment this line for running as regular executable
if __name__ == "__main__":
    # simple_tests()
    unittest.main()
