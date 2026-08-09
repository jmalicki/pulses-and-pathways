import os

def insert_after(filename, search_text, insert_text):
    with open(filename, 'r') as f:
        content = f.read()
    
    if search_text in content and insert_text not in content:
        content = content.replace(search_text, search_text + "\n\n" + insert_text)
        with open(filename, 'w') as f:
            f.write(content)

# Act 1
insert_after('act_1_the_bedside_question.md', 
             ']*\n', 
             '![Exposure Sketch](exposure_sketch.png)')

# Act 2
insert_after('act_2_pressure_and_flow.md',
             'locks the teeth of a vascular clamp across the brachial artery branch. She watches the arterial monitor mounted on the anesthesia pole.]*',
             '![Clamping Sketch](clamping_sketch_1786259348177.jpg)')

# Act 3
insert_after('act_3_living_pipes.md',
             '[Dr. Hayes is suturing the vessel under magnification.]*',
             '![Suturing Sketch](suturing_sketch_1786259361282.jpg)')

# Act 4 (assuming there are places for doppler and closure)
insert_after('act_4_inverse_problems.md',
             'Doppler', # simplistic fallback
             '![Doppler Sketch](doppler_sketch_1786259371250.jpg)')
insert_after('act_4_inverse_problems.md',
             'closure', # simplistic fallback
             '![Closure Sketch](closure_sketch_1786259427073.jpg)')
