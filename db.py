from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY
from sqlalchemy.orm import relationship
meta = MetaData()


Data = Table(
    'Data', meta,
    Column('publication_id', String),
    Column('subsection_id', String),
    Column('submissions_id', String),
    # relationship("PreliminaryInformation", "PreliminaryInformation"),
    # relationship("DepartmentInformation", "DepartmentInformation"),
    # relationship("Feedback", "Feedback"),
    # relationship("PublishableInformation", "PublishableInformation"),
    # relationship("ConfidentialInformation", "ConfidentialInformation")
)

PreliminaryInformation = Table(
    'PreliminaryInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('data_id', Integer, ForeignKey('Data.id')),
    Column('firm_name', String),
    Column('practice_area', String),
    Column('location_jurisdiction', String),
    #relationship("ContactPersonArrangeInterviews", "ContactPersonArrangeInterviews")
)

DepartmentInformation = Table(
    'DepartmentInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('data_id', Integer, ForeignKey('Data.id')),
    Column('department_name', String),
    Column('partners', Integer),
    Column('qualified_lawyers', Integer),
    Column('male_ratio', Integer),
    Column('female_ratio', Integer),
    Column('department_best_known_for', String),
    # relationship("HeadsofDepartment", "HeadsofDepartment"),
    # relationship("Hires", "Hires"),
    # relationship("RankedLawyersInformation", "RankedLawyersInformation"),
    # relationship("UnrankedLawyersInformation", "UnrankedLawyersInformation"),
)

Feedback = Table(
    'Feedback', meta,
    Column('id', Integer, primary_key=True),
    Column('data_id', Integer, ForeignKey('Data.id')),
    Column('provious_coverage_feedback', String),
    # relationship("BarristersAdvocatesInfo", "BarristersAdvocatesInfo"),
)

PublishableInformation = Table(
    'PublishableInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('data_id', Integer, ForeignKey('Data.id')),
    # relationship("PublishableClients", "PublishableClients"),
    # relationship("PublishableMatters", "PublishableMatters"),
)

ConfidentialInformation = Table(
    'ConfidentialInformation', meta,
    Column('id', Integer, primary_key=True),
    Column('data_id', Integer, ForeignKey('Data.id')),
    # relationship("ConfidentialMatters", "ConfidentialMatters"),
)




ContactPersonArrangeInterviews = Table(
    'ContactPersonArrangeInterviews', meta,
    Column('id', Integer, primary_key=True),
    Column('PreliminaryInformation', Integer, ForeignKey('PreliminaryInformation.id')),

    Column('name', String),
    Column('email', String),
    Column('phone', String),
)



def create():
    engine = create_engine('sqlite:///data.db', echo=True)
    meta.create_all(engine)
