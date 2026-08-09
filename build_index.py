import os

front_matter = """---
layout: default
---
<div class="title-page">
  <img src="title_page_sketch_1786259325961.jpg" alt="Pulses and Pathways" />
  <h1>Pulses and Pathways</h1>
  <h2>a Vascular Surgeon meets a Petroleum Engineer</h2>
</div>

<hr>

"""

with open("00_dedication.md", "r") as f:
    dedication = f.read()

with open("chapter_1_the_bedside_question.md", "r") as f:
    ch1 = f.read()
    ch1 = ch1.replace("## Chapter 1: The Bedside Question", "## Chapter 1: The Bedside Question\n\n![Exposure Sketch](exposure_sketch_1786259337787.jpg)\n\n")

with open("chapter_2_pressure_and_flow.md", "r") as f:
    ch2 = f.read()
    ch2 = ch2.replace("## Chapter 2: Pressure and Flow", "## Chapter 2: Pressure and Flow\n\n![Clamping Sketch](clamping_sketch_1786259348177.jpg)\n\n")

with open("chapter_3_living_pipes.md", "r") as f:
    ch3 = f.read()
    ch3 = ch3.replace("## Chapter 3: Living Pipes", "## Chapter 3: Living Pipes\n\n![Suturing Sketch](suturing_sketch_1786259361282.jpg)\n\n")

with open("chapter_4_inverse_problems.md", "r") as f:
    ch4 = f.read()
    ch4 = ch4.replace("## Chapter 4: Inverse Problems", "## Chapter 4: Inverse Problems\n\n![Doppler Sketch](doppler_sketch_1786259371250.jpg)\n\n")
    ch4 += "\n\n![Closure Sketch](closure_sketch_1786259427073.jpg)\n\n"

with open("index.md", "w") as out:
    out.write(front_matter)
    out.write(dedication + "\n\n<hr>\n\n")
    out.write(ch1 + "\n\n<hr>\n\n")
    out.write(ch2 + "\n\n<hr>\n\n")
    out.write(ch3 + "\n\n<hr>\n\n")
    out.write(ch4 + "\n\n")
