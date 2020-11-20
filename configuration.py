from configConstants import VALID_FORMATS, MAX_SIZE


class Configuration:
    def __init__(self, input_format, output_format, data_type, dataset_size):
        self.input_format = input_format
        self.output_format = output_format
        self.data_type = data_type  # i.e. data or metadata
        self.dataset_size = dataset_size  # i.e. the number of rows in an unweighted dataset
        self.is_valid = None

    def validate(self):
        """
        Mandatory: input_format, output_format
        Optional: data_type, size
        """
        if self.is_valid is not None:
            return self.is_valid

        self.is_valid = True

        try:
            if self.input_format is None \
                    or self.input_format.lower() not in VALID_FORMATS:
                raise Exception
            else:
                print(f"Input format {self.input_format} is valid.")
        except:
            print(f"Input format {self.input_format} is invalid.")
            self.is_valid = False

        try:
            if self.output_format is None \
                    or self.output_format.lower() not in VALID_FORMATS:
                raise Exception
            else:
                print(f"Output format {self.output_format} is valid.")
        except:
            print(f"Output format {self.output_format} is invalid.")
            self.is_valid = False

        if self.data_type is not None:
            try:
                if self.data_type.lower() != "data" \
                        and self.data_type.lower() != "metadata":
                    raise Exception
                else:
                    print(f"Data type {self.data_type} is valid.")
            except:
                print(f"Data type {self.data_type} is invalid.")
                self.is_valid = False
        else:
            print("No data type inputted, but since not mandatory. will pass.")

        if self.dataset_size is not None:
            try:
                if self.dataset_size > MAX_SIZE:
                    print(f"Size {self.dataset_size} is invalid, above maximum.")
                    self.is_valid = False
                else:
                    print(f"Size {self.dataset_size} is valid.")
            except:
                print("Size invalid, but since not mandatory, will pass.")
        else:
            print("No size inputted, but since not mandatory, will pass.")

        # No False returned, so must be valid
        return self.is_valid
