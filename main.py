import os
import subprocess
import re
from db import create_database, insert_submission_data, insert_preliminary_information, insert_department_information, insert_feedback, insert_publishable_information, insert_confidential_information, check_db
from docx2python import docx2python
from azure.storage.blob import ContainerClient

preliminary_information = {}
department_information = {}
feedback = {}
publishable_information = {'publishable_matters': []}
confidential_information = {'confidential_matters': []}
connection_string = "DefaultEndpointsProtocol=https;AccountName=sthistoricalsubmissions;AccountKey=5OlZ+H0GndSzvBf13VfUTXAfdQOKJ1lsWBcp+h8Zst17ks44aBu1skOdOLUOlTisdMy7hEQlwyjzvjpSOeFxfw==;EndpointSuffix=core.windows.net"
container_name = "submissions"


def azure():
    global connection_string, container_name
    # Get blobs from container of submissions
    container = ContainerClient.from_connection_string(
        connection_string, container_name=container_name)
    # Get list of the blob
    blob_list = container.list_blobs()
    # parsing of all the blobs
    for blob in blob_list:
        print(blob.name + '\n')
        if ".DOC" in blob.name.upper():
            # get blob string and split it into its subsections
            blob_string = blob.name.split('/')
            # check if it exists in Database before
            id = check_db(
                blob_string[0], blob_string[1], blob_string[2].split('.')[0])
            # If not existed in database
            if id is None:
                # Download blob data
                blob_data = container.download_blob(blob)

                if os.path.exists("files/BlockDestination.docx"):
                    os.remove("files/BlockDestination.docx")

                # convert to .docx if file in old word file .doc
                if not ".DOCX" in blob_string[2].upper():
                    if os.path.exists("files/BlockDestination.doc"):
                        os.remove("files/BlockDestination.doc")

                    with open("./files/BlockDestination.doc", "wb") as my_blob:
                        blob_data.readinto(my_blob)
                    subprocess.call(
                        ['soffice', '--headless', '--convert-to', 'docx', "files/BlockDestination.doc", "--outdir", "./files/"])
                else:
                    with open("./files/BlockDestination.docx", "wb") as my_blob:
                        blob_data.readinto(my_blob)
                result = None
                try:
                    result = docx2python('files/BlockDestination.docx')
                except:
                    pass
                if result:
                    parsing(result)
                    new_id = insert_submission_data(
                        blob_string[0], blob_string[1], blob_string[2].split('.')[0])
                    save_data_into_db(new_id)




def save_data_into_db(id):
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


def extract_single_value(data, key):
    if len(data[0]) == 1 and len(data[0][0]) == 1 and key in data[0][0][0]:
        return data[1][0]
    else:
        return ''


