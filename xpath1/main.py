
import argparse
import requests
from lxml import html
import json
import csv

def extract_data(url, xpath_query, response_format):
    response = requests.get(url)
    tree = html.fromstring(response.content)

    # Execute the XPath query
    data = tree.xpath(xpath_query)

    if response_format == "json":
        # Convert data to JSON
        json_data = json.dumps(data, indent=2)
        print(json_data)
    elif response_format == "xml":
        # Convert data to XML (assuming it's already in XML format)
        xml_data = html.tostring(data[0], pretty_print=True).decode("utf-8")
        print(xml_data)
    elif response_format == "csv":
        # Assuming data is a list of dictionaries
        keys = data[0].keys()
        with open("output.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print("Data saved to output.csv")
    elif response_format == "txt":
        # Assuming data is a list of strings
        for item in data:
            print(item)
    else:
        print("Invalid response format specified.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract data using XPath from a given URL.")
    parser.add_argument("--url", required=True, help="URL to extract data from")
    parser.add_argument("--xpath", required=True, help="XPath query")
    parser.add_argument("--format", required=True, choices=["json", "xml", "csv", "txt"], help="Response format")

    args = parser.parse_args()
    extract_data(args.url, args.xpath, args.format)