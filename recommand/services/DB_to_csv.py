import csv
import os
import django
from recommand.models import Repositories
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def DB_TO_CSV():
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django-erp2.settings")
	django.setup() 
	csv_path = os.path.join(BASE_DIR, 'repo.csv')
	with open(csv_path, 'w', newline='') as f_csv:
		field_names = ['id', 'keyword','repo_id','repo_name','full_name','description','created','language','stars','forks','subscribers','topics']
		data_writer = csv.DictWriter(f_csv, fieldnames=field_names) 
		data_writer.writeheader()

		for row in Repositories.objects.all():
			data_writer.writerow({
				'id':row.id,
				'keyword': row.keyword,
				'repo_id':row.repo_id,
				'repo_name':row.repo_name,
				'full_name':row.full_name,
				'description':row.description,
				'created':row.created,
				'language':row.language,
				'stars':row.stars,
				'forks':row.forks,
				'topics':row.topics
				})