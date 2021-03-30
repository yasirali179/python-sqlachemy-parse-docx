import os
from db import create, insert_submission_data, insert_preliminary_information, insert_department_information, insert_feedback, insert_publishable_information, insert_confidential_information
from docx2python import docx2python
from azure.storage.blob import ContainerClient


def azure():
    connection_string = "DefaultEndpointsProtocol=https;AccountName=sthistoricalsubmissions;AccountKey=5OlZ+H0GndSzvBf13VfUTXAfdQOKJ1lsWBcp+h8Zst17ks44aBu1skOdOLUOlTisdMy7hEQlwyjzvjpSOeFxfw==;EndpointSuffix=core.windows.net"
    container = ContainerClient.from_connection_string(
        connection_string, container_name="submissions")
    blob_list = container.list_blobs()

    for blob in blob_list:
        if ".docx" in blob.name:
            print(blob.name + '\n')
            blob_string = blob.name.split('/')
            id = insert_submission_data(
                blob_string[0], blob_string[1], blob_string[2].split('.')[0])
            if id is not None:
                blob_data = container.download_blob(blob)
                if os.path.exists("BlockDestination.docx"):
                    os.remove("BlockDestination.docx")
                with open("./BlockDestination.docx", "wb") as my_blob:
                    blob_data.readinto(my_blob)
                result = docx2python('BlockDestination.docx')
                parsed_data = parsing(result)
                save_data(id, parsed_data)
            break


def save_data(id, parsed_data):
    insert_preliminary_information(
        int(id), parsed_data['preliminary_information'])
    insert_department_information(
        int(id), parsed_data['preliminary_information'])
    insert_feedback(int(id), parsed_data['preliminary_information'])
    insert_publishable_information(
        int(id), parsed_data['preliminary_information'])
    insert_confidential_information(
    int(id), parsed_data['confidential_information'])
    


def parsing(result):
    i = 0
    parsed_data = {}
    preliminary_information = {}
    department_information = {}
    feedback = {}
    publishable_information = {}
    confidential_information = {}

    while i < len(result.body):
        if len(result.body[i]) >= 2:
            data = result.body[i]
            preliminary_information.update(get_preliminary_information(data))
            department_information.update(get_department_information(data))
            feedback.update(get_feedback(data))
            publishable_information.update(get_publishable_information(data))
            confidential_information.update(get_confidential_information(data))
        i = i+1
    parsed_data['preliminary_information'] = preliminary_information
    parsed_data['department_information'] = department_information
    parsed_data['feedback'] = feedback
    parsed_data['publishable_information'] = publishable_information
    parsed_data['confidential_information'] = confidential_information

    return parsed_data


def get_preliminary_information(data):
    parsed_data = {}
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "Firm name" in data[0][0][0]:
        parsed_data["frim_name"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Practice Area" in data[0][0][0]:
        parsed_data["practice_area"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Location" in data[0][0][0]:
        parsed_data["localtion"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Contact person" in data[0][0][0]:
        parsed_data["contact_person_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        detail['name'] = get_text(row_data[col])
                    elif col == 1:
                        detail['email'] = get_text(row_data[col])
                    elif col == 2:
                        detail['phone'] = get_text(row_data[col])
                    col = col+1
                if len(detail) != 0:
                    parsed_data["contact_person_details"].append(detail)
            row = row+1
    return parsed_data


def get_department_information(data):
    parsed_data = {}
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "Department name" in data[0][0][0]:
        parsed_data["department_name"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Number of partners" in data[0][0][0]:
        parsed_data["number_of_partners"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "qualified lawyers" in data[0][0][0]:
        parsed_data["qualified_lawyers"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Heads of department" in data[0][0][0]:
        parsed_data["heads_of_department_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        detail['name'] = get_text(row_data[col])
                    elif col == 1:
                        detail['email'] = get_text(row_data[col])
                    elif col == 2:
                        detail['phone'] = get_text(row_data[col])
                    col = col+1
                if len(detail) != 0:
                    parsed_data["heads_of_department_details"].append(detail)
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Hires" in data[0][0][0]:
        parsed_data["hires_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
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
                    parsed_data["hires_details"].append(detail)
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Information regarding lawyers (including associates) RANKED" in data[0][0][0]:
        parsed_data["ranked_lawyers_details"] = []
        row = 2
        while row < len(data):

            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
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
                    parsed_data["ranked_lawyers_details"].append(detail)
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Information regarding UNRANKED lawyers" in data[0][0][0]:
        parsed_data["unranked_lawyers_details"] = []
        row = 2
        while row < len(data):

            row_data = data[row]
            if len(get_text(row_data[0])) > 0:
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
                    parsed_data["unranked_lawyers_details"].append(detail)
            row = row+1
    return parsed_data


def get_feedback(data):
    parsed_data = {}
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "barristers / advocates in the UK, Australia, Hong Kong, India, Malaysia, New Zealand or Sri Lanka" in data[0][0][0]:
        parsed_data["barristers_advocates_selected_country_details"] = []
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
                    parsed_data["barristers_advocates_selected_country_details"].append(
                        detail)
            row = row+1
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Feedback on our previous coverage of your department" in data[0][0][0]:
        parsed_data["previous_coverage_department_feedback"] = get_text(
            data[1][0])
    return parsed_data


def get_publishable_information(data):
    parsed_data = {}
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "List of this department's PUBLISHABLE clients" in data[0][0][0]:
        parsed_data["publishable_clients_details"] = []
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
                if len(detail) != 0:
                    parsed_data["publishable_clients_details"].append(detail)
            row = row+1
    elif len(data[0]) >= 1 and len(data[0][0]) >= 1 and (("Publishable Work Highlights in last 12 months" in data[0][0][0] and "Publishable Matter" in data[1][0][0]) or ("Publishable Matter" in data[0][0][0])):
        row = 2
        parsed_data["publishable_matters"] = []
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
        if len(detail) != 0:
            parsed_data["publishable_matters"].append(detail)
    return parsed_data


def get_confidential_information(data):
    parsed_data = {}
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "List of this department's CONFIDENTIAL clients" in data[0][0][0]:
        parsed_data["confidential_clients_details"] = []
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
                    parsed_data["confidential_clients_details"].append(detail)
            row = row+1
    elif len(data[0]) >= 1 and len(data[0][0]) >= 1 and (("Confidential Work Highlights" in data[0][0][0] and "Publishable Matter" in data[1][0][0]) or ("Confidential Matter" in data[0][0][0])):
        parsed_data["confidential_matters"] = []
        detail = {}
        row = 2
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
    return parsed_data


def get_text(data):
    index = 0
    final_text = ''
    while index < len(data):
        final_text += data[index]
        index = index + 1
    return final_text


if __name__ == "__main__":
    #result = docx2python('3362805.docx')
    # parsing(result)
    if os.path.exists("data.db") == False:
        create()
    azure()
    # insert_Data("a", 's', 'f')
    # result = get_Data()

    # for row in result:
    #     print(row)
