# timetable-RESTApi
A flask REST Api which parses a timetable given as excel file to json data and serves on requests by user.

## Dependencies
 * flask
 * pandas
 * json
 
 ## Installation
 
 * A virtual environment is recommended to separate all the server related dependencies from local dependencies.
 ```
 $ python -m venv env
 ```
 
 * Install all the dependencies from requirements.txt
 ```
 $ pip install -r requirements.txt
 ```
 
 ## Usage
 * Run the server as follows
 ```
 $ python app.py
 ```
 This will setup a local server on http://127.0.0.1:5000/
 
 * Json request structure
 ```
 {
  "batch" : "your batch",
  "day" : "timetable of day to parse",
  "enrolled_courses" : ['List of enrolled courses']
}
 ```
 * Use curl to post the request to server on http://127.0.0.1:5000/jiit/timetable
 ```
 $ curl -d request.json -X POST "http://127.0.0.1:5000/jiit/timetable"
 ```
 * Json Response structure
 ```
 {
  "result" : ['List of time-wise timetable data dict']
 }
 
 timetable-data-dict structure
 {
  "course" : "Course at that time",
  "faculty" : "Faculty taking the course",
  "room" : "Room in which it has been scheduled",
  "time" : "Scheduled time",
  "type" : "Type of teaching method Lecture/Tut/Practicle(Dict with duration)"
 }
 
 teaching type dict structure
 {
  "category" : "teaching type",
  "time" : "duration"
 }
 ```
 
 ## To-Do
 
 - [x] A static python script to parse the excel file using pandas.
 - [x] A flask server to handle dynamic requests.
 - [x] Deploy server to Heroku.
 - [ ] Flutter app to add UI.
