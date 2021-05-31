import os
import re
import subprocess
from azure.storage.blob import ContainerClient
from db import create_database, insert_submission_data, insert_preliminary_information, insert_department_information, \
    insert_feedback, insert_publishable_information, insert_confidential_information, check_db
from docx2python import docx2python
from utils import get_text, match_substring_recursive, find_index_sub_string, subarray_exist

preliminary_information = {}
department_information = {}
feedback = {}
publishable_information = {'publishable_matters': []}
confidential_information = {'confidential_matters': []}
connection_string = "DefaultEndpointsProtocol=https;AccountName=sthistoricalsubmissions;AccountKey=5OlZ+H" \
                    "0GndSzvBf13VfUTXAfdQOKJ1lsWBcp+h8Zst17ks44aBu1skOdOLUOlTisdMy7hEQlwyjzvjpSOeFxfw==;" \
                    "EndpointSuffix=core.windows.net"
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
                # Check if previous file exists for prevention of overwrite
                if os.path.exists("files/BlockDestination.docx"):
                    os.remove("files/BlockDestination.docx")

                # convert to .docx if file in old word file .doc
                if ".DOCX" not in blob_string[2].upper():
                    if os.path.exists("files/BlockDestination.doc"):
                        os.remove("files/BlockDestination.doc")
                    # save .doc downloaded file
                    with open("./files/BlockDestination.doc", "wb") as my_blob:
                        blob_data.readinto(my_blob)
                    # convert old .doc into .docx for parsing
                    subprocess.call(
                        ['soffice', '--headless', '--convert-to', 'docx', "files/BlockDestination.doc", "--outdir",
                         "./files/"])
                else:
                    # Save .docx file for parsing
                    with open("./files/BlockDestination.docx", "wb") as my_blob:
                        blob_data.readinto(my_blob)
                result = None
                try:
                    # Parse the file and return parsed data
                    result = docx2python('files/BlockDestination.docx')
                    # Check if successfully parsed the data
                    if result:
                        # extract the relevant data from parsed result
                        parsing(result)
                        # store the parsed data into Database
                        new_id = insert_submission_data(
                            blob_string[0], blob_string[1], blob_string[2].split('.')[0])
                        save_data_into_db(new_id)
                except:
                    pass


def save_data_into_db(id):
    # get global variables which have parsed data
    global preliminary_information, department_information, feedback, publishable_information, confidential_information

    # insert preliminary information into database
    insert_preliminary_information(
        int(id), preliminary_information)

    # insert department information into database
    insert_department_information(
        int(id), department_information)

    # insert feedback into database
    insert_feedback(int(id), feedback)

    # insert publishable information into database
    insert_publishable_information(
        int(id), publishable_information)

    # insert confidential information into database
    insert_confidential_information(
        int(id), confidential_information)

    # Reinitialized for next parsing
    preliminary_information = {}
    department_information = {}
    feedback = {}
    publishable_information = {'publishable_matters': []}
    confidential_information = {'confidential_matters': []}


def parsing(result):
    """ This function takes the parsed object and extract the all the
        relevant information from the object and store it into global
        variables

        input: parsed object
        return: nothing
        """
    i = 0
    # external loop for checking each object in the parsed object list
    while i < len(result.body):
        # check if parsed object list is valid
        if len(result.body[i]) >= 2:
            # get body data
            data = result.body[i]
            # extract preliminary information and store into global variables
            get_preliminary_information(data)

            # extract department information and store into global variables
            get_department_information(data)

            # extract feedback and store into global variables
            get_feedback(data)

            # extract publishable information and store into global variables
            get_publishable_information(data)

            # extract confidential information and store into global variables
            get_confidential_information(data)
        i = i + 1


