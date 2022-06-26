import csv

calls_file = 'GTSystem_solution/Calls.txt'
tours_file = 'GTSystem_solution/Tours.txt'

def simulate_tour():
    """Display Call to Tour Simulation"""   
    calls_list = []
    tours_list = []

    # Opens 'Calls.txt' file, reads each lines and returns 'calls' list 
    with open(calls_file) as f:
        content = f.readlines()
    calls = [x.strip() for x in content]

    # Transforms given timestamps into days
    t = 10
    for call in calls:
        data = call.split(',')
        data_0 = int(data[0])
        if data_0 < t:
            day = 1
        elif data_0 > t & data_0-t != 10:
            day = int(data_0/10) + 1
        elif data_0 - t >= 10:
            t += 10     

        # Creates 'new_call' dictionary and appends it to 'calls_list'
        new_call = {
            'timestamp': int(data[0]),
            'day': day,
            'id': int(data[1]), 
            'num_of_customers': int(data[2]), 
            'travel_days': int(data[3]),
            'budget': int(data[4])    
        }
        calls_list.append(new_call)
    
    # Opens 'Tours.txt' file, reads each lines and returns 'tours' list 
    with open(tours_file) as f:
        content = f.readlines()
    tours = [x.strip() for x in content]
    i = 0
    for tour in tours:
        data = tour.split(',')
        new_tour = {
            'id': i,
            'timestamp': int(data[0]), 
            'name': data[1], 
            'start_day': int(data[2]), 
            'cost_per_day': int(data[3]),
            'capacity': int(data[4])    
        }
        tours_list.append(new_tour)
        i += 1

    new_list = []
    calls_list_copy = calls_list[:]
    for tour in tours_list:
        for call in calls_list_copy:
            if tour['start_day'] > call['day'] and tour['capacity'] >= call['num_of_customers']:
                if ((tour['cost_per_day'] * (1 - ((tour['start_day'] - call['day']) * 0.05))) * call['travel_days']) <= call['budget']:
                    tour['capacity'] -= call['num_of_customers']
                    if tour['capacity'] > 0 :
                        new_dict = {
                            'calls': calls[call['id']],
                            'tours': tours[tour['id']],
                            'day': call['day'],
                            'tour_location': tour['name'],
                            'call_id': call['id'],
                            'capacity': tour['capacity'],
                            'status': 'AVAILABLE'
                        }
                    else:
                        new_dict = {
                            'calls': calls[call['id']],
                            'tours': tours[tour['id']],
                            'day': call['day'],
                            'tour_location': tour['name'],
                            'call_id': call['id'],
                            'capacity': tour['capacity'],
                            'status': 'SOLD OUT'
                        }
                    calls_list_copy.remove(call)
                            
                    new_list.append(new_dict)

    with open('GTSystem_solution/Solution.csv', 'w', newline='') as csvfile:
        fieldnames = ['Requests', 'Tours', 'Call Day', 'Travel Call To Tour Mapping']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in new_list:
            writer.writerow({
                'Requests': f"[{item['calls']}]", 
                'Tours': f"[{item['tours']}]",
                'Call Day': item['day'],
                'Travel Call To Tour Mapping': f"[{item['tour_location']}, travel_cal-{item['call_id']}, "
                        f"capacity: {item['capacity']}, {item['status']}]"
            })
            
    
    """j = 0
    print("\n\t\t---- Calls That Successfully Registered To Available Tours ----\n")
    for a in new_list:
        print(f"Result: {j}, Requests: [{a['calls']}], Tours: [{a['tours']}], Call Day: {a['day']}, Travel Call to Tour Mapping: [{a['tour_location']}, "
            f"travel_call-{a['call_id']}, capacity: {a['capacity']}, {a['status']}]")
        j += 1
    print("\n\t\t---- Calls That Missed Their Chances ----\n")
    k = 0
    for call in calls_list_copy:
        print(f"Call ID: {call['id']}, Call Day: {call['day']}, Number of Customers: {call['num_of_customers']} "
            f"Travel Days: {call['travel_days']}, Budget: {call['budget']}")
        k += 1
    print(f"\n\t\t---- Overall {k} Calls Missed Their Chances ----\n") """

simulate_tour()
