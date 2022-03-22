import csv
import os, sys
import django
from recommand.models import Repositories

def DB_TO_CSV():
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django-erp2.settings")
	django.setup() 
	csv_path = '/Users/gimgunwoo/github/RR_AI/repo2.csv'
	with open(csv_path, 'w', newline='') as f_csv:
		field_names = ['id', 'keyword','repo_id','repo_name','full_name','description','created','language','stars','forks','subscribers','topics']
		data_writer = csv.DictWriter(f_csv, fieldnames=field_names) 
		data_writer.writeheader()

		for row in Repositories.objects.all():
			data_writer.writerow({
				'id':row.id,
				'keyword': row.keyword,
				'repo_id':row.repo_id,
				'full_name':row.full_name,
				'description':row.description,
				'created':row.created,
				'language':row.language,
				'stars':row.stars,
				'forks':row.forks,
				'subscribers':row.subscribers,
				'topics':row.topics
				})