'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import pdb
import logging


def log_debug(debug):
    """Function to enable the required debugging level"""
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '_charges_calc.log'
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    debug_level = debug
    if debug_level == 0:
        """This will disable all the logging"""
        logger.disabled = True
        file_handler.disabled = True
    elif debug_level == 1:
        """Error messages; This prints error and above messages"""
        logger.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)
    elif debug_level == 2:
        """WARNING messages print to console and file; Tis prints Warning and above messages"""
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)
    elif debug_level == 3:
        """DEBUG messages print to console and warning messages to file; This prints debug and above messages"""
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.WARNING)


def parse_cmd_arguments():
    """Required and optional arguments by the user"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug messages', type=int, default=0)

    return parser.parse_args()


#pdb.set_trace()


def load_rentals_file(filename):
    """Function to load the json file"""
    with open(filename) as file:
        try:
            logging.debug("loading the json data file")
            data = json.load(file)
            #logging.debug("complete json data {}".format(data))
        except:
            logging.ERROR("File not found")
            exit(0)
    return data


def calculate_additional_fields(data):
    """Function to calculate the required fields"""
    for value in data.values():
        logging.debug("calculate_additional_fields function is called from main")
        logging.debug("First value of the data {}".format(value))
        try:
            '''Try block to catch if there are empty field for dates'''
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug("Getting the rental start time")
            logging.debug("Rental start period is {}".format(rental_start))
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logging.debug("Getting the rental end time")
            logging.debug("Rental end period is {}".format(rental_end))
        except ValueError:
            logging.debug("Incorrect rental start and end date formats")
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.debug("total period of rental is  {}".format(value['total_days']))
            logging.warning("Rental start and end periods are incorrect for {}".format(value["product_code"]))
        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.warning("Cannot do square root for a negative number{}".format(value['total_price']))
            logging.debug("Cannot do square root for a negative number{}".format(value['total_price']))
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.debug("Units rented cannot be zero")

    return data


def save_to_json(filename, data):
    """Function to save the data after calculating the required fields"""
    with open(filename, 'w') as file:
        json.dump(data, file)
        #logging.debug("complete json data {}".format(data))


if __name__ == "__main__":
    args = parse_cmd_arguments()
    log_debug(args.debug)
    logging.debug(args)
    new_data = calculate_additional_fields(load_rentals_file(args.input))
    save_to_json(args.output, new_data)
