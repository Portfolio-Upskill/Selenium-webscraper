import os
import xml.etree.ElementTree as ET
from datetime import datetime
import sys

def generate_html_report(xml_path):
    """Generates an HTML report from the latest XML test report."""
    
    # --- 1. Determine output directory based on XML path ---
    output_base_dir = os.path.dirname(xml_path)
    
    # --- 2. Parse the XML report ---
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    test_cases = []
    for i, testcase in enumerate(root.iter('testcase')):
        test_name = testcase.get('name')
        test_description = testcase.get('doc') or test_name
        
        status = 'Pass'
        if testcase.find('failure') is not None:
            status = 'Fail'
        elif testcase.find('error') is not None:
            status = 'Error'
            
        screenshot_path = f"{test_name}.png"
        
        test_cases.append({
            'number': i + 1,
            'name': test_name,
            'description': test_description,
            'status': status,
            'screenshot': screenshot_path
        })
        
    # --- 3. Generate the HTML report ---
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"test_report_{now}.html"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Report</title>
        <style>
            body {{ font-family: sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            .status-pass {{ color: green; }}
            .status-fail {{ color: red; }}
            .status-error {{ color: orange; }}
        </style>
    </head>
    <body>
        <h1>Test Report</h1>
        <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <table>
            <tr>
                <th>Test Case #</th>
                <th>Test Case Description</th>
                <th>Status</th>
                <th>Screenshot</th>
            </tr>
    """
    
    for tc in test_cases:
        status_class = f"status-{tc['status'].lower()}"
        html += f"""
            <tr>
                <td>{tc['number']}</td>
                <td>{tc['description']}</td>
                <td class="{status_class}">{tc['status']}</td>
                <td><a href="{tc['screenshot']}" target="_blank">View Screenshot</a></td>
            </tr>
        """
        
    html += """
        </table>
    </body>
    </html>
    """
    
    report_path = os.path.join(output_base_dir, report_filename)
    with open(report_path, 'w') as f:
        f.write(html)
        
    print(f"HTML report generated at: {report_path}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        xml_report_path = sys.argv[1]
        generate_html_report(xml_report_path)
    else:
        print("Usage: python generate_html_report.py <path_to_xml_report>")
