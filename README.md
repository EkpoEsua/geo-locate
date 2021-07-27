# Geo-Locate

## Install prequisite for PostgreSQL connection
`sudo apt install python3-dev libpq-dev`

## Create and activate python virtual environment
`python3 -m venv venv`

`source venv/bin/activate`

## Clone and change working directory

`git clone https://github.com/EkpoEsua/geo-locate.git`

`cd geo-locate`

## Install requiremnents

`pip install -r requirments.txt`

## Run Tests
`python manage.py test locate`

## Run server

`python manage.py runserver`

Access locally on: http://127.0.0.1:8000/providers


Hosted on: https://esuaekpo.pythonanywhere.com/

* providers/ - CRUD endpoint for providers

* providers/<pk>/service-area/ - CRUD endpoint for service area associated with a created provider, access via `"service_area_list"` key in response after creating provider
pk - primary key of existing provider

* locate/ - api for searching for service areas in a specific point 
    sample query parameters: ?lat=1&lon=2 - values must be intergers
