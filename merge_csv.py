import csv

# old csv, less lines
with open("text.csv", "r", encoding="utf-8") as f1:
    reader1 = csv.reader(f1)
    next(reader1)
    rows1 = [[row[0], row[1], row[4]] for row in reader1 if row[4]]

# new csv, more lines
with open("storyText.csv", "r", encoding="utf-8") as f2:
    reader2 = csv.reader(f2)
    next(reader2)
    rows2 = [row for row in reader2]

for r2 in rows2:
    for r1 in rows1:
        if r2[0] == r1[0] and r2[1] == r1[1]:
            r2[4] = r1[2]
            break

with open("storyText.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["filename", "item_id", "character_id", "src", "dst"])
    writer.writerows(rows2)
