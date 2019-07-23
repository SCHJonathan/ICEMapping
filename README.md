# CS411Project

## Important
This project's database is using the latest ```tidychampaign.csv``` and ```geo.csv``` file uploaded by Han Bro.
If you have the conflict, go to sql workbench, drop the table, and reimport the ```tidychampaign.csv```. It should solve the database conflict later on.

## Prerequsite 

I used the ```crispy form``` package. 

``` bash
pip install django-crispy-forms
```

## Integration steps:
To integrate this project, run the following command:

1. Clone this project to your local machine

```bash 
git clone git@github.com:Jonathan-UIUC/ICEMapping.git
```

2. Go to the project directory

```bash 
cd ICEMapping
```

3. Migrate the changes on the databases

```bash 
python manage.py makemigrations
python manage.py migrate
```

4. Run the server

```bash 
python manage.py runserver
```