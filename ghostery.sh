#!/bin/bash

# Output directory to store the results
OUTPUT_DIR="input/Ghostery"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

types=("Google" "Facebook")

# Loop through each element in the list
for element in "${types[@]}"; do
    # File containing the list of domains (one per line)
    INPUT_FILE="input/Receiver/$element.txt"
    # CSV output file
    CSV_FILE="$OUTPUT_DIR/3rd_$element.csv"

    # Write the CSV header
    echo "input|domain|name of organization|name of category" > "$CSV_FILE"

    # Check if the input file exists
    if [[ ! -f "$INPUT_FILE" ]]; then
        echo "File $INPUT_FILE not found!"
    exit 1
    fi

    # Loop through each domain in the file
    
    #while IFS= read -r domain || [[ -n "$domain" ]]
    #do
    while IFS= read -r domain; do
        # Query the domain and get the JSON output
        echo "$domain"
        json_output=$(npx @ghostery/trackerdb "$domain" 2>/dev/null)

        # Check if the output is valid JSON
        if echo "$json_output" | jq empty 2>/dev/null; then
            # Check if there are any matches
            matches_count=$(echo "$json_output" | jq '.matches | length')
    
            if [[ $matches_count -gt 0 ]]; then
                # Extract required fields using jq and append to CSV
                echo "$json_output" | jq --arg v "$domain" -r '.matches[] | "\($v)|\(.pattern.domains[0])|\(.organization.name)|\(.category.name)"' >> "$CSV_FILE"
                echo "Processed $domain..."
            else
                # No matches found, write "None" for organization and category
                echo "$domain|$domain|None|None" >> "$CSV_FILE"
                echo "No matches found for $domain..."
            fi
        else
            # Invalid JSON, but still write "None" for organization and category
            echo "$domain|$domain|None|None" >> "$CSV_FILE"
            echo "Warning: Invalid JSON output for $domain, recorded as None|None..."
        fi
    done < "$INPUT_FILE"

    echo "Results saved to $CSV_FILE"

done