def get_preliminary_information(data):
    global preliminary_information
    # preliminary_information["firm_name"] = get_text(extract_single_value(data, "Firm name"))
    # preliminary_information["practice_area"] = get_text(extract_single_value(data, "Practice Area"))
    # preliminary_information["location"] = get_text(extract_single_value(data, "Location"))

    if len(data[0]) == 1 and len(data[0][0]) == 1 and "Firm name" in data[0][0][0]:
        preliminary_information["firm_name"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Practice Area" in data[0][0][0]:
        preliminary_information["practice_area"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Location" in data[0][0][0]:
        preliminary_information["location"] = get_text(data[1][0])
    if len(data[0]) == 1 and len(data[0][0]) == 1 and "Contact person" in data[0][0][0]:
        preliminary_information["contact_person_details"] = []
        row = 2
        while row < len(data):
            row_data = data[row]
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        detail['name'] = "\n".join(row_data[col])
                    elif col == 1:
                        if "mailto" in get_text(row_data[col]):
                            result = re.search('mailto:(.*)">', get_text(row_data[col]))
                            if result:
                                detail['email'] = result.group(1)
                        else:
                            detail['email'] = get_text(row_data[col])
                    elif col == 2:
                        phone = get_text(row_data[col]).replace(" ", "").replace(
                            "(", "").replace(")", "").replace("-", "")
                        # if len(phone) > 0 and phone[0] != '+':
                        #     detail['phone'] = '+' + phone
                        # else:
                        detail['phone'] = phone
                    col = col+1
                if len(detail) != 0:
                    preliminary_information["contact_person_details"].append(
                        detail)
            row = row+1


def get_department_information(data):
    global department_information
    # department_information["department_name"] =get_text(extract_single_value(data, "Department name"))
    # number_of_partners_data = get_text(extract_single_value(data, "Number of partners"))
    # if len(number_of_partners_data) > 2:
    #     department_information["number_of_partners"] = len(number_of_partners_data) -1
    # else:
    #     department_information["number_of_partners"] = get_text(number_of_partners_data)
    # 
    # qualified_lawyers_data = get_text(extract_single_value(data, "qualified lawyers"))
    # if len(qualified_lawyers_data) > 2:
    #     department_information["qualified_lawyers"] = len(qualified_lawyers_data) - 1
    # else:
    #     department_information["qualified_lawyers"] = get_text(qualified_lawyers_data)
    
    



    if len(data[0]) == 1 and len(data[0][0]) == 1 and "Department name" in data[0][0][0]:
        department_information["department_name"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "Number of partners" in data[0][0][0]:
        if len(data[1][0]) > 2:
            department_information["number_of_partners"] = len(data[1][0]) - 1
        else:
            department_information["number_of_partners"] = get_text(data[1][0])
    elif len(data[0]) == 1 and len(data[0][0]) == 1 and "qualified lawyers" in data[0][0][0]:
        if len(data[1][0]) > 2:
            department_information["qualified_lawyers"] = len(data[1][0]) - 1
        else:
            department_information["qualified_lawyers"] = get_text(data[1][0])
    elif len(data[0]) >= 1 and len(data[0][0]) >= 1 and "Foreign Desks" in data[0][0][0]:
        length = 0
        while(length< len(data)):
            if "department best known" in get_text(data[length][0]):
                if length+1 < len(data):
                    extracted_data = "\n".join(data[length + 1][0]).replace("--", "\u2022").replace("\t", "")
                    department_information["department_best_known"] = extracted_data
                    break;
            length = length + 1
    elif len(data[0]) >= 1 and len(data[0][0]) >= 1 and "department best known" in data[0][0][0]:
        if len(data[1][0]) > 2:
            extracted_data = "\n".join(data[1][0]).replace("--", "\u2022").replace("\t", "")
            department_information["department_best_known"] = extracted_data
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
                        if "mailto" in get_text(row_data[col]):
                            result = re.search('mailto:(.*)">', get_text(row_data[col]))
                            if result:
                                detail['name'] = result.group(1)
                        else:
                            detail['name'] = "\n".join(row_data[col])
                    elif col == 1:
                        if "mailto" in get_text(row_data[col]):
                            result = re.search('mailto:(.*)">', get_text(row_data[col]))
                            if result:
                                detail['email'] = result.group(1)
                        else:
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
                        detail['name'] = "\n".join(row_data[col])
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
                        if "href" in get_text(row_data[col]):
                            result = re.search('">(.*)</', get_text(row_data[col]))
                            if result:
                                detail['name'] = result.group(1).replace(" ", "")
                        else:
                            detail['name'] = "\n".join(row_data[col]).replace(" ", "")
                    elif col == 1:
                        detail['comments'] = "\n".join(row_data[col]).replace("--","\u2022").replace("  ", " ").\
                            replace("\t", "")
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
                        if "href" in get_text(row_data[col]):
                            result = re.search('">(.*)</', get_text(row_data[col]))
                            if result:
                                detail['name'] = result.group(1).replace(" ", "")
                        else:
                            detail['name'] = "\n".join(row_data[col]).replace(" ", "")
                    elif col == 1:
                        detail['comments'] = "\n".join(row_data[col]).replace("--", "\u2022").replace("  ", " "). \
                            replace("\t", "")
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
        feedback["previous_coverage_department_feedback"] = "\n".join(data[1][0]).replace("\t","").replace("  "," ").replace("\n\n", "").replace("--", "\u2022")


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
        while row < len(data)- 1:
            row_data = data[row]
            if len(row_data) > 0 and len(row_data) > 0 and len(get_text(row_data[0])) > 0 and "N/A" not in get_text(row_data[0]) and len(data[row+1]) > 0:
                if "Name of client" in get_text(row_data[0]):
                    detail['name'] = get_text(data[row+1][0])
                elif "Summary of matter and your department" in get_text(row_data[0]):
                    extracted_data = "\n".join(data[row+1][0]).replace("--", "\u2022").replace("\t", "").replace(" ", "")
                    detail['summary'] = extracted_data
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
                    detail['other_information'] = "\n".join(data[row+1][0])
            row = row+1
        if len(detail) > 0 and 'name' in detail and len(detail['name']) > 0:
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
        while row < len(data) - 1:
            row_data = data[row]
            if len(row_data) > 0 and len(get_text(row_data[0])) > 0 and "N/A" not in get_text(row_data[0]) and len(data[row+1]) > 0:
                if "Name of client" in get_text(row_data[0]):
                    detail['name'] = get_text(data[row+1][0])
                elif "Summary of matter and your department" in get_text(row_data[0]):
                    extracted_data = "\n".join(data[row + 1][0]).replace("--", "\u2022").replace("\t", "").replace(" ", "")
                    detail['summary'] = extracted_data
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
                    detail['other_information'] = "\n".join(data[row+1][0])
            row = row+1
        if len(detail) > 0 and 'name' in detail and len(detail['name']) > 0:
            confidential_information["confidential_matters"].append(detail)


def get_text(data):
    index = 0
    final_text = ''
    while index < len(data):
        final_text += data[index]
        index = index + 1
    return final_text


if __name__ == "__main__":
    # import subprocess

    # subprocess.call(
    #     ['soffice', '--headless', '--convert-to', 'docx', "3167883.doc"])
    # result = docx2python('3169276.DOCX')
    # import pdb
    # pdb.set_trace()
    # print(result)
    create_database()
    # result = docx2python('3161842.docx')
    # parsing(result)
    # new_id = insert_submission_data(
    #     '335', '489302', '3161842')
    # save_data(new_id)
    azure()
    #result = docx2python('3169190.docx')
    #parsing(result)
