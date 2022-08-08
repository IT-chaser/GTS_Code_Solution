import csv

#calls_file = input("Please provide a path to Calls text file: ")
#tours_file = input("Please provide a path to Tours text file: ")

calls_file = 'GTS_Code_Solution/Calls.txt'
tours_file = 'GTS_Code_Solution/Tours.txt'

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
        # Creates 'new_call' dictionary and appends it to 'calls_list' list
        new_call = {
            'timestamp': int(data[0]),
            'day': day,
            'id': int(data[1]), 
            'num_of_customers': int(data[2]), 
            'travel_days': int(data[3]),
            'budget': float(data[4])    
        }
        calls_list.append(new_call)  
    # Opens 'Tours.txt' file, reads each lines and returns 'tours' list 
    with open(tours_file) as f:
        content = f.readlines()
    tours = [x.strip() for x in content]
    # Creates 'new_tour' dictionary and appends it to 'tours_list' list
    u = 0
    for tour in tours:
        data = tour.split(',')
        new_tour = {
            'id': u,
            'timestamp': int(data[0]), 
            'name': data[1], 
            'start_day': int(data[2]), 
            'cost_per_day': int(data[3]),
            'capacity': int(data[4])    
        }
        tours_list.append(new_tour)
        u += 1
    # Creates simulation results
    mapping_list = []
    travel_call = []
    calls_list_copy = calls_list[:]
    # Looping through tours list first and calls second
    for tour in tours_list:
        for call in calls_list_copy:
            # Creating new mapping dictionary for call to tour mapping result
            map_dict = {
                'calls': calls[call['id']],
                'tours': tours[tour['id']],
                'day': call['day'],
                'tour_location': tour['name'],
                'call_id': f"{'[%s]' % ', '.join(map(str, travel_call))}",
                'capacity': tour['capacity'],
                'status': 'AVAILABLE'
            }
            # Checking if tour starts after call and tour capacity is higher or equal to number of customers
            if tour['start_day'] > call['day'] and tour['capacity'] >= call['num_of_customers']:
                # Checking if tour cost with all discounts is less or equal to customers' available budget
                if ((tour['cost_per_day'] * (1 - ((tour['start_day'] - call['day']) * 0.05))) * 
                        call['travel_days']) * call['num_of_customers'] <= call['budget']:
                    # If all above conditions are satisfied we decrease the tour capacity by number of customers
                    tour['capacity'] -= call['num_of_customers']
                    # If the tour capacity is not empty we update the result status to 'AVAILABLE' 
                    # and store call id in travel_call list
                    if tour['capacity'] :
                        travel_call.append(f"travel_call-{call['id']}")
                        map_dict['call_id'] = f"{'[%s]' % ', '.join(map(str, travel_call))}"
                        map_dict['capacity'] = tour['capacity']
                    else:
                        # if the capacity is empty then we update tour status to 'SOLD_OUT'
                        # and store all the call ids 
                        travel_call.append(f"travel_call-{call['id']}") 
                        map_dict['call_id'] = f"{'[%s]' % ', '.join(map(str, travel_call))}"
                        map_dict['capacity'] = tour['capacity']
                        map_dict['status'] = 'SOLD_OUT'
                    # After checking the each call we remove them from copied calls_list  
                    mapping_list.append(map_dict)
                    # We append every map_dict to new mapping_list    
                    calls_list_copy.remove(call)
        # Find out the tours where no suitable calls available
        if map_dict['capacity'] > 0 and map_dict['call_id'] == '[]':
            map_dict['call_id'] = '[NULL]'
            map_dict['calls'] = 'NULL'
            map_dict['day'] = 'NULL'
            map_dict['status'] = 'AVAILABLE: NO_SUITABLE_CALLS'
            mapping_list.append(map_dict)                 
        travel_call = []
    # We give the overall result in Solution.csv file format for convenience
    with open('GTS_Code_Solution/GTS_Code_Solution.csv', 'w', newline='') as csvfile:
        fieldnames = ['Requests', 'Tours', 'Call Day', 'Travel Call To Tour Mapping']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in mapping_list:
            writer.writerow({
                'Requests': f"[{item['calls']}]", 
                'Tours': f"[{item['tours']}]",
                'Call Day': item['day'],
                'Travel Call To Tour Mapping': f"({item['tour_location']}, {item['call_id']}, "
                        f"capacity: {item['capacity']}, {item['status']})"
            })    
    # We also displayed the results in the terminal window
    j = 0
    print("\n\t\t---- Calls That Successfully Registered To Available Tours ----\n")
    for a in mapping_list:
        print(f"{j}. Requests: [{a['calls']}], Tours: [{a['tours']}], Call Day: {a['day']}, Travel Call to Tour Mapping: "
            f"({a['tour_location']}, {a['call_id']}, capacity: {a['capacity']}, {a['status']})")
        j += 1
    print("\n\t\t---- Calls That Missed Their Chances ----\n")
    k = 0
    for call in calls_list_copy:
        print(f"Call ID: {call['id']}, Call Day: {call['day']}, Number of Customers: {call['num_of_customers']} "
            f"Travel Days: {call['travel_days']}, Budget: {call['budget']}")
        k += 1
    print(f"\n\t\t---- Overall {k} Calls Missed Their Chances ----\n")

# To ses the Simulation result we run the simulate_tour() function
simulate_tour()
