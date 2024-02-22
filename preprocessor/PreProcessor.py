import os
from main import logger


class PreProcessor:

    ignorable_fields = ["g", "Patm", "r", "v"]
    float_fields = ["rho", "rc", "sigma"]
    exponential_fields = ["G", "mu", "M"]
    final_fields = float_fields + exponential_fields
    output_data_object = None
    map_function = None


    def prepare_data_object(self):
        # Crawl through data files. Read and map data to either CSV or JSON format.
        output_data = self.output_data_object
        base_path = "raw_data/Volcano_Dataset/"
        volcano_id = 1
        observ_id = 1
        volcano_path = base_path + f"Volcano{volcano_id}/"
        max_seconds_for_current_volcano = self.count_files(volcano_path)
        nums_of_observations = [max_seconds_for_current_volcano]
        while volcano_id < 11:
            path = volcano_path + f"observation{observ_id}.txt"
            try:
                assert(os.path.exists(path))
                output_data = self.map_function(path, output_data, volcano_id, observ_id, max_seconds_for_current_volcano)
                observ_id += 1
            except Exception as e:
                logger.error(e)
                volcano_id += 1
                volcano_path = base_path + f"Volcano{volcano_id}/"
                max_seconds_for_current_volcano = self.count_files(volcano_path)
                nums_of_observations.append(max_seconds_for_current_volcano)
                observ_id = 1
        for record in output_data:
            print(record)
        print(nums_of_observations)
        return output_data


    def count_files(self, directory):
        file_count = 0
        for _, _, files in os.walk(directory):
            file_count += len(files)
        return file_count


    # def append_final_tilt_values(self, output_data, nums_of_observations):
    #     for record in output_data


if __name__ == "__main__":
    print(PreProcessor.count_files("raw_data/Volcano_Dataset/Volcano2/"))