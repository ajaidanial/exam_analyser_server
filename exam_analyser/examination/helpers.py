import os
from collections import OrderedDict
from csv import DictWriter
from typing import List

import pandas
import xlrd
from django.conf import settings
from django.db.models import QuerySet
from pandas import ExcelWriter
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from exam_analyser.base.helpers import random_n_token


def write_list_of_dict_to_excel(
    data_list: List[List[dict]], base_file_name=None, is_temporary_file=False
):
    """
    For the given data, generates an excel file. First writes a CSV file and then converts to XLSX.
    Based on the `is_temporary_file` param, the place of file creation varies. The output of this function is
    a public file url to the created file.

    Use Cases:
        1. Used in bulk upload output data files
        2. Bulk export from the frontend

    Note:
        1. This is used to write an excel file based on the given data.
        2. Multiple sheets can also be written using this function.
        3. This first writes the csv files and then converts the csv files to an excel file.

    Input Data Schema:
        [                                           ==> Excel file
            [                                       ==> Excel Sheet
                {                                   ==> Excel Sheet Row
                    "column_name_1": "value1",      ==> Row Column Data | Headers are got dynamically
                    "column_name_2": "value2",
                },
                ...
            ],
            ...
        ]

    Example Data Input:
        [
            [                                       ==> Sheet 1
                {"name":"Ajai Danial", "age": 12},      ==> Row 1
                {"name":"Danial", "age": 20},           ==> Row 2
            ],
            [                                       ==> Sheet 2
                {"name":"Ajai Danial", "age": 12},      ==> Row 1
                {"name":"Danial", "age": 20},           ==> Row 2
            ]
        ]
    """

    # decides where to create the file based on the `is_temporary_file`
    # if temporary, then the files are removed using a celery beat task
    # temporary files are generated for single time use and are not required after some time
    root_directory = settings.TEMP_ROOT if is_temporary_file else settings.STORE_ROOT

    # config for the file
    file_name = base_file_name if base_file_name else random_n_token(10)
    excel_file_path = f"{root_directory}/{file_name}.xlsx"
    excel_file_media_path = f"{root_directory.split('/')[-1]}/{file_name}.xlsx"

    temp_csv_file_paths: List[str] = []
    for single_sheet_data_index in range(0, len(data_list)):
        single_sheet_data = data_list[single_sheet_data_index]
        csv_file_path = f"{root_directory}/{file_name}{single_sheet_data_index}.csv"

        # keys/header for the file | contains all the keys in the dictionaries
        dict_keys = []
        for data_dict in single_sheet_data:
            print(data_dict)
            dict_keys += [_ for _ in data_dict.keys() if _ not in dict_keys]

        # write csv
        with open(csv_file_path, "w") as outfile:
            writer = DictWriter(outfile, dict_keys)
            writer.writeheader()
            writer.writerows(single_sheet_data)

        # store for later conversion
        temp_csv_file_paths.append(csv_file_path)

    # write xlsx file
    writer = ExcelWriter(excel_file_path)

    for csv_path_index in range(0, len(temp_csv_file_paths)):
        csv_file_path = temp_csv_file_paths[csv_path_index]
        # read csv and write to excel
        read_file = pandas.read_csv(csv_file_path)
        read_file.to_excel(
            writer, index=None, header=True, sheet_name=f"sheet{csv_path_index + 1}"
        )
        # remove unnecessary files
        os.remove(csv_file_path)

    # save output
    writer.save()

    return excel_file_media_path


