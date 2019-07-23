from flask import Flask , request , jsonify
from flask_restful import Resource , Api
import json
import pandas as pd

app = Flask(__name__)
api = Api(app)


########

xlsx_df = pd.read_excel('timetable/B.TECH V sem.xlsx' , header=1)
course_desc = xlsx_df[xlsx_df['9 -9.50 AM'] == 'NOTE: COURSE CODES MENTIONED IN THE TIMETABLE ABOVE SHOULD BE READ AS FOLLOWING'].index[0]
monday = xlsx_df[xlsx_df['Unnamed: 0'] == 'MON'].index[0]
tuesday = xlsx_df[xlsx_df['Unnamed: 0'] == 'TUES'].index[0]
wednesday = xlsx_df[xlsx_df['Unnamed: 0'] == 'WED'].index[0]
thursday = xlsx_df[xlsx_df['Unnamed: 0'] == 'THUR'].index[0]
friday = xlsx_df[xlsx_df['Unnamed: 0'] == 'FRI'].index[0]
saturday = xlsx_df[xlsx_df['Unnamed: 0'] == 'SAT'].index[0]
monday_df = xlsx_df[:tuesday].drop(columns=['Unnamed: 0' , '12 NOON-12.50 PM'])
tuesday_df = xlsx_df[tuesday:wednesday].drop(columns=['Unnamed: 0' , '12 NOON-12.50 PM'])
wednesday_df = xlsx_df[wednesday:thursday].drop(columns=['Unnamed: 0' , '12 NOON-12.50 PM'])
thursday_df = xlsx_df[thursday:friday].drop(columns=['Unnamed: 0' , '12 NOON-12.50 PM'])
friday_df = xlsx_df[friday:saturday].drop(columns=['Unnamed: 0' , '12 NOON-12.50 PM'])
saturday_df = xlsx_df[saturday:course_desc].drop(columns=['Unnamed: 0' , '12 NOON-12.50 PM'])

dataframe_map = {
  'monday' : monday_df,
  'tuesday' : tuesday_df,
  'wednesday' : wednesday_df,
  'thursday' : thursday_df,
  'friday' : friday_df,
  'saturday' : saturday_df,
}

with open('courses/courses.json') as fp:
    course_map = json.load(fp)

########

day_map = {
    'monday' : 0,
    'tuesday' : 1,
    'wednesday' : 2,
    'thursday' : 3,
    'friday' : 4,
    'saturday' : 5,
}

teaching_type = {
    'L' : {
        'category' : 'Lecture',
        'time' : 1
    },
    'T' : {
        'category' : 'Tutorial',
        'time' : 1
    },
    'P' : {
        'category' : 'Practical',
        'time' : 2
    }
}

batch_size_utility = {
    'A' : 10,
    'B' : 14,
    'C' : 3
}

def extract_buffer(unstable_batch_list):
  batch_buffers = {
    'A' : [],
    'B' : [],
    'C' : []
  }
  curr_batch = ''
  for it in unstable_batch_list:
    start_index = 0
    end_index = 0
    if(it[0] == 'A' or it[0] == 'B' or it[0] == 'C'):
      curr_batch = it[0]
      if len(it) > 1 :
        batch_nos = it[1:]
      else:
        batch_nos = curr_batch
      if(batch_nos[0] == 'A' or batch_nos[0] == 'B' or batch_nos[0] == 'C'):
        for bat in it:
          for i in range(1 , batch_size_utility[bat] + 1):
            batch_buffers[bat].append(i)
      else:
        bounded_batch = batch_nos.split('-')
        if len(bounded_batch) == 2:
          start_index = int(bounded_batch[0])
          end_index = int(bounded_batch[1])
        else:
          end_index = int(bounded_batch[0])
          start_index = end_index
        for i in range(start_index , end_index + 1):
          batch_buffers[curr_batch].append(i)

    else:
      batch_nos = it
      bounded_batch = batch_nos.split('-')
      if len(bounded_batch) == 2:
        start_index = int(bounded_batch[0])
        end_index = int(bounded_batch[1])
      else:
        end_index = int(bounded_batch[0])
        start_index = end_index
      for i in range(start_index , end_index + 1):
        batch_buffers[curr_batch].append(i)
  
  return batch_buffers

def parse_batch_details(batches):
  teach_method = teaching_type[batches[0]]
  batches = batches[1:]
  unstable_batch_list = batches.split(',')
  batch_buffers = extract_buffer(unstable_batch_list)
  return batch_buffers , teach_method

def timetable_api_v1(day , batch_full , enrolled_courses):
  batch_abb = batch_full[0]
  batch_no = int(batch_full[1:])
  timing = []
  for label , item in dataframe_map[day].iteritems():
    item_list = item.tolist()
    for data in item_list:
      data_list = {}
      flag = False
      if str(data) != 'nan':
        data = data.replace('((' , '(').replace('+' , ',').split('(')
        batches = data[0]
        buffered_data , teach_method = parse_batch_details(batches)
        residue = data[1].split(')')
        course = residue[0]
        residue = residue[1].split('/')
        faculty = residue[1]
        room = residue[0][1:]
        flag = course in enrolled_courses
        if((batch_no in buffered_data[batch_abb]) and flag):
          data_list['course'] = [key for key , value in course_map.items() if value == course][0]
          data_list['faculty'] = faculty
          data_list['room'] = room
          data_list['time'] = int(label.split('-')[0])
          data_list['type'] = teaching_type[batches[0]]
          timing.append(data_list)
          
  return timing

class TimetableApi(Resource):
    def post(self):
        data = request.get_json()
        tables = timetable_api_v1(data['day'] , data['batch'] , data['enrolled_courses'])
        return {'result' : tables} , 201

api.add_resource(TimetableApi , '/')

if __name__ == '__main__':
    app.run(host='192.168.1.201',debug=False)