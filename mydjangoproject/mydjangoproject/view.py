from django.http import HttpResponse
import json
global emp_record
global candidate_record
global date_slot
from django.views.decorators.csrf import csrf_exempt
import os

emp_record = {}
#emp_record_file = {}
date_slot = {}
#date_slot_file = {}
candidate_record = {}
#candidate_record_file = {}
allowed_client_type = ["emp","candidate"]

date_slot_file_path = os.path.join("mydjangoproject","date_slot.json")
time_slot_cand_file_path = os.path.join("mydjangoproject","time_slot_cand.json")
time_slot_emp_file_path = os.path.join("mydjangoproject","time_slot_emp.json")

@csrf_exempt
def process_data(request):
    reg_success = 0
    client_slot = []
    if "id" in request.GET and "ts" in request.GET and "client_type" in request.GET and "date" in request.GET:
        client_id = request.GET['id']
        date_slot =read_json_file(date_slot_file_path)

        if("," in request.GET['date']):
            client_date_slot = request.GET['date'].split(",")
        else:
            client_date_slot = list(request.GET['date'])

        date_slot[client_id] = client_date_slot
        print(date_slot)
        write_json_file(date_slot_file_path,date_slot)
        if(len(client_date_slot) > 1 and  '$' in request.GET['ts']  ):
            client_slot_bucket =(request.GET['ts']).split("$")
            for elements in client_slot_bucket:
                print(elements)
                client_slot.append(elements.split(','))
        else:
            client_slot = request.GET['ts'].split(',')




        if(request.GET['client_type'] in allowed_client_type):
            if(request.GET['client_type']  == "emp"):

                emp_record = read_json_file(time_slot_emp_file_path)

                emp_record[client_id] = client_slot

                write_json_file(time_slot_emp_file_path,emp_record)
                #print(emp_record)
                #print(date_slot)
            elif(request.GET['client_type'] == "candidate" ):

                candidate_record = read_json_file(time_slot_cand_file_path)

                candidate_record[client_id] = client_slot

                write_json_file(time_slot_cand_file_path,candidate_record)

            return HttpResponse("{\"REGISTRATION\" : \"SUCCESS\"}")
        else:
            return HttpResponse("{\"REGISTRATION\" : \"INVALID_CANDIDATE_TYPE\"}")


    else:
        return HttpResponse("{\"REGISTRATION\" : \"INVALID PARAMS\"}")

def read_json_file(file_name):
    file_obj = open(file_name,'r')
    json_data = json.load(file_obj)
    print(json_data)
    file_obj.close()
    return json_data

def write_json_file(filename,input_data):
    file_obj = open(filename,'w')
    print(type(input_data))
    json.dump(input_data,file_obj)
    file_obj.close()

def fetch_time(record_1,record_2 ):
    available_time_slots = []
    print(record_1)
    print(record_2)
    for i in range(int(record_1[0]),int(record_1[1])):
        for j in range(int(record_2[0]),int(record_2[1])):
            if(i == j):
                available_time_slots.append(i)
                continue

    #print(available_time_slots)
    return available_time_slots

def process_input_data(emp_id,candidate_id):
    central_available_time_slot = {}
    date_slot = read_json_file(date_slot_file_path)
    #print(date_slot)
    invalid_data = {"STATUS":"INVALID KEYS "}
    emp_record = read_json_file(time_slot_emp_file_path)
    #print(emp_record)
    candidate_record = read_json_file(time_slot_cand_file_path)
    #print(candidate_record)
    #print(date_slot)
    if emp_id in emp_record.keys() and candidate_id in candidate_record.keys():
        for dates in date_slot[emp_id]:
            #print("in readjson")

            for candidates in date_slot[candidate_id]:
                if( dates == candidates):
                    data = fetch_time( emp_record[emp_id][date_slot[emp_id].index(dates)],candidate_record[candidate_id][date_slot[candidate_id].index(dates)])
                    central_available_time_slot[dates] = data
                    print(data)
                    continue

        print(central_available_time_slot)
        return central_available_time_slot
    else:
        return(invalid_data)


@csrf_exempt
def fetch_time_slot(request):
    #try:

    if "emp_id"in request.GET and "candidate_id" in request.GET:
        #pass


        data = process_input_data(request.GET['emp_id'],request.GET['candidate_id'])

    return  HttpResponse(json.dumps(data))
    """
    except Exception as e :
        print(e)
        return HttpResponse("{\"STATUS \" : \"INVALID  INPUTS\"}")
    """
@csrf_exempt
def test_post(request):
    print("in the statement")
    k = request.POST.get("cr")
    return HttpResponse(k)
