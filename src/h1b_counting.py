import sys
import re

in_file = sys.argv[1]
occupation_out_file = sys.argv[2]
state_out_file = sys.argv[3]
onet_file = sys.argv[4]
soc_file = sys.argv[5]

occupation_name_counter = {}
state_counter = {}
total_certified = 0.0

# Create a dict of onet_code to soc_name
onet_to_name = {}
with open(onet_file, encoding='utf8') as f:
    for line in f:
        onet_code, name = line.strip().split(';')
        onet_to_name[onet_code] = name.upper()

# Create a dict of soc_code to soc_name
soc_to_name = {}
with open(soc_file, encoding='utf8') as f:
    for line in f:
        soc_code, name = line.strip().split(';')
        soc_to_name[soc_code] = name.upper()
        

with open(in_file, encoding='utf8') as f:
    for i, line in enumerate(f):
        fields = line.split(';')
        
        if i==0:
            occupation_code_field_index = [fields.index(field) for field in fields if field in {'SOC_CODE', 'LCA_CASE_SOC_CODE'}][0]
            occupation_name_field_index = [fields.index(field) for field in fields if field in {'SOC_NAME', 'LCA_CASE_SOC_NAME'}][0]
            certified_field_index = [fields.index(field) for field in fields if field in {'CASE_STATUS', 'STATUS'}][0]
            state_field_index = [fields.index(field) for field in fields if field in {'WORKSITE_STATE', 'LCA_CASE_WORKLOC1_STATE'}][0]
            relevant_field_indices = [
                                        occupation_code_field_index,
                                        state_field_index
                                     ]
        else:
            if fields[certified_field_index] == 'CERTIFIED':
                occupation_code = re.sub(r'\"', '', fields[occupation_code_field_index])
                
                occupation_name = re.sub(r'\"', '', fields[occupation_name_field_index]).upper()
                if occupation_code in soc_to_name.keys():
                    occupation_name = soc_to_name[occupation_code]
                elif occupation_code in onet_to_name.keys():
                    occupation_name = onet_to_name[occupation_code]
                
                state = re.sub(r'\n', '', fields[state_field_index])
                
                total_certified += 1.0
                
                if occupation_name in occupation_name_counter:
                    occupation_name_counter[occupation_name] += 1
                else:
                    occupation_name_counter[occupation_name] = 1
                    
                if state in state_counter:
                    state_counter[state] += 1
                else:
                    state_counter[state] = 1

                   
occupation_tuples = sorted(occupation_name_counter.items(), key = lambda x: (-x[1], x[0]))

with open(occupation_out_file, 'w') as f:  
    f.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
    for occupation_name, num in occupation_tuples[:10]:
        f.write( '{};{};{:.1%}\n'.format(occupation_name, num, num/total_certified) )

state_tuples = sorted(state_counter.items(), key = lambda x: (-x[1], x[0]))

with open(state_out_file, 'w') as f:  
    f.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
    for state, num in state_tuples[:10]:
        f.write( '{};{};{:.1%}\n'.format(state, num, num/total_certified) )
