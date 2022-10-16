# Blood bank management system
#### Video Demo: https://youtu.be/o2R06GgSdeM

## Introduction

I am proud to present my final project for the CS50's Introduction to Computer Science course. This project gave me the opportunity to connect almost every topic learned in the course. For instance, Python, SQL, HTML, CSS, and Flask. Including powerful Flask extensions such as flask_login, flask_sqlalchemy, and WTForms.

The idea of building a blood bank management system came from the desire to connect my current studies in Computer Science to my professional background in Biomedical Science.

## Objectives

This project aims to develop an application that allows physicians to place a blood request for their patients to a blood bank. In order to fulfill blood requests, the blood bank professional can search for previously donated blood bag that matches the requirements for that request.

## How I planned the web app  

![Blood bank management system](/assets/blood-bank-management-system.png)

## Resolving the dependencies

Before running the application for the first time, use `pip` to resolve the dependencies:

```shell
$ pip install -r requirements.txt
```

## Running the application

```shell
$ export FLASK_APP=app/app.py
$ export FLASK_ENV=development
$ flask run
```

Or, as a single line:

```shell
$ FLASK_APP=app/app.py FLASK_ENV=development flask run
```

The application will be available at `http://127.0.0.1:5000`.

## Live refresh

When working with static content, such as CSS files, it's nice to have browser live refresh for quick development cycles. To run the application, use:

```shell
$ python live_refresh.py
```

And the application will be available at `http://127.0.0.1:5000`.

## About the dependencies

### Flask

A simple yet powerful Python web framework, it provides the technologies, tools, and modules used to build the actual functionalities of the web app. It includes functions to parse requests individually and requires the program's code to be organised in a certain way as follows:  

- `app.py`: It's the file where the Python code for the webserver lives. The web server can parse or analyse HTTP request headers and return different pages based on the route.
- `requeriments.txt`: This file contains a list of required libraries for the application.
- `static/`: It's a directory of static files, such as images and CSS files.
- `templates/`: It's a directory for HTML files that uses jinja syntax, a template engine. Using a template to set a basic layout for a page allows us to define the header once and keep it consistent over all the pages.

### flask_login

Extension for performing user session management, which handles tasks such as: logging in, logging out, and remembering user sessions.

### flask_sqlalchemy  

SQLAlchemy is an Object Relational Mapper (ORM) for Python, working as an abstraction layer over the database, so developers may not need to write the SQL commands directly.

In short, ORM frameworks map:

- Application classes to database tables.
- Class instances (objects) to database rows.
- And object attributes (fields) to database columns.

### WTForms

Forms are how input is collected from the user via UI elements such as buttons, text boxes, and dropdown menus. WTForms makes it easier to perform form validations, also helps rendering the form fields.

## What each of the files contains and does?

- `app/`:  
  - `app.py`: Initiate the Flask application with all the required configurations for the extensions flask_login and flask_sqlalchemy.  
  - `extensions.py`: Create instances of the main class of each extension.  
  - `utils.py`: Reload the user object from the user ID stored in the session; Create tables in the database before the first request;  Authorize access by roles.  
  - `app_setup.py`: Create tables and populate the database to make it easy to test the app.
  - `forms.py`: Define classes which are representations of forms. They are logical models of the user forms with fields, labels, and validations.  
  - `models.py`: Define classes for representing the application data model, which SQLAlchemy will use to define the database tables.

- `routes/`: Logical content for implementing all the functionalities of each route of the application. The files are organised in this way:  
`auth.py`, `blood_request.py`, `donor.py`, `home.py`, `user.py`.

- `static/`: All the CSS stylesheets of the application. The files are organised in this way: `form.css`, `header.css`, `home.css`, `style.css`, `tables.css`.

- `templates/`: Under templates there is a folder for each of the main application features which are: `auth/`, `blood_request/`, `donor/`, `home/`, `user/`.

## Features

The application was designed with two types of users in mind:

- Physicians working in hospitals that are going to make blood requests. These users have the `physician` profile.

- Blood bank professionals who can fulfill the blood requests created by physicians. These users have the `admin` profile.

Users must be authenticated to use the functionalities provided by the application. Only `admin` users can create new users.

### Login

Registered users can authenticate using their credentials:

![Login screenshot](/assets/login.png)

### Home

Displays a dashboard showing how many blood bags of each blood type is available in the blood bank stock.

There are also blood request statistics showing the amount of pending, approved, and rejected requests.

![Home screenshot](/assets/home.png)

### Users

This functionality is available only to `admin` users, who can perform the following actions:

 - Add new users
  
