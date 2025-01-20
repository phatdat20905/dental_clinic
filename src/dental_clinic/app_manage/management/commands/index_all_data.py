from django.core.management.base import BaseCommand
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
from website.models import Clinic, Dentist, Category
from app_manage.documents import ClinicDocument, DentistDocument, CategoryDocument

def get_clinic_data():
    clinics = Clinic.objects.all()
    for clinic in clinics:
        yield ClinicDocument(
            meta={'id': clinic.id},
            clinic_name = clinic.clinic_name,
            address = clinic.address,
            slug = clinic.slug,
            phone_number = clinic.phone_number,
            opening_hours = clinic.opening_hours,
            status = clinic.status,
            image=clinic.image.url if clinic.image else ""  # Thêm trường image
        ).to_dict(include_meta=True)


def get_dentist_data():
    dentists = Dentist.objects.all()
    for dentist in dentists:
        yield DentistDocument(
            meta={'id': dentist.id},
            dentist_name=dentist.dentist.full_name,
            phone_number=dentist.dentist.phone_number,
            slug=dentist.slug,
            specialization=dentist.specialization,
            position=dentist.position,
            experience_years=dentist.experience_years,
            image=dentist.dentist.image.url if dentist.dentist.image else ""  # Thêm trường image
        ).to_dict(include_meta=True)

def get_category_data():
    categories = Category.objects.all()
    for category in categories:
        yield CategoryDocument(
            meta={'id': category.id},
            name=category.name,
            description=category.description,
            slug=category.slug,
            image=category.image.url if category.image else ""  # Thêm trường image
        ).to_dict(include_meta=True)

class Command(BaseCommand):
    help = "Index data from Clinic, Dentist, and Category models into Elasticsearch"

    def handle(self, *args, **kwargs):
        es = connections.get_connection()
        
        # Index Clinic data
        bulk(client=es, actions=get_clinic_data())
        
        # Index Dentist data
        bulk(client=es, actions=get_dentist_data())
        
        # Index Category data
        bulk(client=es, actions=get_category_data())
        
        self.stdout.write(self.style.SUCCESS('Indexed all data for Clinic, Dentist, and Category'))


