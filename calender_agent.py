#import table csv
#read notNULL Alexander table data
#collect Data (date, time, location, description)
#fill out google calender with collected data

import csv
from sys import argv
from datetime import datetime, timedelta

termine = []

def main():
    # Beispiel-Daten für Termine

    if len(argv) != 2:
        print("No csv file provided.")
        exit(1)

    username = input("Wie ist dein Name im Arbeitsplandokument?")

    with open(argv[1], 'r') as file:
        reader = csv.reader(file)
        myrows = []  # myrows[0] are the dates and the following are the inputs for my appointments


        for index, row in enumerate(reader):
            if index == 2:
                myrows.append(row)
                print(myrows)

            if row[1] == username:
                myrows.append(row)

        # Die Conditionals nochmal überarbeiten! Es geht immer out of range!
        for index, row in enumerate(myrows):
            #if index == 2 or (index >= 4 and index<len(myrows)):
            for item_index, item in enumerate(row):
                if item!= "" and item[0].isnumeric():
                    try:
                        if myrows[index+1][item_index][0] in ("R", "K", "E"):
                            date=convertToUsableDate(f"{myrows[0][item_index]}")
                            output = item.split()
                            print(output)
                            starttime = output[0].replace(".", ":")
                            print(f"Starttime is {starttime}")
                            try:
                                location = output[1][0]
                            except:
                                location = ""
                                print("An exception occurred")

                            # Zugriff auf die nächste Zeile (index + 1), wenn vorhanden
                            if index + 1 < len(myrows):
                                next_row = myrows[index + 1]
                                # Beispiel: Nimm die erste Zelle als Beschreibung
                                if item_index < len(next_row):
                                    description = next_row[item_index] if next_row else ""
                                else:
                                    print("Keine nächste Zeile vorhanden")

                            try:
                                if index+3>=len(myrows) or myrows[index+3][item_index]!=myrows[index+1][item_index]:
                                    endtime = calculateEndtime(starttime, 4)
                                    makeTermin(starttime, date, endtime, location, description)
                                else:
                                    endtime = calculateEndtime(starttime, 4)
                                    makeTermin(starttime, date, endtime, location, description)
                                    makeTermin(endtime, date, calculateEndtime(endtime, 4), location, description)
                            except:
                                starttime= "23:33"
                                endtime="23:35"
                                print("Zeitformat ist nicht gültig.")

                            starttime, date, endtime, location, description = "", "", "", "", ""
                    except:
                        print("Nextrow_Item is empty")
            print("--------------------------------")

    # Spaltennamen wie von Google Kalender erwartet
    feldnamen = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location', 'Private']


    # Schreibe die CSV-Datei
    with open('output/google_calendar_import_' + username.split()[0] + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=feldnamen)
        writer.writeheader()
        for termin in termine:
            writer.writerow(termin)

    print('Die Datei ' + csvfile.name + ' wurde erstellt.')

def convertToUsableDate(input_date):
    year = datetime.now().year
    splitString = input_date.split("-")

    if len(splitString[0])==1:
        day=f"0{splitString[0]}"
    else:
        day = splitString[0]

    if splitString[1][:3].lower()=="jun":
        month="06"
    elif splitString[1][:3].lower()=="jul":
        month="07"
    elif splitString[1][:3].lower()=="aug":
        month="08"
    elif splitString[1][:3].lower()=="sep":
        month="09"
    elif splitString[1][0].lower()=="m":
        month="05"
    elif splitString[1][:3].lower()=="apr":
        month="04"
    elif splitString[1][:2].lower()=="ok":
        month="10"
    else:
        return "Fehler im Datum"
    return f"{day}.{month}.{year}"

def makeTermin(starttime, date, endtime, location, description):
    termin={
        'Subject': f"{description} in {location}",
        'Start Time': starttime,
        'Start Date': date,
        'End Date': date,
        'End Time': endtime,
        'Location': location,
        'Description': description,
        'All Day Event': 'FALSE'
    }
    print("Das hier sind die Infos im neuen Termin:" + str(termin))
    termine.append(termin)
    print(f"Starttime ist jetzt {starttime}")

def calculateEndtime(starttime, time_delta):
    time = datetime.strptime(starttime, "%H:%M")
    time = time + timedelta(hours=time_delta)
    return time.strftime("%H:%M")

if __name__ == "__main__":
    main()
