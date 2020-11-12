# coding: utf-8
import argparse


def get_arguments():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-j", action="store", help="Path to JSON file | Mandatory")
    arg_parser.add_argument("-k", action="store", help="Read credentials from specified key file | Optional")
    arg_parser.add_argument("-v", action="store", help="Write key results into JSON in selected directory | Optional")
    arg_parser.add_argument("-d", action="store_true", help="Display additional debug information | Optional")

    args = arg_parser.parse_args()
    return args
