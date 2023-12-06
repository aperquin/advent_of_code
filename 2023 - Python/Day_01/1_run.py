# %%
import re

# %% Read the input file as independent lines, then clean them.
with open("input", 'r') as opened_file:
    input_data = opened_file.readlines()
data_list = [data.strip() for data in input_data]

# %% Find all calibration values in the input
calibration_values = []
for data in data_list:
    # Find all the digits in the line
    found_digits = re.findall("[1-9]", data)

    # If there is only one, copy it
    if len(found_digits) == 1:
        found_digits.append(found_digits[0])

    # The calibration value is the concatenation of the first and last digit on the line
    calibration_value_string = f"{found_digits[0]}{found_digits[-1]}"
    calibration_value_int = int(calibration_value_string)

    # Save the calibration value for that line, then proceed to the following
    calibration_values.append(calibration_value_int)

# %%
print(calibration_values)
print(sum(calibration_values))
