# CS411Project

## Important
This project's database is the inital ```tidychampaign.csv``` file because a lot of features are based on the "id" attribute of the initial file.
If you have the conflict, go to sql workbench, drop the table, and reimport the initial ```tidychampaign.csv```. It should solve the database conflict later on.

## Integrate steps:
To integrate this project, run the following command:

1. Clone this project to your local machine

```bash 
git clone git@github.com:Jonathan-UIUC/CS411Project.git
```

2. Go to the project directory

```bash 
cd CS411Project
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
