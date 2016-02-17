1. The project is "Restaurants" which includes database_setup.py, project.py, lotsofmenus.py, menu.html, deleteconfirmation.html, newmenuitem.html, editmenuitem.html, deletemenuitem.html. The main function of the project is to show the menu of restaurants, user can edit them, create new item, delete item.

2. The file database_setup.py is used to setup database, lotsofmenus.py is used to add data to db.

3. All the html files are used to show the webpages.

5. The python version 2.7.6 should be installed before running the program, the vagrant version is 1.7.4, the virtual box version is 5.0.0.

6. how to run the code: Start up the vagrant using command vagrant up, then SSH into vagrant using command Vagrant SSH.

Using command cd /vagrant/Web
then run the command python database_setup.py to set up the database
then run the command python lotsofmenus.py to add data to the database
then run the command python project.py to start the server
enter the url at the brower to send the request, the url is http://localhost:5000/restaurants/2/menu

7. List of Author: Jane