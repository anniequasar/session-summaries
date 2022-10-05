# MeetUp 161 - Beginners Python and Machine Learning - Tue 18 Oct 2022 - flask web application - Part 3

Links:
- Youtube: https://youtu.be/
- Github:  https://github.com/timcu/session-summaries/raw/master/online/meetup161_tim_flask_web_app_part_3.md
- Github:  https://github.com/timcu/bpaml-prime-minister
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/

References:
- https://flask.palletsprojects.com/en/2.2.x/tutorial/
- https://docs.python.org/3/library/sqlite3.html

Learning objectives:
- Create a web application using python, flask and sqlite3 to list prime ministers in Australia

@author D Tim Cummings

### Getting Started

Refer to 
- Part 1 https://github.com/timcu/session-summaries/raw/master/online/meetup152_tim_flask_web_app_prime_minister.md
- Part 2 https://github.com/timcu/session-summaries/raw/master/online/meetup156_tim_flask_web_app_part_2.md

### Challenge 5: Add authentication to application so users can log in.

1. Table already exists in database
2. Follow instructions in tutorial at https://flask.palletsprojects.com/en/2.2.x/tutorial/views/
3. Table is tbl_user with fields (id, vc_username, vc_password). Table in tutorial is user with fields (id, username, password)

```Shell
git checkout -b task5attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later
git checkout task6            # switch to a tag/branch to see the solution and be ready to start task 6
git diff task5 task6          # to see what has changed in creating the solution. 
```

### Challenge 6: Keep search form populated after clicking search button

```Shell
git checkout -b task6attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later
git diff task6 task6soln      # to see what has changed in creating the solution. 
```

### Challenge 7: Create files so that app can be packaged and installed

1. See https://flask.palletsprojects.com/en/2.2.x/tutorial/install/
2. Create setup.py
3. Create MANIFEST.in
4. pip install wheel
5. python setup.py bdist_wheel
6. pip install -e .

### Challenge 8: In template view_person.html show marriages in Life between birth and death

- Examples view_person.html
- e.g. "Married 1981 to Margie Aitken and had 3 children"
- If not actually married num_year_marriage will be None.
- e.g. "Partnered with Tim Matheison and had 0 children"
- Modify function view_person(id_person) in `__init__.py` to pass marriages to template
- Use a union sql statement because we need to search id_person and id_person_partner.
- The following sql uses named bindings.
```python
sql = """select id, id_person, id_person_partner, num_children, num_year_marriage
         from tbl_marriage where id_person=:id_person
         union
         select id, id_person_partner, id_person, num_children, num_year_marriage
         from tbl_marriage where id_person_partner=:id_person
         order by num_year_marriage asc"""
```

### Challenge 9: In view_person.html add a table of concurrent ministries under table of ministries.
	
- A concurrent ministry is one which was occurring at the same time as the person's ministry
- eg While John Howard was prime minister there were three deputy prime ministers
	-	Tim Fischer   Deputy from 11-Mar-1996 to 20-Jul-1999
	-	John Anderson Deputy from 20-Jul-1999 to 06-Jul-2005
	-	Mark Vaile    Deputy from 06-Jul-2005 to 03-Dec-2007
- Modify function view_person(id_person) in `__init__.py`
- Modify template view_person.html
- Pseudocode:
	- For each ministry period find other people's ministries which had some overlap.
	- Aggregate and remove duplicates from this list of ministries
	- Show the other ministries in order of start date.
