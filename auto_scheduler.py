
from __future__ import division
import pyomo
from pyomo.environ import *
from pyomo.opt import *

# Initialize
openning_time = 8
closing_time = 22
bts = ["james","jone","jake"]
bt_salary = 7
ssv_salary = 14
ssv = ["amy","emily",'erica']
minimal_server = 2
hours_limit_per_week = 45
hours_min_per_week = 35
n_days_limit = 6
#employees = bts+ssv

# start model
model = ConcreteModel()
model.name="scheduler"

model.days = RangeSet(1,7)
model.hours = RangeSet(openning_time,closing_time)
model.bts = Set(initialize=bts)
model.ssv = Set(initialize = ssv)


model.x_bts = Var(model.bts,model.days,model.hours, within=Binary)
model.x_ssv = Var(model.ssv,model.days,model.hours,within = Binary)

model.y_bts = Var(model.bts,model.days,within=Binary)
model.y_ssv = Var(model.ssv,model.days,within= Binary)

model.z_bts = Var(model.bts,model.days,within=Binary)
model.z_ssv = Var(model.ssv,model.days,within= Binary)

model.shift_morning_bts = Var(model.bts, model.days,within = Binary)
model.shift_evening_bts = Var(model.bts, model.days,within = Binary)
model.shift_morning_ssv = Var(model.ssv, model.days,within = Binary)
model.shift_evening_ssv = Var(model.ssv, model.days,within = Binary)

def days_bts(model,a,b,c):
    return model.z_bts[a,b] >= model.x_bts[a,b,c]
model.con_days_bts = Constraint(model.bts,model.days, model.hours,rule= days_bts)

def days_ssv(model,a,b,c):
    return model.z_ssv[a,b] >= model.x_ssv[a,b,c]
model.con_days_ssv = Constraint(model.ssv,model.days, model.hours,rule= days_ssv)

def days_limit_bts(model,a):
    return sum(model.z_bts[a,b] for b in model.days) <= n_days_limit
model.con_day_limit_bts = Constraint(model.bts,rule=days_limit_bts)

def days_limit_ssv(model,a):
    return sum(model.z_ssv[a,b] for b in model.days) <= n_days_limit
model.con_day_limit_ssvs = Constraint(model.ssv,rule=days_limit_ssv)

def bts_morning_limit(model,a):
    return sum (model.shift_morning_bts[a,b] for b in model.days) <=4
model.conBTSMorningLimit = Constraint(model.bts,rule=bts_morning_limit)

def bts_evening_limit(model,a):
    return sum (model.shift_evening_bts[a,b] for b in model.days) <=4
model.conBTSEveningLimit = Constraint(model.bts,rule=bts_evening_limit)

def ssv_morning_limit(model,a):
    return sum (model.shift_morning_ssv[a,b] for b in model.days) <=4
model.conSSVMorningLimit = Constraint(model.ssv,rule=ssv_morning_limit)

def ssv_evening_limit(model,a):
    return sum (model.shift_evening_ssv[a,b] for b in model.days) <=4
model.conSSVEveningLimit = Constraint(model.ssv,rule=ssv_evening_limit)

def con_shift_morning_ssv(model,a,b,c):
    return getattr(model,"shift_morning_ssv")[a,b] >= model.x_ssv[a,b,c]
def con_shift_evening_ssv(model,a,b,c):
    return getattr(model,"shift_evening_ssv")[a,b] >= model.x_ssv[a,b,c]
model.conShiftMorningSSV = Constraint(model.ssv,model.days,
                               RangeSet(openning_time,openning_time+5),
                               rule = con_shift_morning_ssv)
model.conShiftEveningSSV = Constraint(model.ssv,model.days,
                               RangeSet(closing_time-5,closing_time),
                               rule = con_shift_evening_ssv)

def con_morning_shift_bts(model,a,b,c):
    return model.shift_morning_bts[a,b] >= model.x_bts[a,b,c]
model.conMorningShiftBts = Constraint(model.bts,model.days,
                                      RangeSet(openning_time,openning_time+5),
                                      rule = con_morning_shift_bts)
def con_evening_shift_bts(model,a,b,c):
    return model.shift_evening_bts[a,b] >= model.x_bts[a,b,c]
model.conEveningShiftBts = Constraint(model.bts,model.days,
                                      RangeSet(closing_time-5,closing_time),
                                      rule = con_evening_shift_bts)

def con_bts_morning_evening(model,a,b):
    return model.shift_morning_bts[a,b]+model.shift_evening_bts[a,b] <=1
model.conBTSMorningEvening = Constraint(model.bts,model.days,rule=con_bts_morning_evening)

