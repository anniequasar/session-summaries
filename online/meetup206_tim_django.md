# MeetUp 206 - Beginners Python and Machine Learning - Wed 24 Jul 2024 - Django with PyCharm Community Edition

## Part 1 - 24 Jul 2024

Links:

- Youtube: <https://youtu.be/golNmplBnmI>
- Github:  <https://github.com/timcu/bpaml-sessions/blob/master/online/meetup206_tim_django.md>
- Meetup:  <https://www.meetup.com/beginners-python-machine-learning/events/302090350/>

## Part 2 - 18 Sep 2024

Links:

- Youtube: <https://youtu.be/JSn1CzjyUS0>
- Github:  <https://github.com/timcu/bpaml-sessions/blob/master/online/meetup206_tim_django.md>
- Meetup:  <https://www.meetup.com/beginners-python-machine-learning/events/303070278/>

## References

- <https://www.jetbrains.com/pycharm/>
- <https://docs.djangoproject.com/en/5.0/intro/tutorial01/>
- <https://realpython.com/django-nginx-gunicorn/>

## Procedure

### Create project and app <https://docs.djangoproject.com/en/5.0/intro/tutorial01/>

If you are checking out the source code from github

- `git clone https://github.com/timcu/django_bpaml_site`
- `git checkout step01`

If you are following the script manually

- Create a new PyCharm project `django_bpaml_site`
  - Make sure you use a new virtual environment either venv, conda depending on your python installation
- Add this file to your project `meetup206_tim_django.md`
- Open Terminal window
- `pip install django-allauth[socialaccount]` This will also install Django, allauth with Google Auth and other dependencies
- `django-admin startproject django_bpaml_site`  # instead of `mysite` in tutorial
- PyCharm project and Django both have concept of "Project". We need to move all files from django project into pycharm project (up one directory)
  - Move `manage.py` up a folder
  - Move five files `__init__.py`, `asgi.py`, `settings.py`, `urls.py` and `wsgi.py` up a folder
  - Delete empty folder `django_bpaml_site`
- `pip freeze > requirements.txt`
- `python manage.py runserver`
- `python manage.py startapp django_bpaml_event`

#### Create settings for our app `git checkout step02`

Edit `django_bpaml_site/settings.py`

```python
INSTALLED_APPS = [
    'django_bpaml_event.apps.DjangoBpamlEventConfig',
    # ... before django.contrib
]
# ...
TEMPLATES = [
    {
        # ...
        'DIRS': ['templates'],
        # ...
    },
]
```

- Check database and timezone in `django_bpaml_site/settings.py` (default is sqlite3 and UTC)

In `django_bpaml_site/urls.py` link to new urls 

```python
from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('bpaml-event/', include('django_bpaml_event.urls'))
]
```

Create URLconf in `django_bpaml_event/urls.py`

```python
from django.urls import path
from django_bpaml_event.views import index_page

urlpatterns = [
  path('', index_page, name='index'),
]
```

Create the first view in `django_bpaml_event/views.py`

```python
from django.http import HttpResponse
def index_page(request):
    return HttpResponse("<h1>BPAML Event</h1>")
```

Now can test at <http://localhost:8000/bpaml-event/>

### Database setup <https://docs.djangoproject.com/en/5.0/intro/tutorial02/> `git checkout step03`

Create a data structure for Event and Attendee.

- Events need a code, date, title, location and description.
- Attendees can extend the admin User table. Only extra field required is their meetup name

Override the user model by adding the following to `django_bpaml_site/settings.py`

```python
# Override the provided user model for our use (adding a field for meetup_name and relationship to events)
AUTH_USER_MODEL = 'django_bpaml_event.User'
```

Create database models in `django_bpaml_event/models.py`

```python
from django.db import models
from django.contrib.auth.models import AbstractUser


class Event(models.Model):
    code = models.CharField(max_length=20)
    date = models.DateTimeField("date of event")
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)

    def __str__(self):
        return self.title


class User(AbstractUser):
    # add extra field and relationship to admin user
    meetup_name = models.CharField(max_length=200, null=True)
    events = models.ManyToManyField('Event', related_name='attendees', blank=True)

    def __str__(self):
        return f"{self.email}<{self.first_name} {self.last_name}>"
```

Make bpaml_event show up in admin app by editing `bpaml_event/admin.py`

