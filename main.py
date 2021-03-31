import os
from db import create, insert_submission_data, insert_preliminary_information, insert_department_information, insert_feedback, insert_publishable_information, insert_confidential_information, check_db
from docx2python import docx2python
from azure.storage.blob import ContainerClient

preliminary_information = {}
department_information = {}
feedback = {}
publishable_information = {'publishable_matters': []}
confidential_information = {'confidential_matters': []}


def azure():
    connection_string = "DefaultEndpointsProtocol=https;AccountName=sthistoricalsubmissions;AccountKey=5OlZ+H0GndSzvBf13VfUTXAfdQOKJ1lsWBcp+h8Zst17ks44aBu1skOdOLUOlTisdMy7hEQlwyjzvjpSOeFxfw==;EndpointSuffix=core.windows.net"
    container = ContainerClient.from_connection_string(
        connection_string, container_name="submissions")
    blob_list = container.list_blobs()

    for blob in blob_list:
        if ".docx" in blob.name and "3164475.docx" in blob.name.split('/')[2]:
            print(blob.name + '\n')
            blob_string = blob.name.split('/')
            id = check_db(
                blob_string[0], blob_string[1], blob_string[2].split('.')[0])
            if id is None:
                blob_data = container.download_blob(blob)
                if os.path.exists("BlockDestination.docx"):
                    os.remove("BlockDestination.docx")
                with open("./BlockDestination.docx", "wb") as my_blob:
                    blob_data.readinto(my_blob)
                result = docx2python('BlockDestination.docx')
                parsing(result)
                new_id = insert_submission_data(
                    blob_string[0], blob_string[1], blob_string[2].split('.')[0])
                save_data(new_id)
            break


def save_data(id):
    global preliminary_information, department_information, feedback, publishable_information, confidential_information
    insert_preliminary_information(
        int(id), preliminary_information)
    insert_department_information(
        int(id), department_information)
    insert_feedback(int(id), feedback)
    insert_publishable_information(
        int(id), publishable_information)
    insert_confidential_information(
        int(id), confidential_information)

    # Reinitialized for next parsing
    preliminary_information = {}
    department_information = {}
    feedback = {}
    publishable_information = {'publishable_matters': []}
    confidential_information = {'confidential_matters': []}


def parsing(result):
    i = 0
    while i < len(result.body):
        if len(result.body[i]) >= 2:
            data = result.body[i]
            get_preliminary_information(data)
            get_department_information(data)
            get_feedback(data)
            get_publishable_information(data)
            get_confidential_information(data)
        i = i+1


