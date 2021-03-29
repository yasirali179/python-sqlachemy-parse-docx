from db import create
from docx2python import docx2python


def parsing(result):
    i = 0
    import pdb; pdb.set_trace();
    while i < len(result.body):
        if len(result.body[i]) >= 2:
            data = result.body[i]
            get_preliminary_information(data)
            get_department_information(data)
            get_feedback(data)
            get_publishable_information(data)

        i = i+1


def get_preliminary_information(data):
    
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "Firm name" in data[0][0][0]:
        print("--------------------------Preliminary Information----------------------")
        print("Firm name: " + get_text(data[1][0]))
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Practice Area" in data[0][0][0]:
        print("Practice Area: " + get_text(data[1][0]))
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Location" in data[0][0][0]:
        print("Location: " + get_text(data[1][0]))
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Contact person" in data[0][0][0]:
        print("")
        print("Contact Person Details: ")
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
                print("person " + str(row-1) + " Details")
                col = 0
                while col < len(row_data):
                    if col == 0:
                        print("Name: " + get_text(row_data[col]))
                    elif col ==1:
                        print("Email: " + get_text(row_data[col]))
                    elif col ==2:
                        print("Telephone number: " + get_text(row_data[col]))
                    col = col+1
            row = row+1


def get_department_information(data):
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "Department name" in data[0][0][0]:
        print("--------------------------Department Information----------------------")
        print("Department name: " + get_text(data[1][0]))
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Number of partners" in data[0][0][0]:
        print("Number of partners: " + get_text(data[1][0]))
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "qualified lawyers" in data[0][0][0]:
        print("qualified lawyers: " + get_text(data[1][0]))
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Heads of department" in data[0][0][0]:
        print("")
        print("Heads of department Details: ")
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
                print("person " + str(row-1) + " Details")
                col = 0
                while col < len(row_data):
                    if col == 0:
                        print("Name: " + get_text(row_data[col]))
                    elif col ==1:
                        print("Email: " + get_text(row_data[col]))
                    elif col ==2:
                        print("Telephone number: " + get_text(row_data[col]))
                    col = col+1
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Hires" in data[0][0][0]:
        print("")
        print("Hires Details: ")
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
                print("person " + str(row-1) + " Details")
                col = 0
                while col < len(row_data):
                    if col == 0:
                        print("Name: " + get_text(row_data[col]))
                    elif col ==1:
                        print("Joined / Departed: " + get_text(row_data[col]))
                    elif col ==2:
                        print("Joined From / Destination (firm): " + get_text(row_data[col]))
                    col = col+1
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Information regarding lawyers (including associates) RANKED" in data[0][0][0]:
        print("")
        print("Information regarding lawyers RANKED: ")
        row = 2
        while row < len(data):
            
            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
                print("person " + str(row-1) + " Details")
                col = 0
                while col < len(row_data):
                    if col == 0:
                        print("Name: " + get_text(row_data[col]))
                    elif col ==1:
                        print("Comments: " + get_text(row_data[col]))
                    elif col ==2:
                        print("Partner Y/N: " + get_text(row_data[col]))
                    col = col+1
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Information regarding UNRANKED lawyers" in data[0][0][0]:
        print("")
        print("Information regarding lawyers UNRANKED: ")
        row = 2
        while row < len(data):
            
            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
                print("person " + str(row-1) + " Details")
                col = 0
                while col < len(row_data):
                    if col == 0:
                        print("Name: " + get_text(row_data[col]))
                    elif col ==1:
                        print("Comments: " + get_text(row_data[col]))
                    elif col ==2:
                        print("Partner Y/N: " + get_text(row_data[col]))
                    col = col+1
            row = row+1

def get_feedback(data):
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "barristers / advocates in the UK, Australia, Hong Kong, India, Malaysia, New Zealand or Sri Lanka" in data[0][0][0]:
        print("--------------------------Feed Back----------------------")
        print("information regarding if you have used barristers / advocates in the UK, Australia, Hong Kong, India, Malaysia, New Zealand or Sri Lanka.")
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                print("barristers / advocates " + str(row-1) + " Details")
                col = 0
                while col < len(row_data):
                    if col == 0:
                        print("Barrister/advocate name: " + get_text(row_data[col]))
                    elif col ==1:
                        print("Firm / Set: " + get_text(row_data[col]))
                    elif col ==2:
                        print("Comments: " + get_text(row_data[col]))
                    col = col+1
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Feedback on our previous coverage of your department" in data[0][0][0]:
        print("Feedback on our previous coverage of your department: " + get_text(data[1][0]))

def get_publishable_information(data):
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "List of this department's PUBLISHABLE clients" in data[0][0][0]:
        print("-------------------------- Publishable Information----------------------")
        print("List of this department's PUBLISHABLE clients")
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                print("Client " + str(row-1) + " Details")
                col = 0
                while col < len(row_data):
                    if col == 0:
                        print("Name of Client: " + get_text(row_data[col]))
                    elif col ==1:
                        print("New Client (Yes/No): " + get_text(row_data[col]))
                    col = col+1
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Publishable Work Highlights in last 12 months" in data[0][0][0] and "Publishable Matter" in data[1][0][0]:
        print("Feedback on our previous coverage of your department: " + get_text(data[1][0]))

def get_text(data):
    index = 0
    final_text = ''
    while index < len(data):
        final_text += data[index]
        index = index + 1
    return final_text


if __name__ == "__main__":
    result = docx2python('3362805.docx')
    parsing(result)
