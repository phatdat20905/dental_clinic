Các lệnh cơ bản:
- Tạo môi trường ảo: py -m venv env
- Kích hoạt môi trường ảo: myworld\Scripts\activate.bat
- Cài django: py -m pip install Django
- Tạo project: django-admin startproject my_project
- Tạo app: py manage.py startapp my_app
- Lệnh chạy dự án: py manage.py runserver
- python manage.py makemigrations website
- python manage.py migrate
- pip freeze > requirements.txt
- pip install -r requirements.txt
- tạo người dùng admin: python manage.py createsuperuser

Các bước push project lên github:
- git add .
- git commit -m "noi dung"
- git push origin "ten nhanh"

Các bước kéo dự án:
- git pull origin "ten nhanh"

Cài docker:
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourPassword123!" -p 1444:1433 --name sqlserver2022 -d mcr.microsoft.com/mssql/server:2022-latest

Các lệnh dùng để deploy docker:
- docker-compose down
- docker-compose up --build
- docker exec -it --user root sqlserver2022 /bin/bash
- docker exec -it --user root dental_clinic-web-1 /bin/bash