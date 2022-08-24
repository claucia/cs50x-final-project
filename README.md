# Blood bank management system

## Introduction

This is my final project for the CS50 course. Here I had the opportunity to conect almost every topic covert in the course,  Pyhon, SQL, HTML, CSS and Flask, to mention a few.  
The idea of building a blood bank management system came from the desire to connect my current studies in computer science with my professional background as a Biomedical scients.

## Objectives

This project aims to develop an application that allows Physicians to place a blood request for their patients. To fulfill that request, the blood bank professional can search in the database for blood bag availability that matches the requirements for that request.  
Even more, if eventually there are no blood bags available to fulfill a request, the blood bank professional can look to the database for donors with that blood type and invite them to donate.

## Features
### Users
The application was designed with two kinds of users in mind, Physicians working in hospitals that are going to make requests. And the blood bank professionals, which will have an admin login, to fulfill the Physicians' requests.  
Log in as an admin user is possible to perform the following actions:
 - Add new users;
 - Edit data from already registered users;
 - Moreover, it can search by name or role for the users listed in the database.

<!-- Screenshots or Gif? -->

### Donors
The donor's tab is available only for admin profiles. It lists all the donors that made at least one blood donation at that blood bank. The actions allowed in this tab are:
- Add new donors;
- Search for donors already registered;
- Edit any new information about the donor by clicking on the 'Edit' button;
- Finally, register a new donation at the 'Donate' button.

<!-- Screenshots or Gif? -->

### Blood requests
Both users have permission to access this tab. However, Physicians can place a new request, while admin profiles can not do that. On the other hand, at this tab on the admin profile, the user can take actions, such as view the blood request and work on it to fulfillment.  

<!-- Screenshots or Gif? -->

## Dependencies
- What is it and what each of them does?
- How it solves the problem?
- How I used each of them?

### Flask
A simple yet powerful Python web framework, it provides the technologies, tools, and modules used to build the actual functionalities of the web app.

### flask_login
User session management handles tasks such as logging in, logging out and remembering sessions.

### flask_sqlalchemy
It provides full functionality and flexibility of SQL to the application.


### WTForms
The WTForms is a built-in module of the flask that provides an alternative way of designing forms providing the interactive user interface for the user.


# Resolving the dependencies

Before running the application for the first time, use `pip` to resolve the dependencies:

```shell
$ pip install -r requirements.txt
```

# Running the application

Running the application:

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

# Lessons learned

Defining a route in Flask, we can specify parts of it that will be converted into Python variables and passed to the view function.

```python
@app.route('/user/id/<int:user_id>')
def profile(user_id):
    pass
```

This table shows Flask's built-in URL converters:
| Converter | Description                                     |
|-----------|-------------------------------------------------|
| string    | Accepts any text without a slash (the default). |
| int       | Accepts integers.                               |
| float     | Like int but for floating point value           |
| path      | Like string but accepts slashes.                |