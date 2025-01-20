from elasticsearch_dsl import Document, Text, Keyword, connections
from website.models import Clinic, Dentist, Category

# Define Elasticsearch connection
connections.create_connection(hosts=['http://elasticsearch:9200'])

class ClinicDocument(Document):
    clinic_name = Text()
    slug = Text()
    address = Text()
    phone_number = Text()
    opening_hours = Text()
    status = Text()
    image = Text()
    class Index:
        name = 'clinics'  # Elasticsearch index name
ClinicDocument.init()

class DentistDocument(Document):
    dentist_name = Text()
    slug = Text()
    phone_number = Text()
    specialization = Text()
    position = Keyword()
    experience_years = Keyword()
    image = Text()

    class Index:
        name = 'dentists'  # Elasticsearch index name

DentistDocument.init()

class CategoryDocument(Document):
    name = Text()
    description = Text()
    slug = Text()
    image = Text()

    class Index:
        name = 'categories'  # Elasticsearch index name

CategoryDocument.init()
