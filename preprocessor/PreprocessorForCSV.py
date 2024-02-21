from main import logger
from preprocessor.PreProcessor import PreProcessor


class PreprocessorForCSV(PreProcessor):

    def __init__(self):
        super().__init__()
        self.map_function = self.map_record_to_CSV
        self.output_data_object = []
        self.current_final_tilt = None


    def output_to_CSV(self):
        pass


    def map_record_to_CSV(self, path, record_list, volcano_id, observ_id, max_seconds_for_current_volcano):
        time_remaining = max_seconds_for_current_volcano - observ_id
        record = [f"V{volcano_id}-Ob{observ_id}", volcano_id, observ_id, time_remaining]
        with open(path, "r") as file:
            for _ in range(13):
                line = file.readline().strip()
                if line:
                    key_value = line.split(",")
                    key = key_value[0]
                    value = key_value[1]
                    if key in self.ignorable_fields:
                        pass
                    elif key in self.float_fields:
                        value = float(key_value[1])
                        record.append(value)
                    elif key in self.exponential_fields:
                        base_and_exp = list(map(lambda x: float(x), value.split("^")))
                        record.append(base_and_exp[0] ** base_and_exp[1])
                    elif key == "tilt_erupt":
                        value = float(value.replace("nrad", ""))
                        record.append(value)
                        if observ_id == max_seconds_for_current_volcano:
                            self.current_final_tilt = value
                        record.append(self.current_final_tilt)
        # assert (len(record) == 12)
        record_list.append(record)
        return record_list


if __name__ == "__main__":
    preprocessor = PreprocessorForCSV()
    preprocessor.prepare_data_object()