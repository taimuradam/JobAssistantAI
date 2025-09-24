def parse(raw_text: str):

    #remove newlines and weird spacing characters
    cleaned_text = raw_text.replace("\u200b", "")
    lines = cleaned_text.split("\n")

    #remove all empty lines
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    #replace ● with -> to standardize the bullet points
    normalized_lines = [line.replace("●", "->") for line in non_empty_lines]

    #if -> comes first and then there is a new line with the bullets, put it on one line
    #For example if the structure of it is:
    #->
    #Enhanced semantic keyword mapping and automated section scoring using NLP pipelines
    #Then it will convert point to be:
    #-> Enhanced semantic keyword mapping and automated section scoring using NLP pipelines
    merged_lines = []
    i = 0

    while i < len(normalized_lines):
        cur = normalized_lines[i].strip()
        if cur == "->":
            if normalized_lines[i+1]:
                next_line = normalized_lines[i+1].lstrip()
                cur += " " + next_line
                merged_lines.append(cur)
                i += 2
            else:
                merged_lines.append(cur)
                i += 1
        else:
            merged_lines.append(cur)
            i += 1

    for line in merged_lines:
        print(line)

    return non_empty_lines