def get_preliminary_information(data):
    """ This function takes the parsed object and extract the relevant
        preliminary information from the object and store it into global
        preliminary_information variable

        input: parsed object
        return: nothing
        """

    global preliminary_information
    # check if object contain "Firm name" keyword if exists store its value into preliminary_information object
    if match_substring_recursive("Firm name", data) and subarray_exist(data, [1, 0]):
        preliminary_information["firm_name"] = get_text(data[1][0])

    # check if object contain "Practice Area" keyword if exists store its value into preliminary_information object
    elif match_substring_recursive("Practice Area", data) and subarray_exist(data, [1, 0]):
        preliminary_information["practice_area"] = get_text(data[1][0])

    # check if object contain "A3 Location" or "Guide & location" keyword if exists store its value into
    # preliminary_information object
    elif (match_substring_recursive("A3 Location", data) or match_substring_recursive("Guide & location",
                                                                                      data)) and subarray_exist(data,
                                                                                                                [1, 0]):
        preliminary_information["location"] = get_text(data[1][0])

    # check if object contain "Contact person" keyword
    if match_substring_recursive("Contact person", data) and subarray_exist(data, [2]):
        preliminary_information["contact_person_details"] = []
        row = 2
        # extract the "Contact person" store its value into preliminary_information object
        while row < len(data):
            row_data = data[row]
            # check if array is not empty or contain n/a value
            if subarray_exist(data, [0]) and len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        # check if name value have href string if exists remove the href form it
                        if match_substring_recursive("href", row_data[col]):
                            result = re.search('">(.*)</a>', get_text(row_data[col]))
                            if result:
                                detail['name'] = result.group(1)

                        else:
                            detail['name'] = "\n".join(row_data[col])
                    elif col == 1:
                        # check if email value have mailto string if exists remove the mailto form it
                        if match_substring_recursive("mailto", row_data[col]):
                            result = re.search('mailto:(.*)">', get_text(row_data[col]))
                            if result:
                                detail['email'] = result.group(1)
                        else:
                            detail['email'] = get_text(row_data[col])
                    elif col == 2:
                        # extract phone number of "Contact person" and remove irrelevant information
                        phone = get_text(row_data[col]).replace(" ", "").replace(
                            "(", "").replace(")", "").replace("-", "")
                        detail['phone'] = phone
                    col = col + 1
                # check if "Contact person" detail is not empty
                if len(detail) != 0:
                    # append single Contact into preliminary information object
                    preliminary_information["contact_person_details"].append(
                        detail)
            row = row + 1


