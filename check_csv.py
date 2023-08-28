import csv


def check_over_column(file_name):
    with open(file_name, "r", encoding="utf-8", newline="") as file:
        reader = list(csv.reader(file))
        for row in reader:
            try:
                if row[5]:
                    print(f"{row[0]}|{row[1]}|{row[3]}")
            except:
                pass


def check_data(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        data = file.readlines()
        for row in data:
            if row[0] != '"':
                print(row)


def check_unique_data(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        story_text = list(reader)
        del story_text[0]
        print(len(list(set(row[3] for row in story_text))))


if __name__ == "__main__":
    check_over_column("./text.csv")
    check_data("./storyText.csv")
    check_unique_data("./storyText.csv")
