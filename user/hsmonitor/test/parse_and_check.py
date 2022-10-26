"""Common routine for parsing messages and checking the result"""

from EventExportValues import export_values


def parse_and_check_data(test, data, type_code, parser, upload_code):
    """

    :param filename: path to the text file to read relative to this script.
    :return: the message from the text file.

    """
    data_parser = parser([type_code, data])
    data_parser.uploadCode = upload_code
    parsed_data = data_parser.parseMessage()
    keys = [data_item['data_uploadcode'] for data_item in parsed_data]
    export_keys = [key[0] for key in export_values[upload_code]]
    test.assertEqual([key for key in keys if key not in export_keys], [])
    # HiSPARC Event test data does not include Secondary data, and new HiSPARC
    # configs do not include 'expert password', so lengths will not match.
    if type_code not in [1, 3]:
        test.assertEqual(len(parsed_data), len(export_values[upload_code]))
