import re
# --- Guitar Fretboard Schematic Generator (Standard Tuning EADGBE) ---

def main(is_typst: bool = False):
    notes_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    chromatic_numbers = {note: i + 1 for i, note in enumerate(notes_sharp)}
    scale_degrees = {
        'C': 1, 'C#': '1#', 'D': 2, 'D#': '2#', 'E': 3,
        'F': 4, 'F#': '4#', 'G': 5, 'G#': '5#', 'A': 6,
        'A#': '6#', 'B': 7
    }

    open_notes = ['E', 'A', 'D', 'G', 'B', 'E']  # low to high strings

    def build_fretboard(mapping_func, name):
        frets = 22  # 0–21
        fret_labels = [f"{i:<3}" for i in range(frets)]
        header = "   " + "".join(fret_labels)
        lines = [header]

        for string_note in reversed(open_notes):
            open_index = notes_sharp.index(string_note)
            line = [f"{string_note} |"]
            for fret in range(frets):
                note = notes_sharp[(open_index + fret) % 12]
                if mapping_func == 'notes':
                    val = note
                elif mapping_func == 'notes_single':
                    val = '-' if note.endswith('#') else note
                elif mapping_func == 'notes_empty':
                    val = ' ' if note.endswith('#') else note
                elif mapping_func == 'chromatic':
                    val = str(chromatic_numbers[note])
                else:  # diatonic
                    val = str(scale_degrees[note])
                line.append(f"{val:<3}")
            lines.append("".join(line))

        # Fret marker line
        marker_frets = [3, 5, 7, 9, 12, 15, 17, 19, 21]
        marker_line = "   " + "".join(f"{i:<3}" if i in marker_frets else "   " for i in range(frets))
        lines.append(marker_line)

        title = f"\n{name} (EADGBE, low E at bottom)\n"
        return title + "\n".join(lines)

    notes_fretboard = build_fretboard('notes', "NOTES")
    notes_single_fretboard = build_fretboard('notes_single', "NOTES Single")
    notes_empty_fretboard = build_fretboard('notes_empty', "NOTES Empty")
    chromatic_fretboard = build_fretboard('chromatic', "CHROMATIC NUMBERS (C=1..B=12)")
    scale_fretboard = build_fretboard('diatonic', "SCALE DEGREES (C=1..B=7, sharps marked)")

    full_text = "\n\n".join([notes_fretboard,notes_single_fretboard,notes_empty_fretboard, chromatic_fretboard, scale_fretboard])

    if is_typst:
        # full_text = full_text.replace("#", "\#") 
        #full_text = re.sub("$", "\\\\", full_text, flags = re.MULTILINE)
        def wrap_text(text: str):
            return "#set text(font: \"Courier New\", size: 11pt)\n`\n" + text + "\n`"
 
        full_text = wrap_text(full_text)

    print(full_text)


if __name__ == "__main__":
    main(is_typst=True)

