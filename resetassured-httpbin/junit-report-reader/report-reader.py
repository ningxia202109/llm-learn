import xml.etree.ElementTree as ET
import sys
import os

from AutoGenQA import auto_gen_qa


def parse_junit_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

    return tree, root


def get_test_error(root):
    for testcase in root.findall(".//testcase"):
        failure = testcase.find("failure")
        if failure is not None:
            return failure.get("message"), failure, testcase.get("name")
    return None, None, None


def update_message(failure, additional_text):
    if failure is not None:
        original_message = failure.get("message", "")
        new_message = f"{additional_text}\n{original_message}"
        failure.set("message", new_message)


def process_junit_report(junit_report):
    tree, root = parse_junit_xml(junit_report)
    if root is None:
        return

    error_msg, failure_element, testcase_name = get_test_error(root)
    if error_msg:
        print(f"Error message found in {testcase_name}: {error_msg}")
        update_message(failure_element, f"AI message: \n{auto_gen_qa(error_msg)} \n")
        tree.write(junit_report, encoding="UTF-8", xml_declaration=True)
        print(f"Updated error message: \n{failure_element.get('message')}")


def main(junit_report_folder):
    if not os.path.isdir(junit_report_folder):
        print(f"Error: {junit_report_folder} is not a valid directory")
        return

    for filename in os.listdir(junit_report_folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(junit_report_folder, filename)
            process_junit_report(file_path)


# python resetassured-httpbin/junit-report-reader/report-reader.py resetassured-httpbin/target/surefire-reports/
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_junit_xml_folder>")
    else:
        main(sys.argv[1])
