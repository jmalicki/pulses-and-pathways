import os

def parse_chapter_to_rows(markdown_content):
    lines = markdown_content.split('\n')
    
    html_output = []
    
    in_row = False
    in_text = False
    in_proj = False
    
    def start_row():
        nonlocal in_row, in_text
        if not in_row:
            html_output.append('<stage-row>\n<play-text>\n<div markdown="1">\n')
            in_row = True
            in_text = True
        
    def end_row():
        nonlocal in_row, in_text, in_proj
        if in_row:
            if in_text:
                html_output.append('</div>\n</play-text>')
                in_text = False
            if in_proj:
                html_output.append('</div>\n</projections>')
                in_proj = False
            else:
                html_output.append('<projections></projections>')
            html_output.append('</stage-row>')
            in_row = False

    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Explicit stage-row break (no visible rule)
        if line.strip() == '<!-- stage-break -->':
            end_row()
            i += 1
            continue

        # Headers and dividers break the layout completely
        if line.startswith('#') or line.startswith('---') or line.startswith('<div class="preferred'):
            end_row()
            html_output.append(line)
            i += 1
            continue
            
        # Closing div for preferred-presentation breaks layout too
        if line.startswith('</div>') and not in_row:
            html_output.append(line)
            i += 1
            continue
            

        # Check for image
        if line.startswith('!['):
            start_row()
            if in_text:
                html_output.append('</div>\n</play-text>\n<projections>\n<div markdown="1">\n')
                in_text = False
                in_proj = True
            html_output.append(line)
            i += 1
            continue
            
        # Check for Note / Lookaside
        if line.startswith('> [!NOTE]'):
            start_row()
            if in_text:
                html_output.append('</div>\n</play-text>\n<projections>\n<div markdown="1">\n')
                in_text = False
                in_proj = True

            html_output.append('<div class="note-alert">\n')
            i += 1  # Skip the > [!NOTE] line
            while i < len(lines) and lines[i].startswith('>'):
                content = lines[i][1:]
                if content.startswith(' '):
                    content = content[1:]
                import re
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
                html_output.append(f'<p>{content}</p>\n')
                i += 1
            html_output.append('</div>\n')
            continue
            
        # If it's normal text but we are in projections, we need a new row
        if in_proj and line.strip() != "" and not line.startswith('>'):
            end_row()
            start_row()
            html_output.append(line)
            i += 1
            continue
            
        # Normal text in normal flow
        if line.strip() != "" and not in_row:
            start_row()
            
        html_output.append(line)
        i += 1

    end_row()
    return '\n'.join(html_output)

title_page_md = """
<div class="title-page" markdown="1">

# Pulses and Pathways

## a Vascular Surgeon meets a Petroleum Engineer

<div class="preferred-presentation">
  Preferred Presentation: This play is designed to be experienced with the script on center stage, and educational technical slides projected to the right.
</div>

![Title Page](title_page_sketch_1786259325961.jpg)

</div>
"""

with open("00_dedication.md", "r") as f:
    dedication = f'<div class="title-page" markdown="1">\n\n{f.read()}\n\n</div>'

with open("act_1_the_bedside_question.md", "r") as f:
    ch1_html = parse_chapter_to_rows(f.read())

with open("act_2_pressure_and_flow.md", "r") as f:
    ch2_html = parse_chapter_to_rows(f.read())

with open("act_3_the_network.md", "r") as f:
    ch3_html = parse_chapter_to_rows(f.read())

with open("act_3_living_pipes.md", "r") as f:
    ch4_html = parse_chapter_to_rows(f.read())

with open("act_4_inverse_problems.md", "r") as f:
    ch5_html = parse_chapter_to_rows(f.read())

with open("index.md", "w") as out:
    out.write("---\nlayout: default\n---\n")
    out.write(title_page_md + "\n\n")
    out.write(dedication + "\n\n<hr>\n\n")
    out.write(ch1_html + "\n\n<hr>\n\n")
    out.write(ch2_html + "\n\n<hr>\n\n")
    out.write(ch3_html + "\n\n<hr>\n\n")
    out.write(ch4_html + "\n\n<hr>\n\n")
    out.write(ch5_html + "\n\n")

print("Built five-act index.md")
