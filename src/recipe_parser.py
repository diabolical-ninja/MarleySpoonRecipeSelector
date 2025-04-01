import glob
import json
import os
import re
import sys


def extract_recipe_info(html_content):
    # Extract the recipe title
    recipe_title_regex = r'<h1 class="recipe-title">(.*?)<span class="recipe-subtitle">'
    recipe_title_match = re.search(recipe_title_regex, html_content, re.DOTALL)

    title = ""
    if recipe_title_match:
        title = recipe_title_match.group(1).strip()
    else:
        # Fallback to title tag if recipe title not found
        title_tag_regex = r"<title>(.*?)\s*\|"
        title_tag_match = re.search(title_tag_regex, html_content)
        if title_tag_match:
            title = title_tag_match.group(1).strip()

    # Extract ingredients from "What we send" section
    ingredients = []
    ingredient_send_regex = r'<div class="dish-detail__ingredient.*?<p>(.*?)<\/p>'
    for match in re.finditer(ingredient_send_regex, html_content, re.DOTALL):
        ingredient = match.group(1).strip()
        ingredients.append(ingredient)

    # Extract ingredients from "What you'll need" section
    what_you_need_section_regex = r"<h5>What you\'ll need<\/h5>.*?<ul>(.*?)<\/ul>"
    what_you_need_match = re.search(
        what_you_need_section_regex, html_content, re.DOTALL
    )

    if what_you_need_match:
        what_you_need_content = what_you_need_match.group(1)
        ingredient_need_regex = r"<li><span>(.*?)<\/span><\/li>"

        for match in re.finditer(
            ingredient_need_regex, what_you_need_content, re.DOTALL
        ):
            ingredient = match.group(1).strip()
            ingredients.append(ingredient)

    # Prepare the result
    result = {"title": title, "ingredients": ingredients}

    return result


def process_single_file(html_file):
    """Process a single HTML file and return recipe info."""
    try:
        # Read the HTML file
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Extract recipe information
        recipe_info = extract_recipe_info(html_content)
        return recipe_info

    except Exception as e:
        print(f"Error processing {html_file}: {str(e)}")
        return None


def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Process all files: python recipe_parser.py --all")
        print("  Process single file: python recipe_parser.py <html_file>")
        sys.exit(1)

    # Process all HTML files in the folder
    if sys.argv[1] == "--all":
        folder_path = "rendered_recipe_pages"
        if not os.path.exists(folder_path):
            print(f"Error: Folder '{folder_path}' not found")
            sys.exit(1)

        # Get all HTML files in the folder
        html_files = glob.glob(os.path.join(folder_path, "*.html"))

        if not html_files:
            print(f"No HTML files found in '{folder_path}'")
            sys.exit(1)

        # Process each file and store results
        all_recipes = []
        for html_file in html_files:
            file_name = os.path.basename(html_file)
            print(f"Processing {file_name}...")
            recipe_info = process_single_file(html_file)
            if recipe_info:
                all_recipes.append(recipe_info)

        # Save all results to a single JSON file
        output_file = "all_recipes.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_recipes, f, indent=2)

        print(f"\nProcessed {len(all_recipes)} files. Results saved to {output_file}")

    # Process a single file
    else:
        html_file = sys.argv[1]
        if not os.path.exists(html_file):
            print(f"Error: File '{html_file}' not found")
            sys.exit(1)

        recipe_info = process_single_file(html_file)
        if recipe_info:
            # Print the result as JSON
            print(json.dumps(recipe_info, indent=2))


if __name__ == "__main__":
    main()
