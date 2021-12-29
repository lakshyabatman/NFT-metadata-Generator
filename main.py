import csv
import json
import os.path
from dotenv import load_dotenv

load_dotenv()


def getDataFromCSV(fileName):
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        column_header_list = []
        res = []
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                column_header_list = row
            else:
                data_dict = {}
                for index, column in enumerate(column_header_list):
                    data_dict[column] = row[index]
                res.append(data_dict)
            line_count += 1
        return res


def toERC721Metadata(object_dict):
    IPFS_IMAGE_CID = os.environ["IPFS_BASE_URL"]
    if "Image" not in object_dict:
        raise Exception("Image is required ! ")

    metadata = {
        "index": object_dict["Image"],
        "image": IPFS_IMAGE_CID + "/" + object_dict["Image"] + ".png",
        "description": object_dict["Description"] if "Description" in object_dict else "",
        "name": object_dict["Title"] if "Title" in object_dict else "",
        "external_url": object_dict["URL"] if "URL" in object_dict else "",
        "attributes": []
    }
    object_dict.pop("Image", None)
    object_dict.pop("Description", None)
    object_dict.pop("Title", None)
    object_dict.pop("URL", None)
    for attribute in object_dict:
        metadata["attributes"].append({
            "trait_type": attribute,
            "value": object_dict[attribute]
        })
    return metadata


def saveData(object_dict):
    index = object_dict["index"]
    object_dict.pop("index", None)
    with open('exports/{}.json'.format(index), 'w') as f:
        f.write(json.dumps(object_dict, ensure_ascii=False, indent=4))
        f.close()


if __name__ == '__main__':
    d = getDataFromCSV("./assets/data.csv")
    if not os.path.exists("exports"):
        os.mkdir("exports")
    for i in d:
        saveData(toERC721Metadata(i))
