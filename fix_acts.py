import re
import os

files = ["act_2_pressure_and_flow.md", "act_3_living_pipes.md", "act_4_inverse_problems.md"]

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # Remove the Characters section which looks something like:
    # **CHARACTERS:**
    # ...
    # ...
    # ---
    content = re.sub(r'\*\*CHARACTERS:\*\*.*?\-\-\-\n\n', '', content, flags=re.DOTALL)
    
    # Replace local anesthetic/anesthesia with regional block
    content = content.replace("under local anesthetic", "under a regional block")
    content = content.replace("under local anesthesia", "under a regional block")
    
    with open(file, 'w') as f:
        f.write(content)

print("Fixed character lists and anesthetic terminology.")