def get_department_information(data):
    """ This function takes the parsed object and extract the relevant
        department information from the object and store it into global
        department_information variable

        input: parsed object
        return: nothing
        """

    global department_information
    # check if object contain "Department name" keyword if exists store its value into department_information object
    if match_substring_recursive("Department name", data) and subarray_exist(data, [1, 0]):
        department_information["department_name"] = get_text(data[1][0])
    # check if object contain "Number of partners" keyword if exists store its value into department_information object
    if match_substring_recursive("Number of partners", data) and subarray_exist(data, [1, 0]):
        # if name exists then count number of partners
        if len(data[1][0]) > 2:
            department_information["number_of_partners"] = len(data[1][0]) - 1
        else:
            department_information["number_of_partners"] = get_text(data[1][0])
    # check if object contain "qualified lawyers" keyword if exists store its value into department_information object
    if match_substring_recursive("qualified lawyers", data) and subarray_exist(data, [1, 0]):
        # if name exists then count number of qualified lawyers
        if len(data[1][0]) > 2:
            department_information["qualified_lawyers"] = len(data[1][0]) - 1
        else:
            department_information["qualified_lawyers"] = get_text(data[1][0])
    # check if object contain "Foreign Desks" and "department best known" keyword if exists store its value into
    # department_information object
    if match_substring_recursive("Foreign Desks", data) and match_substring_recursive("department best known", data):
        length = 0
        # loop to check each object
        while length < len(data):
            # check if "department best known" keyword exists in the array
            if "department best known" in get_text(data[length][0]):
                # extract the parsed value
                if length + 1 < len(data):
                    extracted_data = "\n".join(data[length + 1][0]).replace("--", "\u2022").replace("\t", "")
                    department_information["department_best_known"] = extracted_data
                    break
            length = length + 1
    # check if object contain "department best known" keyword if exists store its value into department_information
    # object
    # check if "department best known" keyword exists in the array
    if match_substring_recursive("department best known", data) and subarray_exist(data, [1, 0]):
        if len(data[1][0]) > 2:
            # extract the parsed value
            extracted_data = "\n".join(data[1][0]).replace("--", "\u2022").replace("\t", "")
            department_information["department_best_known"] = extracted_data

    # check if object contain "Heads of department" keyword if exists store its value into department_information object
    if match_substring_recursive("Heads of department", data):
        department_information["heads_of_department_details"] = []
        # move the array to two index to get table values
        row = 2 + find_index_sub_string("Heads of department", data)[0]
        # loop to extract "Heads of department" table values
        while row < len(data):
            row_data = data[row]
            # check if table reached to end
            if len(row_data) == 1:
                break
            # check if table is empty or contained n/a value
            if subarray_exist(row_data, [0]) and len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                # loop to extract table data
                while col < len(row_data):
                    # extract name of Head of department from first column of table
                    if col == 0:
                        # check if html code exists
                        if match_substring_recursive("mailto", row_data[col]):
                            # remove html part
                            result = re.search('mailto:(.*)">', get_text(row_data[col]))
                            if result:
                                detail['name'] = result.group(1)
                        # check if html code of href exists
                        elif match_substring_recursive("href", row_data[col]):
                            # remove html part
                            result = re.search('">(.*)</a>', get_text(row_data[col]))
                            if result:
                                detail['name'] = result.group(1)
                        else:
                            detail['name'] = "\n".join(row_data[col])
                    # extract email of Head of department from second column of table
                    elif col == 1:
                        # check if html code exists
                        if "mailto" in get_text(row_data[col]):
                            # remove html part
                            result = re.search('mailto:(.*)">', get_text(row_data[col]))
                            if result:
                                detail['email'] = result.group(1)
                        else:
                            detail['email'] = get_text(row_data[col])
                    # extract phone of Head of department from third column of table
                    elif col == 2:
                        # extract phone detail
                        phone = get_text(row_data[col]).replace(" ", "").replace(
                            "(", "").replace(")", "").replace("-", "")
                        detail['phone'] = phone
                    col = col + 1
                # check if extracted value object contain data
                if len(detail) != 0:
                    department_information["heads_of_department_details"].append(
                        detail)
            row = row + 1
    # check if object contain "Hires" and "Joined / Departed" keyword if exists store its value into
    # department_information object
    if match_substring_recursive("Hires", data) and match_substring_recursive("Joined / Departed", data):
        department_information["hires_details"] = []
        # move the array to two index to get table values
        row = 2 + find_index_sub_string("Hires", data)[0]
        # loop to extract "Hires" table values
        while row < len(data):
            row_data = data[row]
            # check if table reached to end
            if len(row_data) == 1:
                break
            # check if table is empty or contained n/a value
            if subarray_exist(row_data, [0]) and len(get_text(row_data[0]).replace(" ", "")) > 0 and "N/A" != get_text(
                    row_data[0]).upper():
                col = 0
                detail = {}
                # loop to extract table data
                while col < len(row_data):
                    # extract name from first column of table
                    if col == 0:
                        detail['name'] = "\n".join(row_data[col])
                    # extract joined from second column of table
                    elif col == 1:
                        detail['joined'] = get_text(row_data[col])
                    # extract joined_from from third column of table
                    elif col == 2:
                        detail['joined_from'] = get_text(row_data[col])
                    col = col + 1
                # check if extracted value object contain data
                if len(detail) != 0:
                    department_information["hires_details"].append(detail)
            row = row + 1
    # check if object contain "Information regarding lawyers (including associates) RANKED" and "Partner Y/N" keyword
    # if exists store its value into department_information object
    if match_substring_recursive("Information regarding lawyers (including associates) RANKED",
                                 data) and match_substring_recursive("Partner Y/N", data):
        department_information["ranked_lawyers_details"] = []
        # move the array to two index to get table values
        row = 2 + find_index_sub_string("Information regarding lawyers (including associates) RANKED", data)[0]
        # loop to extract "ranked_lawyers_details" table values
        while row < len(data):
            row_data = data[row]
            # check if table reached to end
            if len(row_data) == 1:
                break
            # check if table is empty or contained n/a value
            if subarray_exist(row_data, [0]) and len(get_text(row_data[0])) > 0 and "N/A" != get_text(
                    row_data[0]).upper():
                col = 0
                detail = {}
                # loop to extract table data
                while col < len(row_data):
                    # extract name from first column of table
                    if col == 0:
                        # check if value contain html part
                        if "href" in get_text(row_data[col]):
                            # remove html part
                            result = re.search('">(.*)</', get_text(row_data[col]))
                            if result:
                                detail['name'] = result.group(1).replace(" ", "")
                        else:
                            detail['name'] = "\n".join(row_data[col]).replace(" ", "")
                    # extract comments from second column of table
                    elif col == 1:
                        detail['comments'] = "\n".join(row_data[col]).replace("--", "\u2022").replace("  ", " "). \
                            replace("\t", "").replace(" ", "")
                    # extract is_partner detail from third column of table
                    elif col == 2:
                        detail['is_partner'] = get_text(row_data[col])
                    col = col + 1
                # check if extracted value object contain data
                if len(detail) != 0:
                    department_information["ranked_lawyers_details"].append(
                        detail)
            row = row + 1

    # check if object contain "Information regarding UNRANKED lawyers" and "Partner Y/N" keyword if exists store its
    # value into department_information object
    if match_substring_recursive("Information regarding UNRANKED lawyers", data):
        department_information["unranked_lawyers_details"] = []
        # move the array to two index to get table values
        row = 2 + find_index_sub_string("B7 Information regarding UNRANKED lawyers", data)[0]
        # loop to extract "UNRANKED lawyers" table values
        while row < len(data):
            row_data = data[row]
            # check if table reached to end
            if len(row_data) == 1:
                break
            # check if table is empty or contained n/a value
            if subarray_exist(row_data, [0]) and len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    # extract name from first column of table
                    if col == 0:
                        # check if value contain html part
                        if "href" in get_text(row_data[col]):
                            # remove html part
                            result = re.search('">(.*)</', get_text(row_data[col]))
                            if result:
                                detail['name'] = result.group(1).replace(" ", "")
                        else:
                            detail['name'] = "\n".join(row_data[col]).replace(" ", "")
                    # extract comments from second column of table
                    elif col == 1:
                        detail['comments'] = "\n".join(row_data[col]).replace("--", "\u2022").replace("  ", " "). \
                            replace("\t", "")
                    # extract is_partner from third column of table
                    elif col == 2:
                        detail['is_partner'] = get_text(row_data[col])
                    col = col + 1
                # check if extracted value object contain data
                if len(detail) != 0:
                    department_information["unranked_lawyers_details"].append(
                        detail)
            row = row + 1


