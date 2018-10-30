import sys
import re

# The python file requires 3 arguments
if len(sys.argv) != 4:
    raise Exception('The python file requires exactly 3 arguments')
    
in_file = sys.argv[1]
occupation_out_file = sys.argv[2]
state_out_file = sys.argv[3]

# We keep track of occupation name counts and state counts using dicts
occupation_counter = {}
state_counter = {}
total_certified = 0.0

with open(in_file) as f:
    for i, line in enumerate(f):
        
        # Split with semi-colon as the delimiter
        fields = line.split(';')
        
        # Header row
        if i==0:
            # The field names can change based on year. So we check for all the know aliases as well.
            occupation_field_index = [fields.index(field) for field in fields if field in {'SOC_NAME', 'LCA_CASE_SOC_NAME'}][0]
            certified_field_index = [fields.index(field) for field in fields if field in {'CASE_STATUS', 'STATUS'}][0]
            state_field_index = [fields.index(field) for field in fields if field in {'WORKSITE_STATE', 'LCA_CASE_WORKLOC1_STATE'}][0]
        # If not header
        else:
            # we should process only certified rows
            if fields[certified_field_index] == 'CERTIFIED':
                
                # Retrieve occupation and state and clean it up
                occupation = re.sub(r'\"', '', fields[occupation_field_index])
                state = re.sub(r'\n', '', fields[state_field_index])
                
                total_certified += 1.0
                
                # Add to occupation counter
                if occupation in occupation_counter:
                    occupation_counter[occupation] += 1
                else:
                    occupation_counter[occupation] = 1
                    
                # Add to state counter
                if state in state_counter:
                    state_counter[state] += 1
                else:
                    state_counter[state] = 1

# Now we need to sort the counts based on the count(descending) and the occupation name (ascending)                
occupation_tuples = sorted(occupation_counter.items(), key = lambda x: (-x[1], x[0]))

# We will now write only the top 10 records after sorting
with open(occupation_out_file, 'w') as f:  
    f.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
    for occupation, num in occupation_tuples[:10]:
        f.write( '{};{};{:.1%}\n'.format(occupation, num, num/total_certified) )

# Similarly for states
state_tuples = sorted(state_counter.items(), key = lambda x: (-x[1], x[0]))

with open(state_out_file, 'w') as f:  
    f.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
    for state, num in state_tuples[:10]:
        f.write( '{};{};{:.1%}\n'.format(state, num, num/total_certified) )
        
