# TodoApp
TodoApp is a simple multi-user task management application for tracking personal to-do's within specific to-do lists created using Django. 

## Overview
Semantics behind TodoApp is based on a system where multiple users under management of an admin, can organize their personal to-do tasks within their special to-do lists.

Users can signup to the system from ```signup``` page (which is accessable through ```login``` page) and get started to using TodoApp directly from ```home``` page.

In ```home``` page users can display their current set to-do lists and some more related information about them as well as creating, editing or sorting them. Once a user has a to-do list, he/she can access its current set of to-do tasks within the options near that specific to-do list via ```todos``` page.

In ```todos``` page, users can display current not-done to-do's and also the already-done ones. In this page, users can create, edit, delete, sort or mark as done the to-do items.

Get started to organize and track your stuff accordingly with Awesome TodoApp!!

Below there are samples from each page:

[login]: https://github.com/ysyesilyurt/TodoApp/blob/master/images/sample_login.png 
[signup]: https://github.com/ysyesilyurt/TodoApp/blob/master/images/sample_signup.png
[home]: https://github.com/ysyesilyurt/TodoApp/blob/master/images/sample_Home.png
[todos]: https://github.com/ysyesilyurt/TodoApp/blob/master/images/sample_Todos.png

```login```

![alt text][login]

```signup```

![alt text][signup]

```home```

![alt text][home]

```todos```

![alt text][todos]

### Fundamental Features

* Simplified and Organized to-do management within special to-do lists
* Basic operations (create, delete, edit) with both to-do lists and to-do items
* Drag and drop task prioritization for both to-do lists and to-do items
* Marking as done/undone feature for tasks


## Requirements

* Django~=2.1.5
* Python 3.6+
* jQuery 
* Bootstrap (to work with provided templates)


# Installation & Usage 

Since current TodoApp repository also contains its configured Django project (TodoProject) you can directly clone the repository get started.

Clone the repository
```
git clone https://github.com/ysyesilyurt/TodoApp/
```
Install requirements

```
cd TodoApp/
pip3 install -r requirements.txt
```

Create database tables
```
./manage.py migrate
```

(Optional) Create a super user to rule other users
```
./manage.py createsuperuser
```

Run django server
```
./manage.py runserver
```
Afterwards, go to server address (if you are using your local development server just go to ```localhost:8000```) and login to the application.
If you haven't created an admin account, you can create a user account easily from  ```signup``` page. 

## Contribution

Not all cases are covered, weird bugs may appear. Feel free to open an issue if you spot a bug. 

**Have an organized day! :blush:**

