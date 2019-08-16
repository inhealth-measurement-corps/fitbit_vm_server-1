#!/usr/bin/env python
import json
import datetime
import MySQLdb as db

import json
import fitbit
import requests
import base64
import sys
import re
import pytz
from dateutil import tz


EST_TZ = pytz.timezone("US/Eastern")
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')
#Remote database info
HOST = "10.162.80.9"
PORT = 3306
USER = "fitbitter"
PASSWORD = "yiGLeVihDHhQMJPo"
DB = "mmcfitbit"

get_checkin_url = "https://jhprohealth.herokuapp.com/polls/get_checkins_yesterday/"
get_survey_url = "https://jhprohealth.herokuapp.com/polls/get_surveys_yesterday/"

now = str(datetime.datetime.now())

class SurveyData:
    def __init__(self, uid, survey_string, submitted_at, weighted_scores):
        self.uid = uid
        self.survey_string = survey_string
        self.submitted_at = submitted_at
        self.weighted_scores = weighted_scores

    def __repr__(self):
        return "SurveyData(User: " + str(self.uid) + ', submitted_at: ' + str(self.submitted_at) + ', survey: ' + str(self.survey_string) + ", " + str(self.weighted_scores) + ")"

class CheckinData:
    def __init__(self, uid, checkin_type, time):
        self.uid = uid
        self.checkin_type = checkin_type
        self.time = time

    def __repr__(self):
        return "CheckinData(User: " + str(self.uid) + ', time: ' + str(self.time) + ', type: ' + str(self.checkin_type) + ")"

def main():
    survey_set = pull_yesterday_survey()
    insert_surveys(survey_set)
    checkin_set = pull_yesterday_checkin()
    insert_checkins(checkin_set)

