#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetUp 040 - Beginners Python Support Sessions - Wed 11 Dec 2019 - flask web applications

Learning objectives:
    Use git to checkout source and move between tagged snapshots
    Create a web application using flask and sqlite3

@author D Tim Cummings
"""
# I have put commands to be typed in Terminal or Bash in triple-singled quoted strings to ease copy-pasting.
'''
git clone https://github.com/timcu/bpss-prime-minister.git  # copy repository from github to your computer
cd bpss-prime-minister                                      # change directory into the project directory
git checkout task1                                          # start project with flask boilerplate code ready for task 1
'''

# Challenge 1: Add a page for view_prime_ministers
#     a. Create a template called list_minister.html which currently shows <h2>People who have held this ministry</h2>
#     b. Create a function view_prime_ministers() which calls render_template("list_minister.html") with suitable title
#     c. Add hyperlink to nav bar
'''
git checkout -b task1attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later if desired
git checkout task1soln        # switch to a tag/branch to see the solution
git diff task1 task1soln      # to see what has changed in creating the solution
git checkout task2            # to get ready for doing task 2
'''

# Demo 2:
#     a. Create a run configuration to init-db
#     b. list all prime ministers in a table

# Challenge 2: List all people in database in list_person.html
#     a. Add sql to prime_minister.view_persons() function and pass results to render_template
#     b. Create a table in list_person.html with a loop to repeat the rows
'''
git checkout -b task2attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later if desired
git checkout task3            # switch to a tag/branch to see the solution and be ready to start task 3
git diff task2 task3          # to see what has changed in creating the solution. <space> to page. q to quit
'''

# Challenge 3: Show list of recreations in view_person.html
#     a. tbl_recreation has a foreign key 'id_person' which joins to tbl_person 'id'
#     b. tbl_recreation has a varchar field 'vc_recreation' which contains the name of the recreation
#     c. Add sql in prime_minister.view_person(id_person) to find the list of recreations
#     d. Pass the list of recreations to render_template('view_person.html')
#     e. Modify view_person.html to list any recreations
'''
git checkout -b task3attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later if desired
git checkout task4            # switch to a tag/branch to see the solution and be ready to start task 4
git diff task3 task4          # to see what has changed in creating the solution.
'''

# Challenge 4: Add functionality for view_deputy_prime_ministers
#     a. Add hyperlink to nav bar "Deputy Prime Ministers"
#     b. Create a function view_ministers(ministry=PRIME_MINISTER, page_title=None) called by
#         view_prime_ministers() and view_deputy_prime_ministers()
'''
git checkout -b task4attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later if desired
git checkout task5            # switch to a tag/branch to see the solution plus demo 5 and be ready to start task 5
git diff task4 task5          # to see what has changed in creating the solution plus demo 5. 
'''

# Demo 5: Add a form to list_person.html so user can search on person's name
#
# Challenge 5: Add authentication to application so users can log in.
#     a. Table already exists in database
#     b. Follow instructions in tutorial at http://flask.pocoo.org/docs/1.0/tutorial/views/
#     c. Table is tbl_user with fields (id, vc_username, vc_password)
#        Table in tutorial is user with fields (id, username, password)
'''
git checkout -b task5attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later
git checkout task6            # switch to a tag/branch to see the solution and be ready to start task 6
git diff task5 task6          # to see what has changed in creating the solution. 
'''

# Challenge 6: Keep search form populated after clicking search button
'''
git checkout -b task6attempt  # create a branch to save your attempt
git commit -a -m "my attempt" # save your changes to this branch so they can be retrieved later
git diff task6 task6soln      # to see what has changed in creating the solution. 
'''
