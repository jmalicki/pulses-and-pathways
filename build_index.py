import os

front_matter = """---
layout: default
---
<div class="title-page">
  <img src="title_page_sketch_1786259325961.jpg" alt="Pulses and Pathways" />
  <h1>Pulses and Pathways</h1>
  <h2>a Vascular Surgeon meets a Petroleum Engineer</h2>
</div>

<div class="preferred-presentation">
  Preferred Presentation: This play is designed to be experienced with the script on center stage, and educational technical slides projected to the right.
</div>

<hr>

"""

def parse_act_to_rows(markdown_content):
    lines = markdown_content.split('\n')
    
    html_output = []
    
    in_row = False
    in_text = False
    in_proj = False
    
    def start_row():
        nonlocal in_row, in_text
        html_output.append('<div class="stage-row" markdown="1">\n<div class="play-text" markdown="1">')
        in_row = True
        in_text = True
        
    def end_row():
        nonlocal in_row, in_text, in_proj
        if in_text:
            html_output.append('</div>')
            in_text = False
        if not in_proj:
            html_output.append('<div class="projections" markdown="1"></div>')
        html_output.append('</div>')
        in_row = False
        in_proj = False

    start_row()
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for image
        if line.startswith('!['):
            if in_text:
                html_output.append('</div>\n<div class="projections" markdown="1">')
                in_text = False
                in_proj = True
            html_output.append(line)
            i += 1
            continue
            
        # Check for Note / Lookaside
        if line.startswith('> [!NOTE]') or (line.startswith('>') and in_proj):
            if in_text:
                html_output.append('</div>\n<div class="projections" markdown="1">')
                in_text = False
                in_proj = True
            html_output.append(line)
            i += 1
            continue
            
        # If it's normal text but we are in projections, we need a new row
        if in_proj and line.strip() != "" and not line.startswith('>'):
            # End the current row and start a new one
            html_output.append('</div>\n</div>')
            in_proj = False
            
            html_output.append('<div class="stage-row" markdown="1">\n<div class="play-text" markdown="1">')
            in_text = True
            html_output.append(line)
            i += 1
            continue
            
        # Normal text in normal flow
        html_output.append(line)
        i += 1

    end_row()
    return '\n'.join(html_output)


with open("00_dedication.md", "r") as f:
    dedication = parse_act_to_rows(f.read())

with open("act_1_the_bedside_question.md", "r") as f:
    ch1 = f.read()
    ch1 = ch1.replace("## Act 1: The Bedside Question", "## Act 1: The Bedside Question\n\n![Exposure Sketch](exposure_sketch_1786259337787.jpg)\n\n")
    ch1_html = parse_act_to_rows(ch1)

with open("act_2_pressure_and_flow.md", "r") as f:
    ch2 = f.read()
    ch2 = ch2.replace("## Act 2: Pressure and Flow", "## Act 2: Pressure and Flow\n\n![Clamping Sketch](clamping_sketch_1786259348177.jpg)\n\n")
    ch2_html = parse_act_to_rows(ch2)

with open("act_3_living_pipes.md", "r") as f:
    ch3 = f.read()
    ch3 = ch3.replace("## Act 3: Living Pipes", "## Act 3: Living Pipes\n\n![Suturing Sketch](suturing_sketch_1786259361282.jpg)\n\n")
    ch3_html = parse_act_to_rows(ch3)

with open("act_4_inverse_problems.md", "r") as f:
    ch4 = f.read()
    ch4 = ch4.replace("## Act 4: Inverse Problems", "## Act 4: Inverse Problems\n\n![Doppler Sketch](doppler_sketch_1786259371250.jpg)\n\n")
    ch4 += "\n\n![Closure Sketch](closure_sketch_1786259427073.jpg)\n\n"
    ch4_html = parse_act_to_rows(ch4)

with open("index.md", "w") as out:
    out.write(front_matter)
    out.write(dedication + "\n\n<hr>\n\n")
    out.write(ch1_html + "\n\n<hr>\n\n")
    out.write(ch2_html + "\n\n<hr>\n\n")
    out.write(ch3_html + "\n\n<hr>\n\n")
    out.write(ch4_html + "\n\n")

print("Built two-pane index.md")
