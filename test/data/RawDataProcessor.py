from main import logger
import os
import json

records = {
    "volcano_1": {},
    "volcano_2": {},
    "volcano_3": {},
    "volcano_4": {},
    "volcano_5": {},
    "volcano_6": {},
    "volcano_7": {},
    "volcano_8": {},
    "volcano_9": {},
    "volcano_10": {}
}


def process_all_records():
    base_path = "test/data/Volcano_Dataset/"
    volcano_id = 1
    observ_id = 1
    while volcano_id < 11:
        path = base_path + f"Volcano{volcano_id}/observation{observ_id}.txt"
        try:
            assert(os.path.exists(path))
            # logger.info(f"Found file: {os.path.abspath(path)}")
            volcano_key = f"volcano_{volcano_id}"
            # records.setdefault(f"volcano_{volcano_id}", {}) # TODO refactor later to only define when initializing or updating volcano_id
            records[volcano_key][f"observation{observ_id}"] = process_one_record(path, volcano_id, observ_id)
            # = {
            #     f"observation_{observ_id}": process_one_record(path, volcano_id, observ_id)
            # }
            observ_id += 1
        except Exception as e:
            logger.error(e)
            volcano_id += 1
            observ_id = 1

    pretty_records = json.dumps(records, indent=4)
    print(pretty_records)


def process_one_record(path, volcano_id, observ_id):
    result = {"id": f"V{volcano_id}-Ob{observ_id}"}
    with open(path, "r") as file:
        for _ in range(13):
            line = file.readline().strip()
            if line:
                values = line.split(",")
                result[values[0]] = values[1]
    assert(len(result) == 12)
    return result


if __name__ == "__main__":
    process_all_records()
