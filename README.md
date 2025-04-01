# MarleySpoonRecipeSelector
Marley Spoon Recipe Selector

## Getting Started

Ensure you've got the list of URLs to hit. Eg `recipe_urls.txt`. 

Install the project using poetry:
```bash
poetry install
```


## Download Recipe Data

First we need to download all the recipe data, in this case as the rendered HTML the browser sees. Everything will get saved in `/rendered_recipe_pages`. It will contain:
- The HTML
- A JSON with the URL & extracted recipe title & ingredients

```bash
poetry run python src/download_recipe.py # Generates all the recipe data
poetry run python src/json_combiner.py rendered_recipe_pages # Creates a single JSON with all extracted data
``` 

You should now have a single JSON called `combined.json` with all the extracted recipe data.


## "The App"
Thanks Claude! 👍🏾

To update the data used by the app, just push the lastest `combined.json` to github. When the app loads, it pulls data from the repo first so will automagically update.