```python
from django.contrib import admin

from django_bpaml_event.models import Event, User

admin.site.register(Event)
admin.site.register(User)
```

- Make the database migrations for bpaml_event with `python manage.py makemigrations`
- Create database tables for django_bpaml_event and admin `python manage.py migrate` (git users do this also)

- From a terminal window create a superuser `python manage.py createsuperuser` (git users do this also)
- Check out admin section of your django app <http://localhost:8000/admin/>

Now you can add some events in the admin interface

### Django views <https://docs.djangoproject.com/en/5.0/intro/tutorial03/> `git checkout step04`

- We need a list of events on a page we will call using url <http://127.0.0.1:8000/bpaml-event/>
- We want an individual event on a page we will call <http://127.0.0.1:8000/bpaml-event/event/[event-code]/>

In `django_bpaml_event/templates/django_bpaml_event/` create some templates used to construct the views.

index.html

```html
<h1>Upcoming events</h1>
<ul>
  <li>One</li>
  <li>Two</li>
  <li>Three</li>
</ul>
```

event.html

```html
<h1>Selected event</h1>
<p>Beginners' Python and Machine Learning</p>
```

In `django_bpaml_event/views.py` create some functions which return these views.

```python
from django.shortcuts import render

def index_page(request):
    return render(request, 'django_bpaml_event/index.html', {})

def event_page(request, code):
    return render(request, 'django_bpaml_event/event.html', {'code': code})
```

In `django_bpaml_event/urls.py` create some functions which return these views.

```python
from django.urls import path
from django_bpaml_event.views import index_page, event_page
urlpatterns = [
  path('', index_page, name='index'),
  path('event/<str:code>/', event_page, name='event'),
]
```

#### Create a template for <http://127.0.0.1:8000> with a couple of links in it

In `django_bpaml_event/templates/bpaml_home.html`

```html
<h1>BPAML</h1>
<ul>
    <li><a href="{% url 'index' %}">BPAML Events</a></li>
    <li><a href="{% url 'event' '20240710' %}">BPAML Event 20240710</a></li>
</ul>
```

In `django_bpaml_site/urls.py`

```python
from django.urls import path
from django.views.generic import TemplateView  # new
urlpatterns = [
     # ...
     path('', TemplateView.as_view(template_name="bpaml_home.html")),  # new
]
```

#### Create a base template so our style can be consistent throughout

Base it on the admin base template. Create file `django_bpaml_event/templates/django_bpaml_event/base.html`

```html
{% extends 'admin/base_site.html' %}
{% load static %}
{% block extrastyle %}
<link rel="stylesheet" href="{% static 'django_bpaml_event/bpaml.css' %}">
{% endblock %}
{% block title %}BPAML{% endblock %}
{% block branding %}
<div id="site-name"><a href="{% url 'index' %}">{{ site_header|default:_('BPAML Events') }}</a></div>
{% include "admin/color_theme_toggle.html" %}
{% endblock %}
{% block content %}
<div class="bpaml-content">
    {% block aside %}
    <aside id="user-sidebar"></aside>
    {% endblock %}
    <div class="bpaml-main">
    {% block main %}{% endblock %}
    </div>
</div>
{% endblock %}
```

Create a style sheet `django_bpaml_event/static/django_bpaml_event/bpaml.css`

```css
.bpaml-content {font-size: 1.0em;}
.bpaml-content .btnlink {padding: 7px; background: var(--button-bg); border: none; border-radius: 4px; color: var(--button-fg); vertical-align: middle; font-family: var(--font-family-primary); font-size: 0.8125rem;}
#user-sidebar .label {font-size: 0.7em;}
#user-sidebar {z-index: 15; flex: 0 0 275px; border-top: 1px solid transparent; border-right: 1px solid var(--hairline-color); background-color: var(--body-bg); overflow: auto;}
#user-sidebar table {width: 100%;}
#user-sidebar .module td {white-space: nowrap;}
#content > .bpaml-content {display: flex; flex: 1 0 auto;}
.bpaml-content .bpaml-main {padding-left: 10px;}
```

Now in each template remove the surrounding `<body>` tags and everything outside them and enclose remainder with

```html
{% extends 'django_bpaml_event/base.html' %}
{% block main %}

{% endblock %}
```

Try it out.