def get_excel_writable_data_from_input_data(input_unclean_data):
    """
    Given any data, they can be of any type list, dict and even a queryset.
    This function converts those to excel writable data. This looks upto only one level of depth.
    This uses recursion to get the data.

    Deciding Factor for the internal keys:
        1. If QuerySet => returns a list of pk's
        2. If a strings/single values => returns the value directly | end of recursion
        3. If a dict, looks for `id` & `name` in the dict => returns key__id & key__name
        4. If a list of dict => recursively get value of each single dict
    """

    # considered classes
    DICT_KIND = [dict, OrderedDict, ReturnDict]
    LIST_KIND = [list, ReturnList]
    SINGLE_VALUE_KIND = [int, str, None]
    DICT_KIND_CHILD_KEYS_TO_CHECK = ["id", "name"]

    if type(input_unclean_data) in SINGLE_VALUE_KIND:
        return input_unclean_data  # end of recursion

    if type(input_unclean_data) == QuerySet:
        # return list of pk's
        pk_field_name = input_unclean_data.model._meta.pk.name
        return list(input_unclean_data.values_list(pk_field_name, flat=True))

    if type(input_unclean_data) in DICT_KIND:
        # return dict of necessary values
        output_clean_data = {}
        for child_dict_key in DICT_KIND_CHILD_KEYS_TO_CHECK:
            if child_dict_key in input_unclean_data.keys():
                output_clean_data[child_dict_key] = input_unclean_data[child_dict_key]
        return output_clean_data

    if type(input_unclean_data) in LIST_KIND:
        output_clean_data = []
        considered_list_child_type = None

        for single_unclean_data in input_unclean_data:

            # checking the child types are same
            if (
                considered_list_child_type
                and type(single_unclean_data) != considered_list_child_type
            ):
                # something is not right in the input data => mixed types
                return [
                    {
                        "detail": f"{type(single_unclean_data)} | {considered_list_child_type}, mixed "
                        f"child types are given. Error in the input data."
                    }
                ]
            considered_list_child_type = type(single_unclean_data)

            if type(single_unclean_data) in DICT_KIND:
                validated_single_clean_data = {}

                for key, value in single_unclean_data.items():
                    single_clean_data = get_excel_writable_data_from_input_data(value)
                    if type(single_clean_data) in DICT_KIND:
                        for (
                            key_clean_data,
                            value_clean_data,
                        ) in single_clean_data.items():
                            validated_single_clean_data[
                                f"{key}__{key_clean_data}"
                            ] = value_clean_data
                    else:
                        validated_single_clean_data[key] = single_clean_data

                output_clean_data.append(validated_single_clean_data)
            else:
                output_clean_data.append(
                    get_excel_writable_data_from_input_data(single_unclean_data)
                )

        return output_clean_data

    # something is not handled
    return [
        {
            "detail": f"{type(input_unclean_data)} is not handled in the BE, this is a temp BE issue."
        }
    ]


def write_data_to_excel_and_get_public_url(input_data: list, request) -> str:
    """
    For a given list of data, passes it to the above mentioned functions and creates the excel
    file by getting the validated data and writing it in the excel, also returns the public url of the file.
    Used in bulk export and other export actions.
    """

    base_media_url = f"{request._current_scheme_host}{settings.MEDIA_URL}"
    clean_data_to_write = get_excel_writable_data_from_input_data(input_data)
    file_media_path = write_list_of_dict_to_excel(
        data_list=[clean_data_to_write], is_temporary_file=True
    )
    return f"{base_media_url}{file_media_path}"


def clean_excel_input(input_data):
    """Simple cleaning for the excel data. Converts raw excel data to python data."""

    data = input_data

    if type(data) == float:
        data = str(data).split(".")[0]

    data = str(data).strip()

    if data.lower() == "false":
        data = False
    if data.lower() == "true":
        data = True
    if data == "" or len(data) <= 0:
        return None

    return data


def get_data_as_list_of_dict_from_excel_file(
    excel_file_config: dict,
    input_indexes_and_dict_keys: dict,
    excel_sheet_index: int = 0,
    starting_row: int = 1,
    extra_keys_and_values: dict = None,
    key_and_function={},
    read_other_excel_data=False,
):
    """
    Reads a given excel sheet. Cleans it and performs small operations.
    Stores the data as a list of dict and returns it. When read_other_excel_data is passed as True,
    this function will get the other data passed in the excel sheet as an input list and passes it as
    `other_excel_data` key in the single_dict.

    @params:
        input_indexes_and_dict_keys:    -> A dict to specify index of input and key of output dict
        extra_keys_and_values:          -> Add extra keys and values, to the output, if necessary
        excel_sheet_index:              -> Sheet in the excel sheet where the data is present | this is an integer
        starting_row:                   -> Row in the sheet to start getting to data | for omitting the headings | int
        excel_file_config               -> Contains file config that can be read, this contains the input data
    """

    print("Reading file...")
    wb = xlrd.open_workbook(**excel_file_config)
    sheet = wb.sheet_by_index(excel_sheet_index)
    sheet.cell_value(0, 0)
    nr = sheet.nrows

    output_list = []
    print("Reading data...")
    for row in range(starting_row, nr):
        data_dict = {}
        for col_index, dict_key in input_indexes_and_dict_keys.items():
            single_col_data = sheet.cell_value(row, col_index)

            # clean a few things
            single_col_data = clean_excel_input(single_col_data)

            # pass the value to func, if passed
            if dict_key in key_and_function.keys():
                single_col_data = key_and_function[dict_key](single_col_data)

            data_dict[dict_key] = single_col_data

        # add extra key values,
        if extra_keys_and_values:
            for key, value in extra_keys_and_values.items():
                if key not in data_dict.keys():
                    data_dict[key] = value

        if read_other_excel_data:
            # if the other columns data are also to be read
            other_excel_data = []
            for other_index in range(len(input_indexes_and_dict_keys), sheet.ncols):
                single_col_data = sheet.cell_value(row, other_index)
                other_excel_data.append(clean_excel_input(single_col_data))
            data_dict["other_excel_data"] = other_excel_data

        # add to output list
        output_list.append(data_dict)
    print("Data read...")
    return output_list