def get_feedback(data):
    """ This function takes the parsed object and extract the relevant
        feedback information from the object and store it into global
        feedback variable

        input: parsed object
        return: nothing
        """

    global feedback
    # check if object contain "barristers / advocates in the UK, Australia" matching string
    if match_substring_recursive(
            "barristers / advocates in the UK, Australia, Hong Kong, India, Malaysia, New Zealand or Sri Lanka", data):
        feedback["barristers_advocates_selected_country_details"] = []
        row = 2
        # loop to get the relevant details from the array list
        while row < len(data):
            row_data = data[row]
            # check if array is not empty or contain n/a value
            if len(get_text(row_data[0])) > 0 and "N/A" != get_text(row_data[0]):
                col = 0
                detail = {}
                while col < len(row_data):
                    if col == 0:
                        # get name
                        detail['name'] = get_text(row_data[col])
                    elif col == 1:
                        # get firm
                        detail['firm'] = get_text(row_data[col])
                    elif col == 2:
                        # get comments
                        detail['comments'] = get_text(row_data[col])
                    col = col + 1
                # check if extracted detail object not empty
                if len(detail) != 0:
                    feedback["barristers_advocates_selected_country_details"].append(
                        detail)
            row = row + 1
    # check if object contain "Feedback on our previous coverage of your department" matching string
    elif match_substring_recursive("Feedback on our previous coverage of your department", data):
        # check if value exist
        if subarray_exist(data, [1, 0]):
            # filter the irrelevant information and store it into relevant global variable
            data = "\n".join(data[1][0]).replace("\t", "").replace("  ", " ").replace("\n\n", ""). \
                replace("--", "\u2022")
            # check if extracted information is not empty
            if len(data) > 0:
                feedback["previous_coverage_department_feedback"] = data


