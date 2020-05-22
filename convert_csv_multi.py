import html.parser
import json

class HTMLTextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super(HTMLTextExtractor, self).__init__()
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def get_text(self):
        return ''.join(self.result)

def html_to_text(html):
    """Converts HTML to plain text (stripping tags and converting entities).
    >>> html_to_text('<a href="#">Demo<!--...--> <em>(&not; \u0394&#x03b7;&#956;&#x03CE;)</em></a>')
    'Demo (\xac \u0394\u03b7\u03bc\u03ce)'

    "Plain text" doesn't mean result can safely be used as-is in HTML.
    >>> html_to_text('&lt;script&gt;alert("Hello");&lt;/script&gt;')
    '<script>alert("Hello");</script>'

    Always use html.escape to sanitize text before using in an HTML context!

    HTMLParser will do its best to make sense of invalid HTML.
    >>> html_to_text('x < y &lt z <!--b')
    'x < y < z '

    Unrecognized named entities are included as-is. '&apos;' is recognized,
    despite being XML only.
    >>> html_to_text('&nosuchentity; &apos; ')
    "&nosuchentity; ' "
    """
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()


# 30.
# Portal
# Platform:
# PC
# October 10, 2007
# Portal is a new single player game from Valve. Set in the mysterious Aperture Science Laboratories, Portal has been called one of the most innovative new games on the horizon and offers gamers hours of unique gameplay. The game is designed to change the way players approach, manipulate, and surmise the possibilities in a given environment; similar to how Half-Life 2's Gravity Gun innovated new ways to leverage an object in any given situation. Players must solve physical puzzles and challenges by opening portals to maneuvering objects, and themselves, through space. [Valve]
# User Score
# 9.2
# Expand

def parse_extra(lines):
    next_index = None
    lines_parsed = []
    state = 0
    skip_platform = 0
    for line in lines:
        if state == 0:
            if next_index is None:
                next_index = int(line.split(".")[0])
            if str(next_index) + "." == line:
                next_index += 1
                state = 1
                lines_parsed.append(line)
        elif state == 1:
            lines_parsed.append(line)
            state = 2
        elif state == 2:
            skip_platform += 1
            if skip_platform == 2:
                state = 3
        elif state == 3:
            lines_parsed.append(line)
            state = 4
        elif state == 4:
            if line == "User Score":
                lines_parsed.append(line)
                state = 5
        elif state == 5:
            lines_parsed.append(line)
            skip_platform = 0
            state = 0        
            
    return lines_parsed


with open("config.json", "r") as f:
    config = f.read()
    config = json.loads(config)

for k, thread in enumerate(config["threads"]):
    print("thread: " + str(k) + "/" + str(len(config["threads"])))

    line_start = 421
    line_start += 41
    # line_end = "*Only games with seven or more reviews are eligible."
    line_end = "prev"
    line_end = None
    folder = thread["out_folder"]
    details_vect = [False, True]

    for i in range(0,100):
        for details in details_vect:
            try:
                filename = None
                if not details:
                    filename = folder + "/page" + str(i) + ".txt"
                else:
                    filename = folder + "/page" + str(i) + ".d.txt"

                with open(filename, "r", encoding="utf-8") as f:
                    data = f.read()
                    text = html_to_text(data)
                    lines = text.split("\n")
                    lines = [line.lstrip() for line in lines if (line and not line.replace("\n","").isspace())]
                    
                    lines = lines[line_start:]

                    end_index = 0

                    if not line_end:
                        end_index = len(lines) - 1
                    else:
                        for line_index, line in enumerate(lines):
                            if line_end in line:
                            # if line_end == line:
                                print(line)
                                end_index = line_index
                                break

                    print(end_index)
                    lines = lines[0:end_index]

                    lines = parse_extra(lines)

                    text = "\n".join(lines)

                if not details:
                    filename = folder + "/page" + str(i) + ".csv"
                else:
                    filename = folder + "/page" + str(i) + ".d.csv"

                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)
            except FileNotFoundError:
                print("file not found at index: " + str(i))
