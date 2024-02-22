from main import logger
import os
import json

from preprocessor.PreProcessor import PreProcessor

records_JSON = {
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


class PreprocessorForJSON(PreProcessor):

    def map_to_JSON(self):
        base_path = "test/preprocessor/Volcano_Dataset/"
        volcano_id = 1
        observ_id = 1
        while volcano_id < 11:
            path = base_path + f"Volcano{volcano_id}/observation{observ_id}.txt"
            try:
                assert(os.path.exists(path))
                volcano_key = f"volcano_{volcano_id}"
                records_JSON[volcano_key][f"observation{observ_id}"] = self.map_one_record_to_JSON(path, volcano_id, observ_id)
                observ_id += 1
            except Exception as e:
                logger.error(e)
                volcano_id += 1
                observ_id = 1

        pretty_records = json.dumps(records_JSON, indent=4)
        print(pretty_records)


    def map_one_record_to_JSON(self, path, volcano_id, observ_id):
        record = {"id": f"V{volcano_id}-Ob{observ_id}"}
        with open(path, "r") as file:
            for _ in range(13):
                line = file.readline().strip()
                if line:
                    values = line.split(",")
                    record[values[0]] = values[1]
        assert(len(record) == 12)
        tilt_erupt = record["tilt_erupt"].replace("nrad", "")
        record["tilt_erupt"] = float(tilt_erupt)
        self.evaluate_exponents(record)
        self.convert_fields_to_float(record)
        return record

    def evaluate_exponents(self, record):
        for key in ["G", "mu", "M"]:
            value = record[key].split("^")
            value = float(value[0]) ** float(value[1])
            record[key] = value


    def convert_fields_to_float(self, record):
        for key in self.float_fields:
            record[key] = float(record[key])


if __name__ == "__main__":
    # map_to_JSON()
    pass
