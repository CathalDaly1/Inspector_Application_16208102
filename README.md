# Inspector_Application 
## Developed By Cathal Daly - 16208102
PYTHON VERSION: 3.7.4

Inspector is a grading application that will be used by Lecturers in the University of Limerick. 
The main aim of this final year project is to increase the turn-around time in the grading process for lecturers.
This application will focus on the speed at which assignments can be graded. This will be achieved using pre-programmed
keys on the computer which will represent grades and also keys which will allow the lecturer to access main menu and 
other features in the application. 

*TO BEGIN GRADING*
1). Create a folder on your File System which will contain a folder for each student in the class for that particular module. 
2). The name of the folder for each student must be their STUDENT ID Number. 
3). Place the students assignments in their respective folder in order to begin grading.
4). On the 'FileAccessScreen' in the Inspector Application:
    4a). Enter the Module Code that is associated with these assignments being graded
    4b). Enter the Assignment number that is associated with these assignments being graded
    4c). Enter the FilePath where the students folders are located 
        4ci). E.g, Folder /16208102/Assignment.py is located in (C:\Users\OneDrive\Assignments)
        So you would enter 'C:\Users\OneDrive\Assignments' in order to display all students folders with assignments
5). Enter values for Keystokes which will be used for assigning marks to each student
6). Enter comments which will be associated with each key value ]#
7). Enter Canned comments if necessary
8). Enter Grading Categories if necessary
9). Select assignment by 'Double Clicking' on folder name in listbox and then 'clicking' the file name
10). Click 'select assignment' button and begin grading. 


*PostgreSQL database with Heroku Server - Credentials are as follows*
Host: ec2-54-217-204-34.eu-west-1.compute.amazonaws.com
Database: d7tfsem11o8afc
User: hjzzzxkldardcd
Port: 5432
Password: 7e4dd09652f3fafaa1f8af3701b741f8c4563ba06e1ea643670d82c758b8c493
URI: postgres://hjzzzxkldardcd:7e4dd09652f3fafaa1f8af3701b741f8c4563ba06e1ea643670d82c758b8c493@ec2-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/d7tfsem11o8afc
Heroku CLI: heroku pg:psql postgresql-objective-79505 --app inspector-server