![Add new user screenshot](/assets/add-new-user.png)

 - Edit data from existing users

 ![Edit user screenshot](/assets/edit-user.png)

 - Search existing users by name or role

 ![Users screenshot](/assets/users.png)

### Donors

The donor functionality is available only for `admin` users, who can manage details from donors.

The actions allowed in this functionality are:

- Add new donors

![Add new donor screenshot](/assets/add-new-donor.png)

- Search for existing donors

![Donors screenshot](/assets/donors.png)

- Edit existing donor details by clicking the _Edit_ button

![Edit donor screenshot](/assets/edit-donor.png)

- Register a donation for an existing donor by clicking the _Donate_ button

![Register donation screenshot](/assets/register-donation.png)

### Blood requests

Both `admin` and `physician` users have permission to access this functionality:

- `physician` users can only create blood requests for a given patient, indicating the requested blood type along with the required amoung of units (blood bags).
- `admin` users can review the blood requests previously created by `physician` users and they can either approve or reject it, as described below.

When fulfilling a blood request, only the compatible blood bags that can be used for fulfilling such request will be displayed, so that the `admin` user can select them.

![Compatibility of blood types](/assets/compatibility-of-blood-types.jpeg)

Once `admin` users select the compatible blood bags they wish to use for fulfilling a given request, they can indicate that the request has been approved by clicking the _Approve_ button. This will associate the choosen blood bags with the request that has been approved. Those blood request can not be associated with any other requests. 

Blood requests cannot be partially fulfilled. In case there are no enough blood bags available for fulfilling a given request, `admin` users can reject the request by clicking the _Reject_ button, indicating that the blood bank is not able to complete that request.

![Blood request screenshot](/assets/blood-request.png)
![Fulfill blood request screenshot](/assets/fulfill-blood-request.png)

### Change password

This functionality allows users to change their password:

![Change password screenshot](/assets/change-password.png)

## Lessons learned

### Dynamic routes

When creating a functionality that requires looking up something by a given ID, it becomes handy to have the ID in the URL.

Consider a `GET` request to `user/100`, where `100` represents a user ID. This request can be mapped using the route displayed below, so that a developer can obtain the user ID, which will be passed as a parameter to the function:

```python
@app.route('/user/<int:user_id>')
def profile(user_id):
    # Use the variable
    print(user_id)
```

The Flask's built-in URL converters are listed below:

| Converter | Description                                     |
|-----------|-------------------------------------------------|
| string    | Accepts any text without a slash (the default). |
| int       | Accepts integers.                               |
| float     | Like int but for floating point value           |
| path      | Like string, but accepts slashes.               |


### Using `GET` and `POST`

![GET/POST](assets/blood-bank-management-system-GET_POST.png)

### `request.args` vs `request.form`

- `request.args`: Contains the URL encoded parameters, the part in the URL after the question mark, from a `GET` request.
- `request.form`: Contains `POST` data, the form parameters.

### Role-based authorisation

flask_login helps with user authentication (telling who the user is), but it does not support authorisation (telling what the user can do).

As the application uses have two types of user (`admin` and `physician`) it became necessary to create a custom decorator for checking the user role (see `utils.py`). It was inspired in this [post](https://stackoverflow.com/a/52323346) from Stack Overflow:

```python
# Decorator to authorize access by roles
def role_required(role):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role == role:
                return func(*args, **kwargs)
            else:
                flash('You don\'t have permissions to access this page.', 'error')
                return redirect(url_for('home'))
        return wrapper
    return actual_decorator
```

### Messing up with the database (and fixing it quickly)

During the development, more than often, I messed up with the database and found myself having to reinsert the data. Having to manually recreate the database and having to execute SQL scripts again and again was time consuming.

So I came up with the `app_setup.py` file: It simply recreates and populates the database for me each time I delete the database file `data.db`. It leverages the SQLAlchemy abstraction, so I don't need to write SQL directly.

### Live refresh for static content

Before CS50x, I've played with frontend development and I remember how handy the live refresh was when editing static content, such as HTML, CSS, and JavaScript.

Flask, by default, doesn't offer such functionality. But I manage to come up with something close by using autoreload, as described in this [post](https://stackoverflow.com/a/56974220) from Stack Overflow.

It sped up the development when working with static content (when editing CSS files, for example). See `live_refresh.py`, which can be executing by running `python live_refresh.py`:

```python
from app import app
from livereload import Server

if __name__ == '__main__':
    server = Server(app.app.wsgi_app)
    server.serve(port=5000)
```

It didn't seem to work well when editing Python code though. For that case, I just started the application using `flask run`.
