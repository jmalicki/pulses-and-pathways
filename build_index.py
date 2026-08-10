import os
import re


def parse_chapter_to_rows(markdown_content):
    """Build stage-rows that keep dialogue with its matching projection.

    Play text and projections (images + notes) stay in the same row until:
    - an explicit break (heading, ---, <!-- stage-break -->), or
    - a new image arrives after projections already have content (new visual beat).
    """
    lines = markdown_content.split('\n')
    html_output = []

    play_buf = []
    proj_buf = []
    projections_end = False

    def flush_row():
        nonlocal play_buf, proj_buf, projections_end
        # Skip entirely empty rows
        if not any(s.strip() for s in play_buf) and not proj_buf:
            play_buf = []
            proj_buf = []
            projections_end = False
            return

        row_class = ' class="projections-end"' if projections_end else ''
        html_output.append(f'<stage-row{row_class}>\n')
        html_output.append('<play-text>\n<div markdown="1">\n')
        html_output.extend(play_buf)
        if play_buf and not play_buf[-1].endswith('\n'):
            html_output.append('\n')
        html_output.append('</div>\n</play-text>\n')

        html_output.append('<projections>\n')
        if proj_buf:
            html_output.append('<div markdown="1">\n')
            html_output.extend(proj_buf)
            html_output.append('\n</div>\n')
        html_output.append('</projections>\n')
        html_output.append('</stage-row>\n')

        play_buf = []
        proj_buf = []
        projections_end = False

    def append_play(line):
        play_buf.append(line if line.endswith('\n') else line + '\n')

    def parse_note_block(start_i):
        """Parse a > [!NOTE] block into HTML; return (html_string, next_index)."""
        parts = ['<div class="note-alert">\n']
        i = start_i + 1  # skip > [!NOTE]
        while i < len(lines) and lines[i].startswith('>'):
            content = lines[i][1:]
            if content.startswith(' '):
                content = content[1:]
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            eq = content.strip()
            if re.fullmatch(r'\$\$[^$]+\$\$', eq):
                parts.append(f'<div class="note-math">{eq}</div>\n')
            elif re.fullmatch(r'\$[^$]+\$', eq):
                parts.append(f'<div class="note-math">$${eq[1:-1]}$$</div>\n')
            else:
                parts.append(f'<p>{content}</p>\n')
            i += 1
        parts.append('</div>\n')
        return ''.join(parts), i

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.strip() == '<!-- stage-break -->':
            flush_row()
            i += 1
            continue

        if line.strip() == '<!-- projections-end -->':
            projections_end = True
            i += 1
            continue

        if line.startswith('#') or line.startswith('---') or line.startswith('<div class="preferred'):
            flush_row()
            out = line if line.endswith('\n') else line + '\n'
            if line.startswith('#'):
                # markdownlint MD022: blank lines around headings
                if html_output and not html_output[-1].endswith('\n\n'):
                    if html_output[-1].endswith('\n'):
                        html_output.append('\n')
                    else:
                        html_output.append('\n\n')
                html_output.append(out)
                html_output.append('\n')
            else:
                html_output.append(out)
            i += 1
            continue

        if line.startswith('</div>') and not play_buf and not proj_buf:
            html_output.append(line + '\n')
            i += 1
            continue

        if line.startswith('!['):
            # New figure after an existing projection beat → new stage-row
            if proj_buf:
                flush_row()
            proj_buf.append(line + '\n')
            i += 1
            continue

        if line.startswith('> [!NOTE]'):
            note_html, i = parse_note_block(i)
            proj_buf.append(note_html)
            continue

        # Normal play text (including blanks) stays with the current projection beat
        append_play(line)
        i += 1

    flush_row()
    return ''.join(html_output)


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

with open("act_0_ed_handoff.md", "r") as f:
    ch0_html = parse_chapter_to_rows(f.read())

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
    out.write(ch0_html + "\n\n<hr>\n\n")
    out.write(ch1_html + "\n\n<hr>\n\n")
    out.write(ch2_html + "\n\n<hr>\n\n")
    out.write(ch3_html + "\n\n<hr>\n\n")
    out.write(ch4_html + "\n\n<hr>\n\n")
    out.write(ch5_html + "\n\n")

print("Built index.md (Act 0–5)")
