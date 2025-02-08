"# BlogPost-Application" 

This is a simple BlogPost application using Python Django.

1. For running the project first you have to create a virtiual environment inside the project folder 
command: python -m venv <virtualenv name>

2. After creating the environment you have to activate the environment:
Command: <env name>\scripts\activate

3. After activating the environment install the necessary packages to run the project. You can find the packages name in requirements.txt file. Either you can install each package one by one using (pip install <package name> ) or all together using the below command
Command: pip install -r requirements.txt

4. Once the packages are installed you should adjust the database name in the settings.py file 
5. After that do the maigrations using 
Command: 
python manage.py makemigrations
python manage.py migrate

6. Once the migrations are complete run the project using 
Command: python manage.py runserver

7. You can view the project running in localhost copy that url from the terminal and paste it in any browser and run it, the application will successfully up and running.