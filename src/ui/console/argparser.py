# coding: utf-8
import argparse


def get_arguments():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-k", action="store_true", help="Read credentials from key file | Optional")
    arg_parser.add_argument("-j", action="store", help="Path to JSON file | Mandatory")

    args = arg_parser.parse_args()
    return args
