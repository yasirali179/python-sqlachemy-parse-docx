from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY
from sqlalchemy.orm import relationship
meta = MetaData()
engine = create_engine('sqlite:///data.db', echo=True)


Data = Table(
    'Data', meta,
    Column('publication_id', String),
    Column('subsection_id', String),
    Column('submissions_id', String),
    Column('preliminary_information_id', Integer,
           ForeignKey('PreliminaryInformation.id')),
    Column('department_information_id', Integer,
           ForeignKey('DepartmentInformation.id')),
    Column('feedback_id', Integer, ForeignKey('Feedback.id')),
    Column('publishable_information_id', Integer,
           ForeignKey('PublishableInformation.id')),
    Column('confidential_information_id', Integer,
           ForeignKey('ConfidentialInformation.id')),
)

# ------------------------------ Preliminary Information ------------------------------
PreliminaryInformation = Table(
    'PreliminaryInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('firm_name', String),
    Column('practice_area', String),
    Column('location_jurisdiction', String),
    Column('contact_person_arrange_interviews_id', Integer,
           ForeignKey('ContactPersonArrangeInterviews.id')),
)

ContactPersonArrangeInterviews = Table(
    'ContactPersonArrangeInterviews', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('phone', String),
)

# ------------------------------ Department Information ------------------------------
DepartmentInformation = Table(
    'DepartmentInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('department_name', String),
    Column('partners', Integer),
    Column('qualified_lawyers', Integer),
    Column('male_ratio', Integer),
    Column('female_ratio', Integer),
    Column('department_best_known_for', String),
    Column('heads_of_department_id', Integer,
           ForeignKey('HeadsofDepartment.id')),
    Column('hires_id', Integer,
           ForeignKey('Hires.id')),
    Column('ranked_lawyers_information_id', Integer,
           ForeignKey('RankedLawyersInformation.id')),
    Column('unranked_lawyers_information_id', Integer,
           ForeignKey('UnrankedLawyersInformation.id')),
)

HeadsofDepartment = Table(
    'HeadsofDepartment', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('phone', String),
)
Hires = Table(
    'Hires', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('joined', String),
    Column('joined_from', String),
)
RankedLawyersInformation = Table(
    'RankedLawyersInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('comment', String),
    Column('partner', String),
)
UnrankedLawyersInformation = Table(
    'UnrankedLawyersInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('comment', String),
    Column('partner', String),
)

# ------------------------------ Feedback ------------------------------
Feedback = Table(
    'Feedback', meta,
    Column('id', Integer, primary_key=True),
    Column('provious_coverage_feedback', String),
    Column('barristers_advocates_info_id', Integer,
           ForeignKey('BarristersAdvocatesInfo.id')),
)

BarristersAdvocatesInfo = Table(
    'BarristersAdvocatesInfo', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('firm', String),
    Column('comments', String),
)

# ------------------------------ Publishable Information ------------------------------
PublishableInformation = Table(
    'PublishableInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('publishable_clients_id', Integer,
           ForeignKey('PublishableClients.id')),
)

PublishableClients = Table(
    'PublishableClients', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('new_lient ', String),
)

PublishableMatters = Table(
    'PublishableMatters', meta,
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
           ForeignKey('PublishableInformation.id')),
)

# ------------------------------ Confidential Information ------------------------------

ConfidentialInformation = Table(
    'ConfidentialInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('confidential_clients_id', Integer,
           ForeignKey('ConfidentialClients.id')),
)

ConfidentialClients = Table(
    'ConfidentialClients', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('new_lient ', String),
)

ConfidentialMatters = Table(
    'ConfidentialMatters', meta,
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
           ForeignKey('ConfidentialInformation.id')),
)


def insert_Data(publication_id, subsection_id, submissions_id):
    ins = Data.insert().values(publication_id=publication_id,
                               subsection_id=subsection_id, submissions_id=submissions_id)
    conn = engine.connect()
    result = conn.execute(ins)


def get_Data():
    s = Data.select()
    conn = engine.connect()
    result = conn.execute(s)
    return result


def create():
    meta.create_all(engine)
