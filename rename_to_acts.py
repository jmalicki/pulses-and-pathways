import os

files = {
    "chapter_1_the_bedside_question.md": "act_1_the_bedside_question.md",
    "chapter_2_pressure_and_flow.md": "act_2_pressure_and_flow.md",
    "chapter_3_living_pipes.md": "act_3_living_pipes.md",
    "chapter_4_inverse_problems.md": "act_4_inverse_problems.md"
}

# Use git mv to rename files
for old, new in files.items():
    os.system(f"git mv {old} {new}")
    
    # Read and replace text
    with open(new, "r") as f:
        content = f.read()
    
    # E.g. "Chapter 1: The Bedside Question" -> "Act 1: The Bedside Question"
    content = content.replace("Chapter 1", "Act 1")
    content = content.replace("Chapter 2", "Act 2")
    content = content.replace("Chapter 3", "Act 3")
    content = content.replace("Chapter 4", "Act 4")
    
    with open(new, "w") as f:
        f.write(content)

# Update build_index.py
with open("build_index.py", "r") as f:
    build_script = f.read()

build_script = build_script.replace("chapter_", "act_")
build_script = build_script.replace("Chapter", "Act")

with open("build_index.py", "w") as f:
    f.write(build_script)

print("Renamed Chapters to Acts.")
