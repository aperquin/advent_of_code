# %%
import re

# %% Read the input file as independent lines, then clean them.
with open("input", 'r') as opened_file:
    input_data = opened_file.readlines()
data_list = [data.strip() for data in input_data]

# %%
def replace_number(input_string):
    match input_string:
        case "one":
            input_string = '1'
        case "two":
            input_string = '2'
        case "three":
            input_string = '3'
        case "four":
            input_string = '4'
        case "five":
            input_string = '5'
        case "six":
            input_string = '6'
        case "seven":
            input_string = '7'
        case "eight":
            input_string = '8'
        case "nine":
            input_string = '9'
    return input_string

# %% Find all calibration values in the input
calibration_values = []
for data in data_list:
    # Find all the digits in the line
    found_digits = re.findall("([1-9]|one|two|three|four|five|six|seven|eight|nine)", data)
    found_digits = list(map(replace_number, found_digits))

    # If there is only one, copy it
    if len(found_digits) == 1:
        found_digits.append(found_digits[0])

    # The calibration value is the concatenation of the first and last digit on the line
    calibration_value_string = f"{found_digits[0]}{found_digits[-1]}"
    calibration_value_int = int(calibration_value_string)

    # # Save the calibration value for that line, then proceed to the following
    calibration_values.append(calibration_value_int)

# %%
print(calibration_values)
print(sum(calibration_values))
