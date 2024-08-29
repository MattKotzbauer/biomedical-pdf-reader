import fitz
import sys

if len(sys.argv) != 2:
    print("Usage: python script_name.py <pdf_filename>")
    sys.exit(1)

pdf_filename = sys.argv[1]

doc = fitz.open(pdf_filename)

highlight_text = []
page_numbers = []
start_char_indices = []

for page in doc:
    page_number = page.number + 1
    words = page.get_text_words()

    # Reconstruct the text with character indices
    text_content = ""
    char_index_map = []
    last_pos = 0

    for word in words:
        current_pos = len(text_content)
        if current_pos != last_pos:
            text_content += " " * (current_pos - last_pos)
        start_index = len(text_content)
        text_content += word[4]
        char_index_map.append((start_index, start_index + len(word[4])))
        last_pos = len(text_content)

    highlights = [annot for annot in page.annots() if annot.type[0] == 8]

    for highlight in highlights:
        highlight_rect = highlight.rect
        highlight_words = [w for w in words if fitz.Rect(w[:4]).intersects(highlight_rect)]
        highlight_sentence = " ".join(w[4] for w in highlight_words)
        start_char_index = char_index_map[words.index(highlight_words[0])][0] if highlight_words else -1

        highlight_text.append(highlight_sentence)
        page_numbers.append(page_number)
        start_char_indices.append(start_char_index)

even_indices = [num for num in range(0, len(highlight_text)) if num % 2 == 0]
odd_indices = [num for num in range(0, len(highlight_text)) if num % 2 != 0]

highlight_text_starts = [highlight_text[index] for index in even_indices]
highlight_text_ends = [highlight_text[index] for index in odd_indices]
page_numbers_starts = [page_numbers[index] for index in even_indices]
page_numbers_ends = [page_numbers[index] for index in odd_indices]
start_char_indices_starts = [start_char_indices[index] for index in even_indices]
start_char_indices_ends = [start_char_indices[index] for index in odd_indices]

txt1 = "Can you summarize the portion of the text between \""
txt2 = "\" (page "
txt3 = " at character "
txt4 = ") and \""
txt5 = "\" (page "
txt6 = " at character "
txt7 = "). The excerpts don't have to be an exact match: as long as a section contains 10 or so words in the excerpt, consider it valid as a starting / ending point. If unable to find the excerpts use the specified page and character locations. Please put the summary in markdown syntax, suitable for compilation to a beamer slide presentation to be compiled with pandoc. Also, do not include unicode characters, please put everything in LaTeX syntax. Also, do not include the YAML front matter."

new_list = [
    txt1 + highlight_text_starts[i] + txt2 + str(page_numbers_starts[i]) + txt3 + str(start_char_indices_starts[i]) +
    txt4 + highlight_text_ends[i] + txt5 + str(page_numbers_ends[i]) + txt6 + str(start_char_indices_ends[i]) + txt7
    for i in range(len(highlight_text_starts))
]

with open("text_prompts.txt", "w") as file:
    file.write("\n\n".join(new_list))

