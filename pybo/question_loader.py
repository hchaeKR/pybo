# 프로젝트 위치: /home/hchae/work/www
# 앱 이름: pybo

import csv
import os
import sys
from datetime import datetime
import django
from django.utils import timezone

sys.path.append('/home/hchae/work/www')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from pybo.models import Question

CSV_PATH='/home/hchae/work/www/pybo_question_data.csv'

question_list = []
author_id = 1

'''
Data Generator 특성으로 인해
author_id 치환 필요 (범위에서 생성)
미래 일시는 현재 (또는 과거 일시)로 변환
'''
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        # 존재하는 author_id로 변환
        if row['author_id'] == '1':
            print('if', row['author_id'])
            author_id = 1
        elif row['author_id'] == '2':
            print('elif', row['author_id'])
            author_id = 21
        else:
            print('else', row['author_id'])
            author_id = 1
        # 미래는 현재로 변환
        if timezone.make_aware(datetime.strptime(row['created'], '%m/%d/%Y')) > timezone.now():
            created = timezone.now()
        else:
            created = timezone.make_aware(datetime.strptime(row['created'], '%m/%d/%Y'))
        q = Question(
            subject=row['subject'],
            content=row['content'],
            created=created,
            last_upd=created,
            author_id=author_id
            )
        question_list.append(q)

total = len(question_list)
result = Question.objects.bulk_create(question_list)

success = len(result)
print(f'전체 { total }건 중 성공 { success }건, 실패 { total - success }')