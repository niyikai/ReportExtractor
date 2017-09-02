import re
import os

def get_words(words):
    ret = []
    pattern = re.compile("[A-Za-z0-9\']+")
    for word in words:
        if bool(re.search(pattern, word)):
            ret.append(word)
    return ret

def check_text(line, last, threshold=0.5):
    if len(line) == 0 or (len(line) < 10 and not last):
        return False
    words = get_words(line.split(' '))
    if len(words) <= 0 or (len(words) <= 5 and not last):
        return False
    total = len(line)
    count = 0.0
    for chr in line:
        if 'a' <= chr <= 'z' or 'A' <= chr <= 'Z':
            count += 1.0
    if count / total >= threshold:
        return True
    else:
        return False

def find_text(doc):
    text = []
    last = False
    
    lines = doc.split('\n')
    for line in lines:
        if check_text(line, last):
            text.append(line)
            words = get_words(line.split(' '))
            last = True if len(line) >= 30 and len(words) >= 7 else False
        else:
            last = False
    return text


def write_orginal_text(doc, filename):
    with open(filename, "w") as f:
        for page in doc:
            f.write(page)

def pdf_to_text(filename):
    with open(filename, "r") as f:
        doc = f.read()
    return doc


# def test(filename):
#     doc = pdf_to_text("./reports_2010/" + filename)
#     write_orginal_text(doc, filename + '.txt')
#     print doc
#     text = find_text(doc)
#     with open("extract_" + filename + '.txt', 'w') as f:
#         f.write('\n'.join(text))


if __name__ == "__main__":
    for root, dirs, files in os.walk('./extracted/'):
        for file in files:
            if file[0] == '.':
                continue
            # convert pdf into a text list
            print(root + file)
            doc = pdf_to_text(root + file)

            text = find_text(doc)
            # write the result
            with open("./results/extract_" + file + '.txt', 'w') as f:
                f.write('\n'.join(text))
                # test("2011-03-21 (DBS VICKERS SECURITIES LIMI) (HK) BJ Jingkelong - A-share listing helps expansion - BUY.17385365.pdf")
