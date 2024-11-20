import json
import os
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate a Markdown summary from a SARIF file.")
parser.add_argument(
    "input_sarif", 
    type=str, 
    help="Path to the input SARIF file (e.g., checkov_analysis.sarif)."
)
parser.add_argument(
    "output_markdown", 
    type=str, 
    help="Path to the output Markdown file (e.g., sarif_summary.md)."
)
args = parser.parse_args()

input_sarif = args.input_sarif
output_markdown = args.output_markdown

def read_sarif(file_path):
    """
    Reads and parses a SARIF file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        return json.load(file)


def extract_markdown_content(run):
    """
    Extracts the findings from a SARIF run to generate Markdown content for Checkov Ansible analysis.
    """
    tool_name = run["tool"]["driver"]["name"]
    tool_version = run["tool"]["driver"].get("version", "Unknown Version")
    results = run.get("results", [])

    findings = []
    for result in results:
        rule = result.get("ruleId", "Unknown Rule")
        message = result["message"]["text"]
        locations = result.get("locations", [])

        # Gather location details
        location_info = []
        code_snippet = []
        for location in locations:
            physical_location = location.get("physicalLocation", {})
            file_path = physical_location.get("artifactLocation", {}).get("uri", "Unknown File")
            region = physical_location.get("region", {})
            start_line = region.get("startLine", "Unknown Line")

            location_info.append(f"File: {file_path}, Line: {start_line}")

            # Get code snippet if available
            snippet = region.get("snippet", {}).get("text", "")
            if snippet:
                code_snippet.append(snippet)
        
        finding = {
            "rule": rule,
            "message": message,
            "locations": location_info,
            "code_snippet": "\n".join(code_snippet) if code_snippet else "No code snippet available"
        }
        findings.append(finding)

    return tool_name, tool_version, findings


def create_markdown_summary(sarif_data, output_file):
    """
    Extracts key information from SARIF and creates a Markdown summary.
    """
    runs = sarif_data.get("runs", [])
    
    if not runs:
        raise ValueError("The SARIF file contains no runs.")
    
    with open(output_file, 'w') as md_file:
        md_file.write("# SARIF Summary Report\n\n")
        for run in runs:
            tool_name, tool_version, findings = extract_markdown_content(run)
            md_file.write(f"## Tool: {tool_name} (Version: {tool_version})\n\n")
            
            if not findings:
                md_file.write("No findings available for this tool.\n\n")
                continue

            for finding in findings:
                # Add Finding Title
                md_file.write(f"### {finding['rule']}\n\n")
                
                # Add Description
                md_file.write(f"{finding['message']}\n\n")
                
                # Add File and Line Details
                for location in finding["locations"]:
                    md_file.write(f"- {location}\n")
                
                # Add Code Snippet as YAML
                md_file.write("\n```yaml\n")
                md_file.write(f"{finding['code_snippet']}\n")
                md_file.write("```\n\n")


if __name__ == "__main__":
    try:
        # Read and parse the SARIF file
        sarif_data = read_sarif(input_sarif)
        
        # Generate Markdown summary
        create_markdown_summary(sarif_data, output_markdown)
        print(f"Markdown summary generated: {output_markdown}")
    except Exception as e:
        print(f"Error: {e}")