### Display real data in our web app `git checkout step05`

Edit `views.py` to fetch the data we want

```python
import datetime
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django_bpaml_event.models import Event

def index_page(request):
    """Find all events with an event date later than yesterday"""
    yesterday = timezone.now() - datetime.timedelta(days=1)
    list_future_events = Event.objects.filter(date__gte=yesterday).order_by("code")
    context = {'list_events': list_future_events}
    return render(request, 'django_bpaml_event/index.html', context)

def event_page(request, code):
    e = get_object_or_404(Event, code=code)
    context = {'event': e}
    return render(request, 'django_bpaml_event/event.html', context)
```

Edit `templates` to display the data

Replace `{%block main%}` to `{%endblock%}` in `django_bpaml_event/templates/django_bpaml_event/index.html` with the following

```html
{% block main %}
<section>
{% if list_events %}
<h1>Upcoming events</h1>
    <table>
    {% for event in list_events %}
        <tr>
            <td><a href="{% url 'event' event.code %}">{{ event.date }}</a></td>
            <td>{{ event.title }}</td>
        </tr>
    {% endfor %}
    </table>
{% else %}
    <p>No events have been scheduled</p>
{% endif %}
</section>
{% endblock %}
```

Replace in `django_bpaml_event/templates/django_bpaml_event/event.html` the following two blocks

```html
{% block main %}
<h1>Selected event</h1>
<h2>{{event.title}}</h2>
<h3>Code: {{event.code}}  Date: {{event.date}}</h3>
<h3>Location: {{event.location}}</h3>
<div>{{event.description|safe}}</div>
<h2>Attendee list</h2>
<table>
    <tr>
        {% if user.is_superuser %}
        <th>Email address</th>
        <th>Name</th>
        {% endif %}
        <th>Meetup name</th>
    </tr>
    {% for attendee in event.attendees.all %}
    <tr>
        {% if user.is_superuser %}
        <td>{{attendee.email}}</td>
        <td>{{attendee.first_name}} {{attendee.last_name}}</td>
        {% endif %}
        <td>{{attendee.meetup_name}}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}

{% block nav-breadcrumbs %}
<nav aria-label="Breadcrumbs">
  <div class="breadcrumbs">
    <a href="{% url 'index' %}">Events</a>
      &gt;
    <a href="{% url 'event' event.code %}">{{event.code}}</a>
  </div>
</nav>
{% endblock %}
```

This code demonstrates how to:

- show values from data model
- construct dynamic URLs
- override different blocks in templates being extended

### Challenge - add the breadcrumbs to index page `git checkout step06`

Here are the breadcrumbs for the top navigation bar in `index.html`

```html
{% block nav-breadcrumbs %}
<nav aria-label="Breadcrumbs">
  <div class="breadcrumbs">
    <a href="{% url 'index' %}">Events</a>
  </div>
</nav>
{% endblock %}
```

### Handling authenticated users who want to register `git checkout step07`

Edit `django_bpaml_site/settings.py` to add allauth components

```python
AUTHENTICATION_BACKENDS = [
    # Needed to log in by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]
INSTALLED_APPS = [
    'django_bpaml_event.apps.DjangoBpamlEventConfig',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # ... before django.contrib
]
MIDDLEWARE = [
    # ...
    "allauth.account.middleware.AccountMiddleware",
]
# ...
import json
try:
    with open('client_secret.json', mode='r') as json_file:
        client_secret = json.load(json_file)
except FileNotFoundError:
    client_secret = {'web': {'client_id': 'placeholder', 'client_secret': 'placeholder'}}
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APPS': [{
            'client_id': client_secret['web']['client_id'],
            'secret': client_secret['web']['client_secret'],
            'key': ''
        }],
        'EMAIL_AUTHENTICATION': True,  # User will take over account with his email
    }
}
```

Now we need to run the allauth migrations `python manage.py migrate` so that the database data structure exists for allauth.

Add the following to project `django_bpaml_site/urls.py`

```python
from django.urls import include, path
urlpatterns = [
    # ...
    path('accounts/', include('allauth.urls')),
]
```

In `base.html` load socialaccount at the top (after extends) `{% load socialaccount %}` and
add the following to the bottom of the aside block

