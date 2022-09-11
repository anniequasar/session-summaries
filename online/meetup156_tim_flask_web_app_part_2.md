# MeetUp 152 - Beginners Python and Machine Learning - Tue 9 Aug 2022 - flask web application

Links:
- Youtube: https://youtu.be/5d-O92wYv3o
- Github:  https://github.com/timcu/session-summaries/raw/master/online/meetup156_tim_flask_web_app_part_2.md
- Github:  https://github.com/timcu/bpaml-prime-minister
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/287815114/

References:
- https://flask.palletsprojects.com/en/2.2.x/tutorial/
- https://docs.python.org/3/library/sqlite3.html

Learning objectives:
- Use Python virtual environments in PyCharm Community Edition IDE
- Use git to check out source from a code repository and move between branches
- Create a web application using python, flask and sqlite3 to list prime ministers in Australia

@author D Tim Cummings

### Getting Started

Refer to https://github.com/timcu/session-summaries/raw/master/online/meetup152_tim_flask_web_app_prime_minister.md


### Demo 2:

```Shell
git checkout task2            # to get ready for doing task 2
flask init-db
```

### Challenge 2: List all people in database in list_person.html

1. Add sql to `prime_minister.view_persons()` function and pass results to `render_template`
2. Create a table in `list_person.html` with a loop to repeat the rows

```sql
select distinct p.id, p.vc_common_name, p.vc_surname, p.date_birth, p.vc_birth_place, p.date_death 
from tbl_person p
order by p.vc_surname asc, p.vc_common_name asc
```

```Shell
git checkout -b task2attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later if desired
git checkout task3            # switch to a branch to see the solution and be ready to start task 3
git diff task2 task3          # to see what has changed in creating the solution. <space> to page. q to quit
```

### Challenge 3: Show list of recreations in view_person.html

1. `tbl_recreation` has a foreign key `id_person` which joins to `tbl_person` `id`
2. `tbl_recreation` has a varchar field `vc_recreation` which contains the name of the recreation
3. Add sql in `prime_minister.view_person(id_person)` to find the list of recreations
4. Pass the list of recreations to `render_template('view_person.html')`
5. Modify `view_person.html` to list any recreations

```
sql = """select * from tbl_recreation where id_person=?"""
recreations = pm_db.execute(sql, (person['id'],)).fetchall()
```

```Shell
git checkout -b task3attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later if desired
git checkout task4            # switch to a branch to see the solution and be ready to start task 4
git diff task3 task4          # to see what has changed in creating the solution.
```

### Challenge 4: Add functionality for view_deputy_prime_ministers

1. Add hyperlink to nav bar "Deputy Prime Ministers"
2. Create a function `view_ministers(ministry=PRIME_MINISTER, page_title=None)` called by
         `view_prime_ministers()` and `view_deputy_prime_ministers()`

```Shell
git checkout -b task4attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later if desired
git checkout task5            # switch to a tag/branch to see the solution plus demo 5 and be ready to start task 5
git diff task4 task5          # to see what has changed in creating the solution plus demo 5. 
```

### Demo 5: Add a form to list_person.html so user can search on person's name

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