def con_ssv_morning_evening(model,a,b):
    return model.shift_morning_ssv[a,b]+model.shift_evening_ssv[a,b] <=1
model.conSSVMorningEvening = Constraint(model.ssv,model.days,rule=con_ssv_morning_evening)

def turnover_bts(model,a,b):
    return model.shift_evening_bts[a,b]+model.shift_morning_bts[a,b+1] <=1
model.conTurnOverBTS = Constraint(model.bts,RangeSet(1,6),rule=turnover_bts)

def turnover_ssv(model,a,b):
    return model.shift_evening_ssv[a,b]+model.shift_morning_ssv[a,b+1] <=1
model.conTurnOverSSV = Constraint(model.ssv,RangeSet(1,6),rule=turnover_ssv)

# Every day work limit for Bar Tenders
def con_8_hours_per_day_bt(model,a,b):
    return sum(model.x_bts[a,b,c] for c in model.hours) <=8
model.conHourPerDayBT = Constraint(model.bts,model.days,rule = con_8_hours_per_day_bt)

# Every day work limit for SSV
def con_8_hours_per_day_ssv(model,a,b):
    return sum(model.x_ssv[a,b,c] for c in model.hours) <=8
model.conHourPerDaySSV = Constraint(model.ssv,model.days,rule = con_8_hours_per_day_ssv)

# Weekly working hours limit for BTs and SSVs
def con_ssv_week_hours_limit(model,a):
    return sum(model.x_ssv[a,b,c] for b in model.days for c in model.hours) <= hours_limit_per_week
def con_bt_week_hours_limit(model,a):
    return sum(model.x_bts[a,b,c] for b in model.days for c in model.hours) <= hours_limit_per_week
model.conSSVWeekHourLimit = Constraint(model.ssv,rule = con_ssv_week_hours_limit)
model.conBTSWeekHourLimit = Constraint(model.bts,rule = con_bt_week_hours_limit)


# Weekly working hours minimal for BTs and SSVs
def con_ssv_week_hours_min(model,a):
    return sum(model.x_ssv[a,b,c] for b in model.days for c in model.hours) >= hours_min_per_week
def con_bt_week_hours_min(model,a):
    return sum(model.x_bts[a,b,c] for b in model.days for c in model.hours) >= hours_min_per_week
model.conSSVWeekHourMin = Constraint(model.ssv,rule = con_ssv_week_hours_min)
model.conBTSWeekHourMin = Constraint(model.bts,rule = con_bt_week_hours_min)

# any worker cannot work both in the morning and evening
# def conn_night_morning_limit_bts(model,a,b,x):
#     return model.x_bts[a,b,openning_time+x]+model.x_bts[a,b,closing_time-x] <=1
# def conn_night_morning_limit_ssv(model,a,b,x):
#     return model.x_ssv[a,b,openning_time+x]+model.x_ssv[a,b,closing_time-x] <=1
# model.conMorningEveningLimitBTs = Constraint(model.bts,model.days,RangeSet(0,4),
#                                           rule=conn_night_morning_limit_bts)
# model.conMorningEveningLimitSSVs = Constraint(model.ssv,model.days,RangeSet(0,4),
#                                           rule=conn_night_morning_limit_ssv)

# always have a superviser in duty
def con_ssv_present(model,b,c):
    return sum(model.x_ssv[a,b,c] for a in model.ssv)>=1
model.connSSVPresent = Constraint(model.days,model.hours,rule=con_ssv_present)

# minimal number of server at any time
def con_minimal_server(model,b,c):
    return sum(model.x_ssv[a,b,c] for a in model.ssv)\
           +sum(model.x_bts[a,b,c] for a in model.bts) >= minimal_server
model.conMinServer = Constraint(model.days,model.hours,rule=con_minimal_server)

for bt in bts:
    x = sum(model.z_bts[bt,i] for i in model.days)
    print x

def goal(model):
    g = sum(model.x_bts[a,b,c]*bt_salary for a in model.bts for b in model.days for c in model.hours)
    # for bt in bts:
    #     x = sum(model.z_bts[bt,i] for i in model.days)
    #     g = g+ x**2
    return g
model.obj = Objective(rule = goal, sense = minimize)



print("this is monet auto sceduler")


instance = model

#instance.pprint()

# Indicate which solver to use
Opt = SolverFactory("glpk")

# Generate a solution
Soln = Opt.solve(instance)

#Load solution to instance then Display the solution
instance.solutions.load_from(Soln)
# display(instance)
#print instance.solutions

for var in instance.component_data_objects(Var):
     if var.value ==1:
         print var



# print instance.solutions
#
# print "this is solution"
# print Soln

