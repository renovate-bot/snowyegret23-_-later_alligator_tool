import UnityPy
import os
import sys
import csv
import json


def sanitize_text(text):
    return text.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")


def restore_text(text):
    return text.replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")


######################################################################################


def extract_bundles(csv_name="storyText.csv"):
    print("extract 작업 시작")
    with open(csv_name, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["filename", "item_id", "character_id", "src", "dst"])
    filelst = [i for i in os.listdir("./1.original_bundle") if i.endswith(".bundle")]
    for fn in filelst:
        extract_text(fn, csv_name)


def extract_text(fn, csv_name):
    clean_fn = os.path.splitext(fn)[0]
    text_lst = []
    env = UnityPy.load(f"./1.original_bundle/{fn}")
    for obj in env.objects:
        # fmt: off
        if (obj.type.name == "MonoBehaviour" and obj.serialized_type.nodes):
            tree: dict = obj.read_typetree()
            if tree.get('storyText') == None:
                continue
            if tree.get('itemId') == None:
                continue
            if tree.get('character') == None:
                continue
            if tree.get('character').get('m_PathID') == None:
                continue
            item_id, character_id, text = tree.get('itemId'), tree.get('character').get('m_PathID'), sanitize_text(tree.get('storyText'))
            text_lst.append([clean_fn, item_id, character_id, text, ""])
    sorted_lst = sorted(text_lst, key=lambda x: x[1])
    with open(csv_name, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(sorted_lst)
    if text_lst:
        print(f" - {clean_fn} 번들 작업 완료! ({len(text_lst)}항목)")


def extract_test(fn):
    clean_fn = os.path.splitext(os.path.split(fn)[1])[0]
    text_lst = []
    env = UnityPy.load(fn)
    for obj in env.objects:
        if obj.type.name == "MonoBehaviour" and obj.serialized_type.nodes:
            tree = obj.read_typetree()
            item_id = tree.get("itemId")
            character_id = tree.get("character").get("m_PathID")
            text = sanitize_text(tree.get("storyText"))
            text_lst.append([clean_fn, item_id, character_id, text, ""])
    sorted_lst = sorted(text_lst, key=lambda x: x[1])
    with open(f"{clean_fn}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(sorted_lst)


######################################################################################


def import_bundles(csv_name="storyText.csv"):
    print("import 작업 시작")
    with open(csv_name, "r", encoding="utf-8", newline="") as f:
        reader = list(csv.reader(f))
        del reader[0]
        translate_dict = {}
        for i in reader:
            if i[0] not in translate_dict:
                translate_dict[i[0]] = {}
            translate_dict[i[0]][i[1]] = {
                "item_id": i[1],
                "character_id": i[2],
                "src": i[3],
                "dst": i[4],
            }
    filelst = [
        fn
        for fn in os.listdir("./1.original_bundle")
        if fn.endswith(".bundle") and os.path.splitext(fn)[0] in translate_dict
    ]
    for fn in filelst:
        import_text(fn, translate_dict)


def import_text(fn, translate_dict):
    clean_fn = os.path.splitext(os.path.basename(fn))[0]
    count = 0
    translate_count = 0
    env = UnityPy.load(f"./1.original_bundle/{fn}")
    for obj in env.objects:
        # fmt: off
        if (obj.type.name == "MonoBehaviour" and obj.serialized_type.nodes):
            tree = obj.read_typetree()
            if tree.get('storyText') == None:
                continue
            if tree.get('itemId') == None:
                continue
            if tree.get('character') == None:
                continue
            if tree.get('character').get('m_PathID') == None:
                continue
            item_id = str(tree.get('itemId'))
            if translate_dict[clean_fn][item_id]["dst"] == "":
                continue
            count += 1
            if count == 1:
                print(f" - {clean_fn} 번들 작업 중...", end="")
            translated = restore_text(translate_dict[clean_fn][item_id]["dst"])
            translate_count += 1
            tree["storyText"] = translated
            obj.save_typetree(tree)
    if count != 0:
        with open(f"./2.edited_bundle/{clean_fn}.bundle", "wb") as f:
            f.write(env.file.save())
        # fmt: off
        all_count = len(translate_dict[clean_fn])
        print(f"완료! ({translate_count}/{all_count}) [{translate_count/all_count*100:.2f}%]")


######################################################################################


if __name__ == "__main__":
    extract_bundles()
    # import_bundles()
    # extract_test("./2.edited_bundle/scenes_scenes_artdealer.bundle")
    # extract_test("./2.edited_bundle/scenes_scenes_grilldad.bundle")
    # extract_test("./2.edited_bundle/scenes_scenes_locationintro.bundle")
    pass
