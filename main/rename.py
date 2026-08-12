import os

files = [
    "chapter_1_the_bedside_question.md",
    "chapter_2_pressure_and_flow.md",
    "chapter_3_living_pipes.md",
    "chapter_4_inverse_problems.md"
]

for f in files:
    with open(f, "r") as file:
        content = file.read()
    
    # Replace the dialogue tags and character list names
    content = content.replace("**DR. HAYES**", "**DR. SARAH HAYES**")
    
    with open(f, "w") as file:
        file.write(content)

print("Renamed Dr. Hayes to Dr. Sarah Hayes in all chapters.")
