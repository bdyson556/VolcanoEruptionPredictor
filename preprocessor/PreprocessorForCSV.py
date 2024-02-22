import csv
import os

class PreprocessorForCSV:

    # ignorable_fields = ["g", "Patm", "r", "v"]
    float_fields = ["rho", "rc", "sigma"]
    exponential_fields = ["G", "mu", "M"]
    final_fields = ["id", "volcano_id", "observ_id", "G", "rho", "mu", "rc", "M", "sigma",
                    "time_remaining", "sensor_reading", "tilt_erupt"]
    output_data_object = None
    map_function = None
    output_file = "../data/prepared_observations.csv"

    def __init__(self):
        super().__init__()
        self.map_function = self.map_records_to_CSV_format
        self.output_data_object = []
        self.current_final_tilt = None


    def prepare_data_object(self):
        # Crawl through data files. Read and map data to either CSV or JSON format.
        output_data = self.output_data_object
        base_path = "../data/raw_data/Volcano_Dataset/"
        volcano_id = 1
        volcano_path = base_path + f"Volcano{volcano_id}/"
        total_observations_for_current_volcano = self.count_files(volcano_path)
        observ_id = total_observations_for_current_volcano
        while volcano_id < 11:
            path = volcano_path + f"observation{observ_id}.txt"
            try:
                assert (os.path.exists(path))
                output_data = self.map_function(path, output_data, volcano_id, observ_id)
                observ_id -= 1
            except Exception as e:
                volcano_id += 1
                volcano_path = base_path + f"Volcano{volcano_id}/"
                total_observations_for_current_volcano = self.count_files(volcano_path)
                observ_id = total_observations_for_current_volcano
        self.write_to_csv(output_data, self.output_file, headers=True)
        return output_data


    def map_records_to_CSV_format(self, path, record_list, volcano_id, observ_id):

        # Get base volcano params, countdown values, and sensor readings for current observation.
        params, countdown_values, sensor_readings, tilt_erupt = self.get_volcano_parameters(path, volcano_id, observ_id)

        # Create one record for each sensor reading, adding countdown time and parameters accordingly.
        length = len(countdown_values)
        assert (abs(countdown_values[0]) + 2 == length == len(sensor_readings))
        for i in range(0, length):
            sub_record = [f"V{volcano_id}-Ob{observ_id}-{(i + 1)}"] + params.copy()
            sub_record.append(countdown_values[i])
            sub_record.append(sensor_readings[i])
            sub_record.append(tilt_erupt)
            record_list.append(sub_record)
        return record_list

    def get_volcano_parameters(self, path, volcano_id, observ_id):
        params = [volcano_id, observ_id]
        countdown_values = []
        sensor_readings = []
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    if "-" in line[:4] or line[0].isdigit():
                        if "e" in line[:30]:
                            sensor_readings = [self.evaluate_sci_notation(x) for x in line.split(",")]
                        else:
                            countdown_values = [int(x) for x in line.split(",")]
                    else:
                        key_value = line.split(",")
                        key = key_value[0]
                        value = key_value[1]
                        # if key in self.ignorable_fields:
                        #     pass             # TODO you shouldn't need to explcitly id a field as ignorable. If it doesn't meet the other criteria, it's ignorable.
                        if key in self.float_fields:
                            value = float(key_value[1])
                            params.append(value)
                        elif key in self.exponential_fields:
                            base_and_exp = list(map(lambda x: float(x), value.split("^")))
                            params.append(base_and_exp[0] ** base_and_exp[1])
        return params, countdown_values, sensor_readings, sensor_readings[-1]

    def count_files(self, directory):
        file_count = 0
        for _, _, files in os.walk(directory):
            file_count += len(files)
        return file_count

    def evaluate_sci_notation(self, string):
        base_and_exp = list(map(lambda x: float(x), string.split("e")))
        return base_and_exp[0] * (10 ** base_and_exp[1])

    def write_to_csv(self, data, filename, headers):
        if headers:
            data = [self.final_fields] + data
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)


if __name__ == "__main__":
    preprocessor = PreprocessorForCSV()
    preprocessor.prepare_data_object()