```html
{% block aside %}
<aside class="sticky" id="user-sidebar">
    <div class="module">
        <table>
            <caption>Authenticated user</caption>
            {% if user.is_authenticated %}
            <tr><td><div class="label">Email</div><div>{{user.email}}</div></td></tr>
            <tr><td><div class="label">Name</div><div>{{user.first_name}} {{user.last_name}}</div></td></tr>
            <tr><td><div class="label">Name on Meetup</div><div>{{user.meetup_name}}</div></td></tr>
            <tr><td><div><a class="btnlink" href="{% url 'index' %}">Update member details</a></div></td></tr>
            <tr><td><div><a class="btnlink" href="{% url 'account_logout' %}">Sign out</a></div></td></tr>
            {% else %}
            <tr><td><div>Not logged in. <a class="btnlink" href="{% url 'admin:login' %}?next={{request.path}}">Sign in</a></div></td></tr>
            {% endif %}
        </table>
    </div>
</aside>
{% endblock %}
```

### Accepting registrations to events `git checkout step08`

Add a registration function to the `django_bpaml_event/views.py`

```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from allauth.account.decorators import login_required
from django_bpaml_event.models import Event
@login_required()
def attend(request, code, rsvp):
    """Set registration status for logged-in user as not attending
    code: event code
    rsvp: yes or no or true or false"""
    user = request.user
    e = get_object_or_404(Event, code=code)
    # Add to event on y, yes, Y, Yes, t, True, true
    if rsvp is None or len(rsvp) < 1:
        pass  # do nothing
    if rsvp.lower()[:1] in 'yt':
        user.events.add(e)
    elif rsvp.lower()[:1] in 'nf':
        user.events.remove(e)
    url_next = request.GET.get('next')
    if url_next is None:
        context = {'event': e}
        return render(request, 'django_bpaml_event/event.html', context)
    else:
        return HttpResponseRedirect(url_next)
```

Add URLs to `django_bpaml_event/urls.py`

```python
from django.urls import path
from django_bpaml_event.views import attend
urlpatterns = [
    # ...
    path('event/attend/<str:code>/<str:rsvp>/', attend, name='attend'),
]
```

In the templates add hyperlinks and status of attendance.

`django_bpaml_event/index.html` add a third column to table

```html
            {% if user.is_authenticated %}
            <td>
            {% url 'index' as url_next %}
            {% if user in event.attendees.all %}
                ATTENDING  (<a href="{% url 'attend' code=event.code rsvp='no' %}" title="change to NOT ATTENDING">change</a>)
            {% else %}
                NOT ATTENDING  (<a href="{% url 'attend' code=event.code rsvp='yes' %}" title="change to ATTENDING">change</a>)
            {% endif %}
            </td>
            {% endif %}
```

`django_bpaml_event/event.html` add a paragraph after location heading indicating attendee status.

```html
{% if user.is_authenticated %}
<p class="highlight">
    Member {{ user.first_name }} {{user.last_name}} with email address {{ user.email }}:
    {% if user in event.attendees.all %}
      ATTENDING  (<a href="{% url 'attend' code=event.code rsvp='no' %}" title="change to NOT ATTENDING">change</a>)
    {% else %}
      NOT ATTENDING (<a href="{% url 'attend' code=event.code rsvp='yes' %}" title="change to ATTENDING">change</a>)
    {% endif %}
</p>
{% endif %}
```

### Django form to allow member to update their own details `git checkout step09`

Add function to `django_bpaml_event/views.py` to render a form (if GET request) or save form data (if POST request)

```python
from allauth.account.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required()
def member(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first-name", user.first_name)
        user.last_name = request.POST.get("last-name", user.last_name)
        user.meetup_name = request.POST.get("meetup-name", user.meetup_name)
        user.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "django_bpaml_event/member.html", context={})
```

Create the html template of the form `django_bpaml_event/templates/django_bpaml_event/member.html`

```html
{% extends 'django_bpaml_event/base.html' %}
{% block main %}
{% if user.is_authenticated %}
<h2>Authenticated user</h2>
<form action="{% url 'member-edit' %}" method="post">
{% csrf_token %}
    <table>
        <tr>
            <td>Email: </td>
            <td>{{ user.email }}</td>
        </tr>
        <tr>
            <td>Name:</td>
            <td><input type="text" name="first-name" value="{{ user.first_name }}" size="20"><input type="text" name="last-name" value="{{ user.last_name }}" size="20"></td>
        </tr>
        <tr>
            <td>Meetup Name:</td>
            <td><input type="text" name="meetup-name" value="{{ user.meetup_name }}" size="47"></td>
            <td>Your name on meetup, so we can match the two attendee lists</td>
        </tr>
    </table>
    <input type="submit" value="Save">
</form>
{% else %}
<p>Please sign in to update member details</p>
{% endif %}
{% endblock %}
```

