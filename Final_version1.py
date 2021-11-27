# ---------------------------------
import requests

from pygame import mixer
from datetime import datetime, timedelta
import time

base_url = "https://api.telegram.org/bot2104687208:AAFjWXHwwVpe9SFthTHiw1QzrvSHOP3Wo2g"


# ------------------------------

# ---------- read message from Telegram API------------------------------
def read_msg(offset):
    parameters = {
        "offset": offset
    }
    resp = requests.get(base_url + "/getUpdates", data=parameters)
    data = resp.json()
    print(data)
    for result in data["result"]:
        fun1(result)
    if data["result"]:
        return data["result"][-1]["update_id"] + 1


# ------------------------------------------------


# ----------------------Function for  Text and Username  -----------------------------
def fun1(message):
    text = message["message"]["text"]
    message_id = message["message"]["message_id"]
    #print(text)
    name = message["message"]["from"]["username"]
    solve(text, message_id,name)


# ------------ Send Message Function --------------------
def send_msg(answer, message_id):
    parameters = {
        "chat_id": "-1001663608248",
        "text": answer,
        "reply_to_message_id": message_id
    }

    resp = requests.get(base_url + "/sendMessage", data=parameters)
    # print(resp.text)


# --------------------------------------------------------------------


# ---------------------------------------------------------------------
def solve(text, message_id, name):
    # pin = input("Enter Pincode to Search vaccine")
    age = 52
    pincodes = [text]
    num_days = 1

    print_flag = 'Y'

    print("Starting search for Covid vaccine slots!")

    actual = datetime.today()  # Todays Actual date
    list_format = [actual + timedelta(days=i) for i in
                   range(num_days)]  # conver date in List formate by timedelta method
    actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]  # Fetch dates from List and store date in DATE format
    # ----------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------
    # we will run loop to fetch detail of sloat
    global x
    x = True
    while x:
        counter = 0  # counter

        for pincode in pincodes:  # each pincode
            for given_date in actual_dates:  # for each given date for each pincode

                # API url for COWIN
                URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                    pincode, given_date)
                # go to get request
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

                # get request . it all  Data for Pincode
                result = requests.get(URL, headers=header)

                if result.ok:
                    response_json = result.json()
                    if response_json["centers"]:
                        if (print_flag.lower() == 'y'):
                            for center in response_json["centers"]:
                                for session in center["sessions"]:
                                    for slots in session["slots"]:

                                        answer = """--------------------------------\n"""
                                        answer += f"""  Vaccine Tracker {center["district_name"]} \n"""
                                        answer += """------------------------------\n"""
                                        if (session["min_age_limit"] <= age and session["available_capacity"] > 0):
                                            answer += f"""Pincode : {pincode}\n"""
                                            answer += f"""Available on {format(given_date)}\n"""
                                            answer += f"""\t{center["name"]}\n"""
                                            answer += f"""\t{center["block_name"]}\n"""
                                            answer += f"""\tPrice : {center["fee_type"]}\n"""
                                            answer += f"""\tTime  : {slots}\n"""
                                            answer += f"""\tAvailability : {session["available_capacity"]}\n"""
                                            answer += f"""\t\tDose 1  : {session["available_capacity_dose1"]}\n"""
                                            answer += f"""\t\tDose 2  : {session["available_capacity_dose2"]}\n"""

                                        if (session["vaccine"] != ''):
                                            answer += f"""\tVaccine Type : {session["vaccine"]}\n"""
                                        answer += f"""****************************\n"""
                                        # print(answer)
                                        send_msg(answer, message_id)
                                        counter = counter + 1


            else:
                print(f"No Response! :- Total Responces :{counter}")
                x = False

    if counter == 0:

        print("No Vaccination slot available!")
        ans = f"""Mr/Mrs {name} plz Enter PINCODE in correct format  """
        send_msg(ans,message_id)
        x = False


# --------------------------------------------------------

offset = 4
while True:
    offset = read_msg(offset)
