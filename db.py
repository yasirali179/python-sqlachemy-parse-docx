from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, Boolean
meta = MetaData()
engine = create_engine('sqlite:///data.db', echo=True)


submission_data = Table(
    'submission_data', meta,
    Column('id', Integer, primary_key=True),
    Column('publication_id', String),
    Column('subsection_id', String),
    Column('submissions_id', String),
)

# ------------------------------ Preliminary Information ------------------------------
preliminary_information = Table(
    'preliminary_information', meta,
    Column('id', Integer, primary_key=True),
    Column('firm_name', String),
    Column('practice_area', String),
    Column('location_jurisdiction', String),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

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
department_information = Table(
    'department_information', meta,
    Column('id', Integer, primary_key=True),
    Column('department_name', String),
    Column('number_of_partners', Integer),
    Column('qualified_lawyers', Integer),
    Column('male_ratio', Float),
    Column('female_ratio', Float),
    Column('department_best_known_for', String),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

heads_of_department = Table(
    'heads_of_department', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('phone', String),
    Column('department_information_id', Integer,
           ForeignKey('department_information.id')),
)
hires = Table(
    'hires', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('joined', String),
    Column('joined_from', String),
    Column('department_information_id', Integer,
           ForeignKey('department_information.id')),
)
ranked_lawyers_information = Table(
    'ranked_lawyers_information', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('comment', String),
    Column('partner', String),
    Column('department_information_id', Integer,
           ForeignKey('department_information.id')),
)
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
feedback = Table(
    'feedback', meta,
    Column('id', Integer, primary_key=True),
    Column('provious_coverage_feedback', String),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

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
publishable_information = Table(
    'publishable_information', meta,
    Column('id', Integer, primary_key=True),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

publishable_clients = Table(
    'publishable_clients', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('is_new_client ', Boolean),
    Column('publishable_information_id', Integer,
           ForeignKey('publishable_information.id')),
)

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

confidential_information = Table(
    'confidential_information', meta,
    Column('id', Integer, primary_key=True),
    Column('submission_data_id', Integer,
           ForeignKey('submission_data.id')),
)

confidential_clients = Table(
    'confidential_clients', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('is_new_client ', Boolean),
    Column('confidential_information_id', Integer,
           ForeignKey('confidential_information.id')),
)

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


def insert_submission_data(publication_id, subsection_id, submissions_id):
    data = submission_data.select().where(submission_data.c.publication_id == publication_id and
                                          submission_data.c.subsection_id == subsection_id and
                                          submission_data.c.submissions_id == submissions_id
                                          )
    conn = engine.connect()
    result = conn.execute(data)
    count = 0
    for row in result:
        count = count+1

    id = result.scalar()
    if count == 0:
        ins = submission_data.insert().values(publication_id=publication_id,
                                              subsection_id=subsection_id, submissions_id=submissions_id)
        conn = engine.connect()
        result = conn.execute(ins)
        return result.inserted_primary_key[0]
    else:
        return result.scalar()


def insert_preliminary_information(submission_data_id, data):
    insert = preliminary_information.insert().values(firm_name=data['frim_name'],
                                                     practice_area=data['practice_area'],
                                                     location_jurisdiction=data['localtion'],
                                                     submission_data_id=submission_data_id
                                                     )
    conn = engine.connect()
    result = conn.execute(insert)
    for person in data["contact_person_details"]:
        detailed = contact_person_arrange_interviews.insert().values(
            name=person['name'],
            email=person['email'],
            phone=person['phone'],
            preliminary_information_id=result.inserted_primary_key[0]
        )
        conn = engine.connect()
        result = conn.execute(detailed)


def insert_department_information(submission_data_id, data):
    insert = department_information.insert().values(department_name=data['department_name'],
                                                     number_of_partners=int(data['number_of_partners']),
                                                     qualified_lawyers=int(data['qualified_lawyers']),
                                                     department_best_known_for=data['qualified_lawyers'],
                                                     submission_data_id= submission_data_id
                                                     )
    conn = engine.connect()
    result = conn.execute(insert)
    for person in data["contact_person_details"]:
        detailed = contact_person_arrange_interviews.insert().values(
            name=person['name'],
            email=person['email'],
            phone=person['phone'],
            preliminary_information_id=result.inserted_primary_key[0]
        )
        conn = engine.connect()


def insert_feedback(submission_data_id, data):
    return


def insert_publishable_information(submission_data_id, data):
    return

def insert_confidential_information(submission_data_id, data):
    return
# def get_Data():
#     s = submission_data.select()
#     conn = engine.connect()
#     result = conn.execute(s)
#     return result


# def add_PreliminaryInformation():
#     ins = submission_data.insert().values(publication_id=publication_id,
#                                subsection_id=subsection_id, submissions_id=submissions_id)
#     conn = engine.connect()
#     result = conn.execute(ins)


def create():
    meta.create_all(engine)
