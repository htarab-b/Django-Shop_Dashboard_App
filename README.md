# Django Shop Dashboard App

## Description

This django app has normal dashboard of shops for the shop owners to view their shop data and alter or update them.

## Getting Started

### Installing
* Open terminal in your desired location of installation of local.
* Clone the repository.
```
git clone https://github.com/htarab-b/Django-Shop_Dashboard_App.git
```
* Create a virtual environment. (Optional)
```
python3 -m venv env
```
* Install the requirements for the project in the 'requirements.txt' file.
```
pip install -r requirements.txt
```

### Executing program
* Open VS Code or any IDE.
* Open new terminal and start the django server.
```
python manage.py runserver
```

## Use App
* Open your localhost, default : http://127.0.0.1:8000/
* Initially, the user has to signup/login
* After logging in, List of shops available is shown. Order can be placed for the shop by the user.
* To access the dashboard, open http://127.0.0.1:8000/dashboard.
* Only the users who own shops can access the dashboard.
* In the dashboard, all order details are displayed. The owner can change the status of the order.
* The dashboard also displays the progress of the shop and its orders. By displaying the percentage of orders delivered.
* Shops can be added only in the admin panel.


## Help
Superuser :
> Username : admin <br>Password  : adminpassword