def get_publishable_information(data):
    """ This function takes the parsed object and extract the relevant
        publishable information from the object and store it into global
        publishable_information variable

        input: parsed object
        return: nothing
        """

    global publishable_information
    # check if object contain "List of this department's PUBLISHABLE clients" matching string
    if match_substring_recursive("List of this department's PUBLISHABLE clients", data):
        publishable_information["publishable_clients_details"] = []
        row = 2
        # loop to get the relevant details from the array list
        while row < len(data):
            row_data = data[row]
            # check if array is not empty or contain n/a value
            if subarray_exist(row_data, [1]) and subarray_exist(row_data, [1]) and len(
                    get_text(row_data[1]).replace(" ", "")) > 0 and "N/A" != get_text(row_data[0]).upper():
                col = 1
                detail = {}
                while col < len(row_data):
                    if col == 1:
                        # extract name and store it into global variable
                        detail['name'] = get_text(row_data[col])
                    elif col == 2:
                        # extract data if is_new_client and store it into global variable
                        detail['is_new_client'] = get_text(row_data[col])
                    col = col + 1
                # check if extracted information in detail variable is not empty
                if len(detail) > 0:
                    publishable_information["publishable_clients_details"].append(
                        detail)
            row = row + 1

    # check if object contain "Publishable Matter" and "Publishable Work Highlights in last 12 months" matching string
    elif match_substring_recursive("Publishable Matter", data) or match_substring_recursive(
            "Publishable Work Highlights in last 12 months", data):
        row = 0
        detail = {}
        # loop to get the Publishable Matter details from the array list
        while row < len(data) - 1:
            row_data = data[row]
            # check if array not contain n/a value
            if not match_substring_recursive("N/A", row_data):
                # check if array values contain "Name of client" matching string
                if match_substring_recursive("Name of client", row_data) and subarray_exist(data, [row + 1, 0]):
                    detail['name'] = get_text(data[row + 1][0])
                # check if array values contain "Summary of matter and your department" matching string
                elif match_substring_recursive("Summary of matter and your department", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    extracted_data = "\n".join(data[row + 1][0]).replace("--", "\u2022").replace("\t", ""). \
                        replace(" ", "")
                    detail['summary'] = extracted_data
                # check if array values contain "Matter value" matching string
                elif match_substring_recursive("Matter value", row_data) and subarray_exist(data, [row + 1, 0]):
                    detail['matter_value'] = get_text(data[row + 1][0])
                # check if array values contain "Is this a cross-border matter" matching string
                elif match_substring_recursive("Is this a cross-border matter", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    detail['is_cross_border_matter'] = get_text(data[row + 1][0])
                # check if array values contain "Lead partner" matching string
                elif match_substring_recursive("Lead partner", row_data) and subarray_exist(data, [row + 1, 0]):
                    detail['lead_partner'] = get_text(data[row + 1][0])
                # check if array values contain "Other team members" matching string
                elif match_substring_recursive("Other team members", row_data) and subarray_exist(data, [row + 1, 0]):
                    detail['other_team_members'] = get_text(data[row + 1][0])
                # check if array values contain "Other firms advising on the matter" matching string
                elif match_substring_recursive("Other firms advising on the matter", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    detail['other_firms_advising'] = get_text(data[row + 1][0])
                # check if array values contain "Date of completion or current status" matching string
                elif match_substring_recursive("Date of completion or current status", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    detail['date_of_completion'] = get_text(data[row + 1][0])
                # check if array values contain "Other information about this matter" matching string
                elif match_substring_recursive("Other information about this matter", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    detail['other_information'] = "\n".join(data[row + 1][0])
            row = row + 1
        # check if array values contain "Name of client" matching string
        if len(detail) > 0 and 'name' in detail and len(detail['name']) > 0:
            publishable_information["publishable_matters"].append(detail)


def get_confidential_information(data):
    """ This function takes the parsed object and extract the relevant
        confidential information from the object and store it into global
        confidential_information variable

        input: parsed object
        return: nothing
        """

    global confidential_information
    # check if object contain "List of this department's CONFIDENTIAL clients" matching string
    if match_substring_recursive("List of this department's CONFIDENTIAL clients", data):
        confidential_information["confidential_clients_details"] = []
        row = 2
        # loop to get the relevant details from the array list
        while row < len(data):
            row_data = data[row]
            # check if array is not empty or contain n/a value
            if subarray_exist(row_data, [1]) and subarray_exist(row_data, [1]) and len(
                    get_text(row_data[1]).replace(" ", "")) > 0 and "N/A" != get_text(row_data[0]).upper():
                detail = {}
                col = 1
                while col < len(row_data):
                    # extract name and store it into global variable
                    if col == 1:
                        detail['name'] = get_text(row_data[col])
                    # extract data if is_new_client and store it into global variable
                    elif col == 2:
                        detail['is_new_client'] = get_text(row_data[col])
                    # check if extracted information in detail variable is not empty
                    col = col + 1
                # check if extracted information in detail variable is not empty
                if len(detail) != 0:
                    confidential_information["confidential_clients_details"].append(
                        detail)
            row = row + 1
    # check if object contain "Confidential Matter" and "Confidential Work Highlights in last 12 months" matching string
    elif match_substring_recursive("Confidential Matter", data) or match_substring_recursive(
            "Confidential Work Highlights in last 12 months", data):
        detail = {}
        row = 0
        # loop to get the Confidential Matter details from the array list
        while row < len(data) - 1:
            row_data = data[row]
            # check if array not contain n/a value
            if not match_substring_recursive("N/A", row_data):
                # check if array values contain "Name of client" matching string
                if match_substring_recursive("Name of client", row_data) and subarray_exist(data, [row + 1, 0]):
                    detail['name'] = get_text(data[row + 1][0])
                # check if array values contain "Summary of matter and your department" matching string
                elif match_substring_recursive("Summary of matter and your department", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    extracted_data = "\n".join(data[row + 1][0]).replace("--", "\u2022").replace("\t", ""). \
                        replace(" ", "")
                    detail['summary'] = extracted_data
                # check if array values contain "Matter value" matching string
                elif match_substring_recursive("Matter value", row_data) and subarray_exist(data, [row + 1, 0]):
                    detail['matter_value'] = get_text(data[row + 1][0])
                # check if array values contain "Is this a cross-border matter" matching string
                elif match_substring_recursive("Is this a cross-border matter", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    detail['is_cross_border_matter'] = get_text(data[row + 1][0])
                # check if array values contain "Lead partner" matching string
                elif match_substring_recursive("Lead partner", row_data) and subarray_exist(data, [row + 1, 0]):
                    detail['lead_partner'] = get_text(data[row + 1][0])
                # check if array values contain "Other team members" matching string
                elif match_substring_recursive("Other team members", row_data) and subarray_exist(data, [row + 1, 0]):
                    detail['other_team_members'] = get_text(data[row + 1][0])
                # check if array values contain "Other firms advising on the matter" matching string
                elif match_substring_recursive("Other firms advising on the matter", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    detail['other_firms_advising'] = get_text(data[row + 1][0])
                # check if array values contain "Date of completion or current status" matching string
                elif match_substring_recursive("Date of completion or current status", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    detail['date_of_completion'] = get_text(data[row + 1][0])
                # check if array values contain "Other information about this matter" matching string
                elif match_substring_recursive("Other information about this matter", row_data) and \
                        subarray_exist(data, [row + 1, 0]):
                    detail['other_information'] = "\n".join(data[row + 1][0])
            row = row + 1
        # check if array values contain "Name of client" matching string
        if len(detail) > 0 and 'name' in detail and len(detail['name']) > 0:
            confidential_information["confidential_matters"].append(detail)


if __name__ == "__main__":
    create_database()
    azure()