Add url to `django_bpaml_event/urls.py`

```python
from django.urls import path
from django_bpaml_event.views import member
urlpatterns = [
    # ...
    path('member-edit/', member, name='member-edit'),
]
```

Change url in `django_bpaml_event/base.html` to `{% url 'member-edit' %}`

### Changing admin forms - Use a textarea rather than a text input field for event description `git checkout step10`

Create a file `django_bpaml_event/forms.py`

```python
from django import forms
from django_bpaml_event.models import Event

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 20, 'cols': 80})
        }
```

Change `djando_bpaml_event/admin.py` to the following

```python
from django.contrib import admin
from django_bpaml_event.forms import EventAdminForm
from django_bpaml_event.models import Event, User

admin.site.register(User)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
```

### OAuth `git checkout step11`

(git users do this also)

Follow Google OpenID Connect to create a project and get credentials <https://developers.google.com/identity/openid-connect/openid-connect>

Set up project in Google API Console <https://console.developers.google.com/>

Needed credentials are client ID and client secret <https://docs.allauth.org/en/latest/socialaccount/providers/google.html>

<https://console.cloud.google.com/apis/credentials>

- Select project (or create a new one)
- Create credentials > OAuth Client ID > Configure OAuth consent screen
  - External
  - App name: BPAML
  - User support email: <pythonatordev@gmail.com>
  - Home page: <https://bpaml.pythonator.com>
  - Privacy: <https://link.pythonator.com/privacy.html>
  - Terms of service: <https://link.pythonator.com/terms-of-service.html>
  - Developer contact: <pythonatordev@gmail.com>
  - Non-sensitive Scopes: /auth/userinfo.email, /auth/userinfo.profile, openid
- Create credentials > OAuth Client ID > Web Application
  - Name: BPAML Event
  - Authorised JavaScript origins: <http://localhost:8000>
  - Authorised redirect URIs: <http://127.0.0.1:8000/accounts/google/login/callback/>
- Download client_secret.json to project directory top level `django_bpaml_site`. Don't commit to git.

Follow set up in <https://docs.allauth.org/en/latest/installation/quickstart.html>

Add following to `django_bpaml_site/settings.py`

```python
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_ONLY = True
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
LOGIN_REDIRECT_URL = "/bpaml-event/"
LOGOUT_REDIRECT_URL = "/bpaml-event/"
```

In `base.html` replace

`<a class="btnlink" href="{% url 'admin:login' %}?next={{request.path}}">Sign in</a>`

with

`<a class="btnlink" href="{% provider_login_url 'google' %}">Sign in with Google</a>`

### Fix style on `Sign in` and `Sign out` pages by overriding allauth base.html (copied from venv) `git checkout step12`

Create file `templates/allauth/layouts/base.html`