def get_preliminary_information(data):
    global preliminary_information
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "Firm name" in data[0][0][0]:
        preliminary_information["frim_name"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Practice Area" in data[0][0][0]:
        preliminary_information["practice_area"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Location" in data[0][0][0]:
        preliminary_information["localtion"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Contact person" in data[0][0][0]:
        preliminary_information["contact_person_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        detail['name'] = get_text(row_data[col])
                    elif col == 1:
                        detail['email'] = get_text(row_data[col])
                    elif col == 2:
                        phone = get_text(row_data[col]).replace(" ", "").replace(
                            "(", "").replace(")", "").replace("-", "")
                        detail['phone'] = phone
                    col = col+1
                if len(detail) != 0:
                    preliminary_information["contact_person_details"].append(
                        detail)
            row = row+1


def get_department_information(data):
    global department_information
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "Department name" in data[0][0][0]:
        department_information["department_name"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Number of partners" in data[0][0][0]:
        department_information["number_of_partners"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "qualified lawyers" in data[0][0][0]:
        department_information["qualified_lawyers"] = get_text(data[1][0])
    elif len(data[0]) >= 1 and len(data[0][0]) >= 1 and "Foreign Desks" in data[0][0][0]:
        if len(data) > 6 and "" in get_text(data[6][0]):
            department_information["department_best_known"] = get_text(
                data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Heads of department" in data[0][0][0]:
        department_information["heads_of_department_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        detail['name'] = get_text(row_data[col])
                    elif col == 1:
                        detail['email'] = get_text(row_data[col])
                    elif col == 2:
                        phone = get_text(row_data[col]).replace(" ", "").replace(
                            "(", "").replace(")", "").replace("-", "")
                        detail['phone'] = phone
                    col = col+1
                if len(detail) != 0:
                    department_information["heads_of_department_details"].append(
                        detail)
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Hires" in data[0][0][0]:
        department_information["hires_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        detail['name'] = get_text(row_data[col])
                    elif col == 1:
                        detail['joined'] = get_text(row_data[col])
                    elif col == 2:
                        detail['joined_from'] = get_text(row_data[col])
                    col = col+1
                if len(detail) != 0:
                    department_information["hires_details"].append(detail)
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Information regarding lawyers (including associates) RANKED" in data[0][0][0]:
        department_information["ranked_lawyers_details"] = []
        row = 2
        while row < len(data):

            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        detail['name'] = get_text(row_data[col])
                    elif col == 1:
                        detail['comments'] = get_text(row_data[col])
                    elif col == 2:
                        detail['is_partner'] = get_text(row_data[col])
                    col = col+1
                if len(detail) != 0:
                    department_information["ranked_lawyers_details"].append(
                        detail)
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Information regarding UNRANKED lawyers" in data[0][0][0]:
        department_information["unranked_lawyers_details"] = []
        row = 2
        while row < len(data):

            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        detail['name'] = get_text(row_data[col])
                    elif col == 1:
                        detail['comments'] = get_text(row_data[col])
                    elif col == 2:
                        detail['is_partner'] = get_text(row_data[col])
                    col = col+1
                if len(detail) != 0:
                    department_information["unranked_lawyers_details"].append(
                        detail)
            row = row+1


def get_feedback(data):
    global feedback
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "barristers / advocates in the UK, Australia, Hong Kong, India, Malaysia, New Zealand or Sri Lanka" in data[0][0][0]:
        feedback["barristers_advocates_selected_country_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        detail['name'] = get_text(row_data[col])
                    elif col == 1:
                        detail['firm'] = get_text(row_data[col])
                    elif col == 2:
                        detail['comments'] = get_text(row_data[col])
                    col = col+1
                if len(detail) != 0:
                    feedback["barristers_advocates_selected_country_details"].append(
                        detail)
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Feedback on our previous coverage of your department" in data[0][0][0]:
        feedback["previous_coverage_department_feedback"] = get_text(
            data[1][0])


def get_publishable_information(data):
    global publishable_information
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "List of this department's PUBLISHABLE clients" in data[0][0][0]:
        publishable_information["publishable_clients_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[1])) > 0 and "N/A" != get_text(row_data[0]):
                col = 1
                detail = {}
                while col < len(row_data):
                    if col == 1:
                        detail['name'] = get_text(row_data[col])
                    elif col == 2:
                        detail['is_new_client'] = get_text(row_data[col])
                    col = col+1
                if len(detail) > 0:
                    publishable_information["publishable_clients_details"].append(
                        detail)
            row = row+1
    elif len(data[0]) >= 1 and len(data[0][0]) >= 1 and (("Publishable Work Highlights in last 12 months" in data[0][0][0] and "Publishable Matter" in data[1][0][0]) or ("Publishable Matter" in data[0][0][0])):
        row = 0
        detail = {}
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" not in get_text(row_data[0]):
                if "Name of client" in get_text(row_data[0]):
                    detail['name'] = get_text(data[row+1][0])
                elif "Summary of matter and your department" in get_text(row_data[0]):
                    detail['summary'] = get_text(data[row+1][0])
                elif "Matter value" in get_text(row_data[0]):
                    detail['matter_value'] = get_text(data[row+1][0])
                elif "Is this a cross-border matter" in get_text(row_data[0]):
                    detail['is_cross_border_metter'] = get_text(data[row+1][0])
                elif "Lead partner" in get_text(row_data[0]):
                    detail['lead_partner'] = get_text(data[row+1][0])
                elif "Other team members" in get_text(row_data[0]):
                    detail['other_team_members'] = get_text(data[row+1][0])
                elif "Other firms advising on the matter" in get_text(row_data[0]):
                    detail['other_firms_advising'] = get_text(data[row+1][0])
                elif "Date of completion or current status" in get_text(row_data[0]):
                    detail['date_of_completion'] = get_text(data[row+1][0])
                elif "Other information about this matter" in get_text(row_data[0]):
                    detail['other_information'] = get_text(data[row+1][0])
            row = row+1
        if len(detail) > 0:
            publishable_information["publishable_matters"].append(detail)


def get_confidential_information(data):
    global confidential_information
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "List of this department's CONFIDENTIAL clients" in data[0][0][0]:
        confidential_information["confidential_clients_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[1])) > 0 and "N/A" != get_text(row_data[0]):
                detail = {}
                col = 1
                while col < len(row_data):
                    if col == 1:
                        detail['name'] = get_text(row_data[col])
                    elif col == 2:
                        detail['is_new_client'] = get_text(row_data[col])
                    col = col+1
                if len(detail) != 0:
                    confidential_information["confidential_clients_details"].append(
                        detail)
            row = row+1
    elif len(data[0]) >= 1 and len(data[0][0]) >= 1 and (("Confidential Work Highlights" in data[0][0][0] and "Confidential Matter" in data[1][0][0]) or ("Confidential Matter" in data[0][0][0])):
        detail = {}
        row = 0
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" not in get_text(row_data[0]):
                if "Name of client" in get_text(row_data[0]):
                    detail['name'] = get_text(data[row+1][0])
                elif "Summary of matter and your department" in get_text(row_data[0]):
                    detail['summary'] = get_text(data[row+1][0])
                elif "Matter value" in get_text(row_data[0]):
                    detail['matter_value'] = get_text(data[row+1][0])
                elif "Is this a cross-border matter" in get_text(row_data[0]):
                    detail['is_cross_border_metter'] = get_text(data[row+1][0])
                elif "Lead partner" in get_text(row_data[0]):
                    detail['lead_partner'] = get_text(data[row+1][0])
                elif "Other team members" in get_text(row_data[0]):
                    detail['other_team_members'] = get_text(data[row+1][0])
                elif "Other firms advising on the matter" in get_text(row_data[0]):
                    detail['other_firms_advising'] = get_text(data[row+1][0])
                elif "Date of completion or current status" in get_text(row_data[0]):
                    detail['date_of_completion'] = get_text(data[row+1][0])
                elif "Other information about this matter" in get_text(row_data[0]):
                    detail['other_information'] = get_text(data[row+1][0])
            row = row+1
        if len(detail) > 0:
            confidential_information["confidential_matters"].append(detail)


def get_text(data):
    index = 0
    final_text = ''
    while index < len(data):
        final_text += data[index]
        index = index + 1
    return final_text


if __name__ == "__main__":
    # result = docx2python('3362805.docx')
    # parsing(result)
    if os.path.exists("data.db") == False:
        create()

    # result = docx2python('BlockDestination.docx')
    # parsing(result)
    # new_id = insert_submission_data(
    #     "blob_string", "blob_string", "blob_string")
    # save_data(new_id)
    azure()
    # insert_Data("a", 's', 'f')
    # result = get_Data()

    # for row in result:
    #     print(row)
