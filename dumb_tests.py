import .meal_plan


def dumb_tests():
    # myCal = Calendar()
    # print(myCal.cur_date)
#    def __init__(self, plan_meals, cur_meals, start_date):
        
    myPlan = MealPlan(210, 120)

    try:
        badPlan = MealPlan(300, 23)
    except ValueError:
        print("Caught an error!!!!!!")
    
if __name__ == "__main__":
    dumb_tests()