```html
{% extends 'django_bpaml_event/base.html' %}
{% load i18n %}
        {% block body %}
            {% if messages %}
                <div>
                    <strong>{% trans "Messages:" %}</strong>
                    <ul>
                        {% for message in messages %}<li>{{ message }}</li>{% endfor %}
                    </ul>
                </div>
            {% endif %}
            <div>
                <strong>{% trans "Menu:" %}</strong>
                <ul>
                    {% if user.is_authenticated %}
                        {% url 'account_email' as email_url %}
                        {% if email_url %}
                            <li>
                                <a href="{{ email_url }}">{% trans "Change Email" %}</a>
                            </li>
                        {% endif %}
                        {% url 'account_change_password' as change_password_url %}
                        {% if change_password_url %}
                            <li>
                                <a href="{{ change_password_url }}">{% trans "Change Password" %}</a>
                            </li>
                        {% endif %}
                        {% url 'mfa_index' as mfa_url %}
                        {% if mfa_url %}
                            <li>
                                <a href="{{ mfa_url }}">{% trans "Two-Factor Authentication" %}</a>
                            </li>
                        {% endif %}
                        {% url 'usersessions_list' as usersessions_list_url %}
                        {% if usersessions_list_url %}
                            <li>
                                <a href="{{ usersessions_list_url }}">{% trans "Sessions" %}</a>
                            </li>
                        {% endif %}
                        {% url 'account_logout' as logout_url %}
                        {% if logout_url %}
                            <li>
                                <a href="{{ logout_url }}">{% trans "Sign Out" %}</a>
                            </li>
                        {% endif %}
                    {% else %}
                        {% url 'account_login' as login_url %}
                        {% if login_url %}
                            <li>
                                <a href="{{ login_url }}">{% trans "Sign In" %}</a>
                            </li>
                        {% endif %}
                        {% url 'account_signup' as signup_url %}
                        {% if signup_url %}
                            <li>
                                <a href="{{ signup_url }}">{% trans "Sign Up" %}</a>
                            </li>
                        {% endif %}
                    {% endif %}
                </ul>
            </div>
            {% block content %}
            {% endblock content %}
        {% endblock body %}
        {% block extra_body %}
        {% endblock extra_body %}
```

### Creating a deployable package <https://docs.djangoproject.com/en/5.0/intro/reusable-apps/> `git checkout step13`

Copy this file to `django_bpaml_site/README.md`

Create `django_bpaml_site/LICENSE`

```text
MIT License

Copyright (c) 2024 D Tim Cummings

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Create `django_bpaml_site/pyproject.toml` 
- <https://packaging.python.org/en/latest/guides/writing-pyproject-toml/>
- <https://setuptools-scm.readthedocs.io/en/stable/usage/>

```toml
[project]
name = "django-bpaml-event"
dynamic = ["version"]
authors = [
    {name = "D Tim Cummings", email = "pythonatordev@gmail.com"},
]
description = "A Django app to accept registrations for upcoming events using Google login"
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">= 3.10"
keywords = ["bpaml", "registration", "oauth", "django", "google", "beginners' python"]
dependencies = [
    "Django ~= 5.1.1",
    "django-allauth[socialaccount] ~= 64.2.1",
    "gunicorn ~= 23.0.0",
    "psycopg ~= 3.2.1",
]

classifiers =[
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: Implementation :: CPython",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Framework :: Django :: 5.1.1",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
]

[project.urls]
homepage = "https://bpaml.pythonator.com/bpaml-event/"
repository = "https://github.com/timcu/django_bpaml_site"

[build-system]
requires = ['setuptools>=74.1.2', "wheel>=0.44.0", "setuptools-scm[toml]>=8.1.0"]
build-backend = 'setuptools.build_meta'

[tool.setuptools_scm]
version_file = "django_bpaml_event/_version.py"

