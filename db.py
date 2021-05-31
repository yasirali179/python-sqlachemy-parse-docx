from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, Boolean, and_
from sqlalchemy import create_engine
from utils import to_int
meta = MetaData()

# database url
# engine = create_engine('postgresql://chambersadmin@historical-submissions-db:!:&<G9n5Jc?L@historical-submissions-db.postgres.database.azure.com:5432/postgres', echo=True)
db_path = "sqlite:///data.db"
engine = create_engine(db_path, echo=True)

# submission_data table
submission_data = Table(
    'submission_data', meta,
    Column('id', Integer, primary_key=True),
    Column('publication_id', String),
    Column('subsection_id', String),
    Column('submissions_id', String),
)

# ------------------------------ Preliminary Information ------------------------------
# preliminary_information table
preliminary_information = Table(
    'preliminary_information', meta,
    Column('id', Integer, primary_key=True),
    Column('firm_name', String),
    Column('practice_area', String),
    Column('location_jurisdiction', String),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

# contact_person_arrange_interviews table
contact_person_arrange_interviews = Table(
    'contact_person_arrange_interviews', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('phone', String),
    Column('preliminary_information_id', Integer,
           ForeignKey('preliminary_information.id')),
)

# ------------------------------ Department Information ------------------------------
# department_information table
department_information = Table(
    'department_information', meta,
    Column('id', Integer, primary_key=True),
    Column('department_name', String),
    Column('number_of_partners', String),
    Column('qualified_lawyers', String),
    Column('male_ratio', Float),
    Column('female_ratio', Float),
    Column('department_best_known_for', String),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

# heads_of_department table
heads_of_department = Table(
    'heads_of_department', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('phone', String),
    Column('department_information_id', Integer,
           ForeignKey('department_information.id')),
)

# hires table
hires = Table(
    'hires', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('joined_departed', String),
    Column('joined_from_destination_firm', String),
    Column('department_information_id', Integer,
           ForeignKey('department_information.id')),
)

# ranked_lawyers_information table
ranked_lawyers_information = Table(
    'ranked_lawyers_information', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('comment', String),
    Column('partner', String),
    Column('department_information_id', Integer,
           ForeignKey('department_information.id')),
)

# unranked_lawyers_information table
unranked_lawyers_information = Table(
    'unranked_lawyers_information', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('comment', String),
    Column('partner', String),
    Column('department_information_id', Integer,
           ForeignKey('department_information.id')),
)

# ------------------------------ Feedback ------------------------------
# feedback table
feedback = Table(
    'feedback', meta,
    Column('id', Integer, primary_key=True),
    Column('previous_coverage_feedback', String),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

# barristers_advocates_info table
barristers_advocates_info = Table(
    'barristers_advocates_info', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('firm', String),
    Column('comments', String),
    Column('feedback_id', Integer,
           ForeignKey('feedback.id')),
)

# ------------------------------ Publishable Information ------------------------------
# publishable_information table
publishable_information = Table(
    'publishable_information', meta,
    Column('id', Integer, primary_key=True),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

# publishable_clients table
publishable_clients = Table(
    'publishable_clients', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('new_client', String),
    Column('publishable_information_id', Integer,
           ForeignKey('publishable_information.id')),
)

# publishable_matters table
publishable_matters = Table(
    'publishable_matters', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('summary', String),
    Column('value', String),
    Column('cross_border', String),
    Column('lead_partner', String),
    Column('other_team_members', String),
    Column('other_firms_advising', String),
    Column('date_of_completion', String),
    Column('other_information', String),
    Column('publishable_information_id', Integer,
           ForeignKey('publishable_information.id')),
)

# ------------------------------ Confidential Information ------------------------------
# confidential_information table
confidential_information = Table(
    'confidential_information', meta,
    Column('id', Integer, primary_key=True),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

# confidential_clients table
confidential_clients = Table(
    'confidential_clients', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('new_client', String),
    Column('confidential_information_id', Integer,
           ForeignKey('confidential_information.id')),
)

# confidential_matters table
confidential_matters = Table(
    'confidential_matters', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('summary', String),
    Column('value', String),
    Column('cross_border', String),
    Column('lead_partner', String),
    Column('other_team_members', String),
    Column('other_firms_advising', String),
    Column('date_of_completion', String),
    Column('other_information', String),
    Column('confidential_information_id', Integer,
           ForeignKey('confidential_information.id')),
)


def check_db(publication_id, subsection_id, submissions_id):
    """ This function check if submission already exists in
        database.

        input: publication_id, subsection_id, submissions_id
        output: length of selected objects or None
    """
    # select query to get data from submission_data table
    data = submission_data.select().where(and_(submission_data.c.publication_id == publication_id,
                                               submission_data.c.subsection_id == subsection_id,
                                               submission_data.c.submissions_id == submissions_id)
                                          )
    # connect to the database
    conn = engine.connect()
    # execute the query
    result = conn.execute(data).fetchall()
    if len(result) == 0:
        return None
    else:
        return result[-1][0]


def insert_submission_data(publication_id, subsection_id, submissions_id):
    """ This function insert submission data into the database.

           input: publication_id, subsection_id, submissions_id
           output: primary key
       """
    # insert query to insert data into submission_data table
    ins = submission_data.insert().values(publication_id=publication_id,
                                          subsection_id=subsection_id, submissions_id=submissions_id)
    # connect to the database
    conn = engine.connect()
    # execute the query
    result = conn.execute(ins)
    # extract the primary key
    return result.inserted_primary_key[0]


def insert_preliminary_information(submission_data_id, data):
    """ This function insert preliminary information data
        into the "preliminary_information" table of database.

           input: object of preliminary information data
           output: nothing
       """
    # check if data exists in input object
    if 'firm_name' in data or 'practice_area' in data or 'location' in data:
        # insert query to insert data into preliminary_information table
        insert = preliminary_information.insert().values(firm_name=data['firm_name'] if "firm_name" in data else None,
                                                         practice_area=data[
                                                             'practice_area'] if "practice_area" in data else None,
                                                         location_jurisdiction=data[
                                                             'location'] if "location" in data else None,
                                                         submission_data_id=submission_data_id
                                                         )
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(insert)
        # extract the primary key
        id = result.inserted_primary_key[0]
    # insert contact person details into "contact_person_arrange_interviews" table
    for person in data.get("contact_person_details", []):
        # insert query to insert data into contact_person_arrange_interviews table
        detailed = contact_person_arrange_interviews.insert().values(
            name=person['name'] if "name" in person else None,
            email=person['email'] if "email" in person else None,
            phone=person['phone'] if "phone" in person else None,
            preliminary_information_id=id
        )
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(detailed)


def insert_department_information(submission_data_id, data):
    """ This function insert department information data
            into the "department_information" table of database.

               input: object of department information data
               output: nothing
           """
    # check if data exists in input object
    if len(data) > 0:
        # insert query to insert data into department_information table
        insert = department_information. \
            insert().values(department_name=data['department_name'] if "department_name" in data else None,
                            number_of_partners=
                            data['number_of_partners'] if "number_of_partners" in data and data[
                                'number_of_partners'] != '' else None,
                            qualified_lawyers=
                            data['qualified_lawyers'] if "qualified_lawyers" in data and data[
                                'qualified_lawyers'] != '' else None,
                            department_best_known_for=data[
                                'department_best_known'] if "department_best_known" in data else None,
                            submission_data_id=submission_data_id
                            )
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(insert)
        # extract the primary key
        id = result.inserted_primary_key[0]
    # insert heads_of_department_details into "heads_of_department" table
    for person in data.get("heads_of_department_details", []):
        # insert query to insert data into heads_of_department table
        detailed = heads_of_department.insert().values(
            name=person['name'] if "name" in person else None,
            email=person['email'] if "email" in person else None,
            phone=person['phone'] if "phone" in person else None,
            department_information_id=id
        )
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(detailed)
    # insert hires_details into "hires" table
    for person in data.get("hires_details", []):
        # insert query to insert data into hires table
        detailed = hires.insert().values(
            name=person['name'] if "name" in person else None,
            joined_departed=person['joined'] if "joined" in person else None,
            joined_from_destination_firm=person['joined_from'] if "joined_from" in person else None,
            department_information_id=id
        )
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(detailed)

    # insert ranked_lawyers_details into "ranked_lawyers_information" table
    for person in data.get("ranked_lawyers_details", []):
        # insert query to insert data into ranked_lawyers_information table
        detailed = ranked_lawyers_information.insert().values(
            name=person['name'] if "name" in person else None,
            comment=person['comments'] if "comments" in person else None,
            partner=person['is_partner'] if "is_partner" in person else None,
            department_information_id=id
        )
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(detailed)
    # insert unranked_lawyers_details into "unranked_lawyers_information" table
    for person in data.get("unranked_lawyers_details", []):
        # insert query to insert data into unranked_lawyers_information table
        detailed = unranked_lawyers_information.insert().values(
            name=person['name'] if "name" in person else None,
            comment=person['comments'] if "comments" in person else None,
            partner=person['is_partner'] if "is_partner" in person else None,
            department_information_id=id
        )
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(detailed)


def insert_feedback(submission_data_id, data):
    """ This function insert feedback information data
             into the "feedback" table of database.

                input: object of feedback information data
                output: nothing
            """
    # check if previous_coverage_department_feedback object exists in input object
    if 'previous_coverage_department_feedback' in data:
        previous_coverage_department_feedback = data['previous_coverage_department_feedback']
    else:
        previous_coverage_department_feedback = ''

    # insert query to insert data into feedback table
    insert = feedback.insert().values(previous_coverage_feedback=previous_coverage_department_feedback,
                                      submission_data_id=submission_data_id
                                      )
    # connect to the database
    conn = engine.connect()
    # execute the query
    result = conn.execute(insert)
    # extract the primary key
    id = result.inserted_primary_key[0]
    # check if barristers_advocates_selected_country_details object exists in input object
    if 'barristers_advocates_selected_country_details' in data:
        # insert barristers_advocates_selected_country_details into "barristers_advocates_info" table
        for person in data["barristers_advocates_selected_country_details"]:
            # insert query to insert data into barristers_advocates_info table
            detailed = barristers_advocates_info.insert().values(
                name=person['name'] if "name" in person else None,
                firm=person['firm'] if "firm" in person else None,
                comments=person['comments'] if "comments" in person else None,
                feedback_id=id
            )
            # connect to the database
            conn = engine.connect()
            # execute the query
            result = conn.execute(detailed)


def insert_publishable_information(submission_data_id, data):
    """ This function insert publishable information data
                into the "publishable_information" table of database.

                   input: object of publishable information data
                   output: nothing
               """
    # insert query to insert data into publishable_information table
    insert = publishable_information.insert().values(submission_data_id=submission_data_id)
    # connect to the database
    conn = engine.connect()
    # execute the query
    result = conn.execute(insert)
    # extract the primary key
    id = result.inserted_primary_key[0]
    # insert publishable_clients_details into "publishable_clients" table
    for person in data.get("publishable_clients_details", []):
        # insert query to insert data into publishable_clients table
        insert = publishable_clients.insert().values(
            name=person['name'] if "name" in person else None,
            new_client=person['is_new_client'] if "is_new_client" in person else None,
            publishable_information_id=id)
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(insert)
    # insert publishable_matters into "publishable_matters" table
    for matter in data.get("publishable_matters", []):
        # insert query to insert data into publishable_matters table
        insert = publishable_matters.insert().values(
            name=matter['name'] if "name" in matter else None,
            summary=matter['summary'] if "summary" in matter else None,
            value=matter['matter_value'] if "matter_value" in matter else None,
            cross_border=matter['is_cross_border_matter'] if "is_cross_border_matter" in matter else None,
            lead_partner=matter['lead_partner'] if "lead_partner" in matter else None,
            other_team_members=matter['other_team_members'] if "other_team_members" in matter else None,
            other_firms_advising=matter['other_firms_advising'] if "other_firms_advising" in matter else None,
            date_of_completion=matter['date_of_completion'] if "date_of_completion" in matter else None,
            other_information=matter['other_information'] if "other_information" in matter else None,
            publishable_information_id=id,
        )
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(insert)


def insert_confidential_information(submission_data_id, data):
    """ This function insert confidential information data
                    into the "confidential_information" table of database.

                       input: object of confidential information data
                       output: nothing
                   """
    # insert query to insert data into confidential_information table
    insert = confidential_information.insert().values(submission_data_id=submission_data_id)
    # connect to the database
    conn = engine.connect()
    # execute the query
    result = conn.execute(insert)
    # extract the primary key
    id = result.inserted_primary_key[0]
    # insert confidential_clients_details into "confidential_clients" table
    for person in data.get("confidential_clients_details", []):
        # insert query to insert data into confidential_clients table
        insert = confidential_clients.insert().values(
            name=person['name'] if "name" in person else None,
            new_client=person['is_new_client'] if "is_new_client" in person else None,
            confidential_information_id=id)
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(insert)

    # insert confidential_matters into "confidential_matters" table
    for matter in data.get("confidential_matters", []):
        # insert query to insert data into confidential_matters table
        insert = confidential_matters.insert().values(
            name=matter['name'] if "name" in matter else None,
            summary=matter['summary'] if "summary" in matter else None,
            value=matter['matter_value'] if "matter_value" in matter else None,
            cross_border=matter['is_cross_border_matter'] if "is_cross_border_matter" in matter else None,
            lead_partner=matter['lead_partner'] if "lead_partner" in matter else None,
            other_team_members=matter['other_team_members'] if "other_team_members" in matter else None,
            other_firms_advising=matter['other_firms_advising'] if "other_firms_advising" in matter else None,
            date_of_completion=matter['date_of_completion'] if "date_of_completion" in matter else None,
            other_information=matter['other_information'] if "other_information" in matter else None,
            confidential_information_id=id,
        )
        # connect to the database
        conn = engine.connect()
        # execute the query
        result = conn.execute(insert)


def create_database():
    # run migrations
    meta.create_all(engine)


if __name__ == "__main__":
    create_database()