def pull_yesterday_checkin():
    print("Retrieving surveys from yesterday...")
    r = requests.get(get_checkin_url)
    print(r.text)

    checkin_json = json.loads(r.text)
    checkin_list = []
    checkins = checkin_json["Checkins"]
    for checkin in checkins:
        checkin_time = checkin["time"]
        if '.' not in checkin_time:
            checkin_time = checkin_time[:-1] + ".000Z"
        utc = datetime.datetime.strptime(checkin_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        utc = utc.replace(tzinfo=from_zone)
        # Convert time zone
        est = utc.astimezone(to_zone).strftime("%Y-%m-%d %H:%M:%S")
        print est

        checkin_list.append(CheckinData(uid=checkin["userid"], time=est, checkin_type=checkin["ping_type"]))

    # print(uid)
    print(checkin_list)
    print("\t...Done getting yesterday's checkins")

    return checkin_list

def insert_checkins(checkin_list):
    insert_set = []
    for checkin in checkin_list:
        # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_set.append((checkin.uid, checkin.time,  checkin.checkin_type, datetime.datetime.now()))


    try:
        connection = db.Connection(host=HOST, port=PORT,
                                   user=USER, passwd=PASSWORD, db=DB)

        dbhandler = connection.cursor()
        stmt = "INSERT INTO PC_Checkin (user_id, checked_in, type, added_on) \
            VALUES (%s, %s, %s, %s)"
        dbhandler.executemany(stmt, insert_set)


    except Exception as e:
        print "EXCEPTION IN insert_checkins: " + str(e)

    finally:
        connection.commit()
        connection.close()

def pull_yesterday_survey():
    print("Retrieving surveys from yesterday...")
    r = requests.get(get_survey_url)
    print(r.text)

    survey_json = json.loads(r.text)
    print(r.text)
    survey_list = []
    surveys = survey_json["Surveys"]
    # surveys = json.loads("""{"Surveys": [{"id": 1, "submit_user_id": 999888666, "submit_time": "2018-11-29T06:37:12.767Z", "answer_sequence": "Intervention: 142232132221121112152346554321332334"},{"id": 1, "submit_user_id": 7, "submit_time": "2018-11-26T22:53:19.767Z", "answer_sequence": "Intervention: 352232333333111111134346544334333543"},{"id": 1, "submit_user_id": 6, "submit_time": "2018-11-15T22:53:57.767Z", "answer_sequence": "Intervention: 341232321233211111124366545443345334"},{"id": 1, "submit_user_id": 6, "submit_time": "2018-10-23T15:38:30.767Z", "answer_sequence": "Intervention: 342221221233111122224366556553333344"}]}""")
    # surveys = surveys["Surveys"]

    # print(surveys)

    for survey in surveys:
        print(survey)
        survey_time = survey["submit_time"]
        if '.' not in survey_time:
            survey_time = survey_time[:-1] + ".000Z"
        utc = datetime.datetime.strptime(survey_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        utc = utc.replace(tzinfo=from_zone)
        # Convert time zone
        est = utc.astimezone(to_zone).strftime("%Y-%m-%d %H:%M:%S")
        # print est
        survey_sequence = survey["answer_sequence"][-36:]
        survey_list.append(SurveyData(uid=survey["submit_user_id"], survey_string=survey_sequence, submitted_at=est, weighted_scores=calculate_category_scores(survey_sequence)))

    # print(uid)
    print(survey_list)
    print("\t...Done getting yesterday's surveys")

    return survey_list

def calculate_category_scores(survey_string):
    def recode_choices(answer_map):
        recode_type_one = [1, 2, 20, 22, 34, 36]
        recode_type_two = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        recode_type_three = [13, 14, 15, 16, 17, 18, 19]
        recode_type_four = [21, 23, 26, 27, 30]
        recode_type_five = [24, 25, 28, 29, 31]
        recode_type_six = [32, 33, 35]

        for q in recode_type_one:
            answer_map[q] = 25 * (5 - answer_map[q])
        for q in recode_type_two:
            answer_map[q] =50 * (answer_map[q] - 1)
        for q in recode_type_three:
            answer_map[q] = 100 * (answer_map[q] - 1)
        for q in recode_type_four:
            answer_map[q] = 20 * (6 - answer_map[q])
        for q in recode_type_five:
            answer_map[q] = 20 * (answer_map[q] - 1)
        for q in recode_type_six:
            answer_map[q] = 25 * (answer_map[q] - 1)
        return answer_map

    def weigh_categories(ra):
        avg_map = dict()
        avg_map["physical_functioning"] = (ra[3] + ra[4] + ra[5] + ra[6] + ra[7] + ra[8] + ra[9] + ra[10] + ra[11] + ra[12]) / float(10)
        avg_map["role_limited_physical"] = (ra[13] + ra[14] + ra[15] + ra[16]) / float(4)
        avg_map["role_limited_emotional"] = (ra[17] + ra[18] + ra[19]) / float(3)
        avg_map["energy"] = (ra[23] + ra[27] + ra[29] + ra[31]) / float(4)
        avg_map["emotional_wellbeing"] = (ra[24] + ra[25] + ra[26] + ra[28] + ra[30]) / float(5)
        avg_map["social_functioning"] = (ra[20] + ra[32]) / float(2)
        avg_map["pain"] = (ra[21] + ra[22]) / float(2)
        avg_map["general_health"] = (ra[1] + ra[33] + ra[34] + ra[35] + ra[36]) / float(5)
        return avg_map

    answer_map = dict()
    count = 1
    for i in survey_string:
        answer_map[count] = int(i)
        count += 1
    recoded_answers = recode_choices(answer_map)
    weighted_map = weigh_categories(recoded_answers)
    return weighted_map


def insert_surveys(survey_set):
    insert_set = []
    for survey in survey_set:
        dataset = list(survey.survey_string)
        # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_set.append((survey.uid, survey.submitted_at, str(datetime.datetime.now()), \
            survey.weighted_scores["physical_functioning"], survey.weighted_scores["role_limited_physical"], survey.weighted_scores["role_limited_emotional"], survey.weighted_scores["energy"], \
            survey.weighted_scores["emotional_wellbeing"], survey.weighted_scores["social_functioning"], survey.weighted_scores["pain"], survey.weighted_scores["general_health"]) \
            + tuple(dataset))

    try:
        print("Inserting surveys into DB...")
        print(insert_set)
        connection = db.Connection(host=HOST, port=PORT,
                                   user=USER, passwd=PASSWORD, db=DB)

        dbhandler = connection.cursor()
        stmt = "INSERT INTO PC_Surveys_QoL (user_id, submitted_at, added_on, \
            physical_functioning, role_limited_physical, role_limited_emotional, \
            energy, emotional_wellbeing, social_functioning, pain, general_health, \
            q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, \
            q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, \
            q21, q22, q23, q24, q25, q26, q27, q28, q29, q30, \
            q31, q32, q33, q34, q35, q36) VALUES (\
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s)"
        dbhandler.executemany(stmt, insert_set)

    except Exception as e:
        print "EXCEPTION IN insert_surveys: " + str(e)

    finally:
        connection.commit()
        connection.close()

def query_test_surveys():
    try:
        connection = db.Connection(host=HOST, port=PORT,
                                   user=USER, passwd=PASSWORD, db=DB)

        cursor = connection.cursor(db.cursors.DictCursor)
        result = cursor.execute("SELECT * FROM PC_Surveys_QoL WHERE user_id = 74477")

        rows = cursor.fetchall()

        for row in rows:
            # print(row["submitted_at"] < datetime.datetime.now())
            print(row)

        result = cursor.execute("UPDATE PC_Surveys_QoL SET physical_functioning=%s WHERE user_id=2") % datetime.datetime.now()

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        connection.close()


print("==========================================")
main()
print("Data as of: " + str(datetime.datetime.now()))
print("==========================================")

# pull_yesterday_checkin()
# query_test_surveys()