[tool.setuptools.packages.find]
include = ["django_bpaml_event*"]
```

Create `django_bpaml_site/MANIFEST.in`

```text
# setuptools_scm includes all files in git so need to exclude some
recursive-exclude .idea *
recursive-exclude django_bpaml_site *
exclude manage.py requirements.txt meetup206_tim_django.md
```

Git ignore _version.py by adding to .gitignore

```txt
django_bpaml_event/_version.py
```

Create a new branch in git and commit these changes. Then create a tag 0.13.0

```commandline
git checkout -b my-branch
git add .
git commit -m "ready to build wheel"
git tag 0.13.0
```

To package python distribution:

```bash
rm -R dist django_bpaml_event.egg-info
python -m build
```

### Deploy to debian based linux such as debian, ubuntu, or raspios

Need to create a new client_secret.json file as we will be calling javascript from different host other than 127.0.0.1
If you have a domain name, use that. In our example we could use https://bpaml.pythonator.com

- "redirect_uris":["http://192.168.0.1/accounts/google/login/callback/"]
- "javascript_origins":["http://192.168.0.1"]


Copy the following files to debian server

```
dist/django_bpaml_event-0.13.0-py3-none-any.whl
django_bpaml_site/settings.py
django_bpaml_site/urls.py
client_secret.json
```

We are going to run as an unprivileged user `djangoer`

```bash
sudo apt install nginx
sudo useradd -m -s /bin/bash djangoer  # creates user
sudo mv django_bpaml_event-0.13.0-py3-none-any.whl ~djangoer/  # move install wheel to deploy user from 
sudo mv settings.py ~djangoer/  # copy our site settings to deploy user
sudo mv urls.py ~djangoer/  # copy our site urls to deploy user
sudo mv client_secret.json ~djangoer/  # copy our google credentials to deploy user
sudo su - djangoer  # switch user to that new user
```

As deploy user `djangoer`

```bash
python3 -m venv venv-bpaml-event  # create virtual environment so we don't pollute system or user environments
source venv-bpaml-event/bin/activate  # activate virtual environment
pip install django_bpaml_event-0.13.0-py3-none-any.whl  # install app and all dependencies into venv
mkdir -p wsgi-scripts/  # create folder for configuration and log files
cd wsgi-scripts
django-admin startproject bpaml_project  # creates manage.py and settings
cp ../client_secret.json bpaml_project/  # make google client secrets available to app
cp ../settings.py bpaml_project/bpaml_project/  # replace sample settings with our settings
cp ../urls.py bpaml_project/bpaml_project/  # replace sample urls with our urls
# Set up database
cd bpaml_project
python manage.py migrate
python manage.py createsuperuser
```

Update bpaml_project/settings.py for new deployment environment

```python
SECRET_KEY = 'give me a new secret key'
DEBUG = False  # was True and you could leave as True until site is working
ALLOWED_HOSTS = ["192.168.0.1"]  # set to your IP address and or fully qualified domain name (FQDN) of nginx webserver
ROOT_URLCONF = 'bpaml_project.urls'  # was django_bpaml_site.urls
WSGI_APPLICATION = 'bpaml_project.wsgi.application'  # was django_bpaml_site.wsgi.application
```

As sudo user. 
```bash
# Configure systemd so can run as a service automatically
# (gunicorn will look for application in django_bpaml_event.wsgi so can omit :application)
cat <<EOF | sudo tee /etc/systemd/system/bpaml-event.service
[Unit]
Description=Gunicorn instance to serve BPAML Event
After=network.target
[Service]
User=djangoer
Group=www-data
WorkingDirectory=/home/djangoer/wsgi-scripts/bpaml_project
Environment="PATH=/home/djangoer/venv-bpaml-event/bin"
ExecStart=/home/djangoer/venv-bpaml-event/bin/gunicorn --workers 2 --bind unix:bpaml_project.sock -m 007 'bpaml_project.wsgi'
[Install]
WantedBy=multi-user.target
EOF

# Configure nginx webserver for unencrypted http access on port 80
# Add extra server names or wild cards if required. Underscore _ is a catch-all server name
#   server_name bpaml.pythonator.com 192.168.0.1 *.bpaml.pythonator.com;
cat <<EOF | sudo tee /etc/nginx/sites-available/bpaml.pythonator.com
server {
    server_name bpaml.pythonator.com;
    # log files
    access_log /var/log/nginx/bpaml.access.log;
    error_log /var/log/nginx/bpaml.error.log;
    location / {
        proxy_pass http://unix:/home/djangoer/wsgi-scripts/bpaml_project/bpaml_project.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    location /static {
        autoindex on;
        alias /var/www/bpaml.pythonator.com/static/;
    }
    listen 80;
}
EOF

# Create links so nginx serves static content directly rather than through gunicorn
sudo mkdir -p /var/www/bpaml.pythonator.com/static/
sudo ln -s /home/djangoer/venv-bpaml-event/lib/python3.11/site-packages/django/contrib/admin/static/admin /var/www/bpaml.pythonator.com/static/admin
sudo ln -s /home/djangoer/venv-bpaml-event/lib/python3.11/site-packages/django_bpaml_event/static/django_bpaml_event /var/www/bpaml.pythonator.com/static/django_bpaml_event

# Enable systemd service
sudo systemctl enable bpaml-event.service  # start automatically after reboot
sudo systemctl start bpaml-event.service   # start now
sudo systemctl status bpaml-event.service  # check 
```

You might need to open up the firewall

```bash
sudo ufw allow http
sudo ufw allow https
```

See https://letsencrypt.org to see how to use certbot to get TLS certificates. You need to own the domain name and your server needs to be accessible from the Internet.

Now you can view website using URLs such as http://192.168.0.1/bpaml-event or https://bpaml.pythonator.com/bpaml-event
