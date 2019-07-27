# CS411Project

## Important (Updated July 27)
1. This project's database is using the latest ```tidychampaign.csv``` and ```geo.csv``` file uploaded by Han Bro.
If you have the conflict, go to sql workbench, drop the table, and reimport the ```tidychampaign.csv```. It should solve the database conflict later on.

2. There is a list of new package I used to build this website. Please install those:

``` bash
pip install django-crispy-forms
pip install django-bootstrap-pagination
pip install django-bootstrap-toolkit
```

3. Please make sure you have imported all the csv files in the folder ```CSVDataFile``` via SQL workbench. For the ```CommentDB``` file, after you import it, you need to change the attribute type of geoid from ```int(11)``` to ```bigint(20)```. If you don't know to alter the table. See this link: https://stackoverflow.com/questions/33094174/how-to-change-update-column-name-in-table-using-mysql-workbench

4. If you create a new databse table, for the sake of convenience, you can create a sample .csv file like ```CommentDB.csv``` with some random data in it. Upload your sample .csv file in the ```CSVDataFile```.

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

3. Do all the stuffs in the ```Importent``` section.

4. Migrate the changes on the databases

```bash 
python manage.py makemigrations
python manage.py migrate
```

5. Run the server

```bash 
python manage.py runserver
```