from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
import json
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OEBPS = ROOT / "book" / "epub_build" / "OEBPS"

RECIPES = [
    ("Steamed Tomatoes", "Hylian tomato and wild greens", "tomato-basil steamed greens", "Serves: 4 | Time: 15 min | Difficulty: Easy", ["4 ripe tomatoes, halved or wedged", "4 cups spinach, chard, or tender greens", "1 tbsp olive oil", "1 garlic clove, sliced", "Pinch of salt", "Basil or parsley", "Lemon juice"], ["Set a skillet over medium heat with oil and garlic.", "Add tomatoes cut-side down and cook 2 minutes.", "Pile greens on top, sprinkle with salt, cover, and steam 4–5 minutes.", "Toss gently, finish with herbs and lemon, and serve warm."]),
    ("Cooked Stambulb", "Stambulb", "quick blistered spring onions", "Serves: 2–3 | Time: 10 min | Difficulty: Easy", ["1 bunch scallions or small spring onions", "1 tsp oil", "Pinch of salt", "Lemon wedge"], ["Trim scallions, leaving the white and tender green parts attached.", "Heat oil in a skillet until shimmering.", "Cook scallions until blistered and softened, 3–5 minutes.", "Season with salt and lemon." ]),
    ("Buttered Stambulb", "Stambulb and goat butter", "butter-glazed spring onions", "Serves: 2–3 | Time: 12 min | Difficulty: Easy", ["1 bunch scallions or spring onions", "1 tbsp butter", "1 tsp water", "Pinch of salt", "Black pepper"], ["Melt butter in a small pan and add scallions.", "Add water and cover for 2 minutes to steam.", "Uncover and cook until the butter lightly browns and coats the onions.", "Season with salt and pepper." ]),
    ("Fragrant Seafood Stew", "seafood, stambulb, and oil jar", "aromatic seafood stew with scallion oil", "Serves: 4 | Time: 30 min | Difficulty: Easy", ["1 lb mixed seafood", "1 bunch scallions, chopped", "2 tbsp olive oil", "2 garlic cloves, sliced", "1 tsp grated ginger", "3 cups seafood or vegetable stock", "1 tomato, chopped", "Salt and lemon"], ["Warm oil with scallions, garlic, and ginger until fragrant.", "Add tomato and cook until jammy.", "Pour in stock and simmer 10 minutes.", "Add seafood and cook just until done.", "Season with salt and lemon." ]),
    ("Deep-Fried Drumstick", "raw bird drumstick and oil jar", "crispy shallow-fried chicken drumsticks", "Serves: 4 | Time: 45 min plus rest | Difficulty: Medium", ["8 chicken drumsticks", "1 cup buttermilk or yogurt", "1 cup flour", "1 tsp paprika", "1 tsp salt", "1/2 tsp pepper", "Oil for shallow frying"], ["Coat drumsticks in buttermilk and rest 20 minutes or overnight.", "Mix flour with paprika, salt, and pepper.", "Dredge chicken, then fry in 1 inch of oil, turning often, until crisp and 165°F / 74°C inside.", "Drain and salt lightly." ]),
    ("Deep-Fried Thigh", "raw bird thigh and oil jar", "crispy boneless chicken thighs", "Serves: 4 | Time: 35 min | Difficulty: Medium", ["1 1/2 lb boneless chicken thighs", "1 egg", "1/2 cup flour", "1/2 cup cornstarch", "1 tsp salt", "1 tsp garlic powder", "Oil for frying"], ["Cut thighs into large pieces and coat with beaten egg.", "Mix flour, cornstarch, salt, and garlic powder.", "Dredge chicken and fry until deeply golden and cooked through.", "Rest on a rack so the crust stays crisp." ]),
    ("Deep-Fried Bird Roast", "raw whole bird and oil jar", "festival fried roast chicken pieces", "Serves: 4–6 | Time: 1 hr | Difficulty: Medium", ["1 small chicken, cut into pieces", "1 cup buttermilk", "1 1/2 cups flour", "1 tsp salt", "1 tsp smoked paprika", "1/2 tsp thyme", "Oil for frying"], ["Marinate chicken pieces in buttermilk at least 30 minutes.", "Season flour with salt, paprika, and thyme.", "Dredge chicken, then fry in batches until crisp and cooked through.", "Keep warm on a rack in a low oven while finishing batches." ]),
    ("Simmered Tomato", "Hylian tomato", "simple warm tomato bowl", "Serves: 2 | Time: 15 min | Difficulty: Easy", ["4 ripe tomatoes, chopped", "1 tbsp olive oil", "1 small garlic clove", "Pinch of salt", "Basil or parsley"], ["Warm oil and garlic in a small pot.", "Add tomatoes and salt.", "Simmer 8–10 minutes until saucy but still bright.", "Finish with herbs and eat with bread or rice." ]),
    ("Fruity Tomato Stew", "Hylian tomato, milk, and rock salt", "creamy tomato-fruit bisque", "Serves: 4 | Time: 25 min | Difficulty: Easy", ["5 ripe tomatoes", "1 peach or small apple, diced", "1 tbsp butter", "1 cup milk or cream", "1 cup vegetable stock", "Salt and pepper", "Basil"], ["Cook tomatoes and fruit in butter until softened.", "Add stock and simmer 10 minutes.", "Blend smooth, then stir in milk.", "Season with salt, pepper, and basil." ]),
    ("Tomato Mushroom Stew", "Hylian tomato and mushrooms", "tomato-mushroom skillet stew", "Serves: 4 | Time: 30 min | Difficulty: Easy", ["1 lb mushrooms, sliced", "4 tomatoes, chopped", "1 onion, diced", "2 tbsp olive oil", "1 tsp thyme", "Salt and pepper"], ["Brown mushrooms in oil until their liquid cooks off.", "Add onion and thyme; cook until soft.", "Add tomatoes, salt, and pepper.", "Simmer until thick and savory." ]),
    ("Tomato Seafood Soup", "seafood and Hylian tomato", "tomato fish soup", "Serves: 4 | Time: 30 min | Difficulty: Easy", ["1 lb white fish or shrimp", "4 tomatoes, chopped", "2 cups seafood stock", "1 garlic clove", "1 tbsp olive oil", "Salt, pepper, lemon"], ["Warm oil with garlic, then add tomatoes.", "Cook until tomatoes collapse.", "Add stock and simmer 10 minutes.", "Add seafood and cook gently until done.", "Finish with lemon." ]),
    ("Cheesy Curry", "Hateno cheese, rice, and Goron spice", "cheese-topped curry rice", "Serves: 4 | Time: 35 min | Difficulty: Easy", ["2 cups cooked rice", "1 onion, sliced", "2 carrots, chopped", "2 cups stock", "Japanese curry roux or curry powder slurry", "1 cup shredded cheese"], ["Cook onion and carrots until softened.", "Add stock and simmer until tender.", "Stir in curry roux until glossy.", "Spoon over rice, top with cheese, and broil or cover until melted." ]),
    ("Cheesy Risotto", "rice, salt, Hateno cheese, and fish/mushrooms/greens", "flexible cheese risotto", "Serves: 4 | Time: 40 min | Difficulty: Medium", ["1 cup arborio rice", "4 cups warm stock", "1 tbsp butter", "1 shallot, minced", "1 cup mushrooms, greens, or cooked fish", "3/4 cup shredded cheese", "Salt and pepper"], ["Cook shallot in butter, then toast rice for 2 minutes.", "Add stock a ladle at a time, stirring until absorbed.", "Fold in mushrooms, greens, or fish.", "Melt in cheese and season well." ]),
    ("Crunchy Fried Rice", "meat, rice, egg, and oil jar", "crispy egg fried rice", "Serves: 2–3 | Time: 20 min | Difficulty: Easy", ["3 cups cold cooked rice", "1/2 lb cooked meat, diced", "2 eggs", "2 tbsp oil", "1 tbsp soy sauce", "1 scallion", "Salt and pepper"], ["Heat oil in a wide skillet and press rice into a thin layer.", "Let it crisp before stirring.", "Add meat and soy sauce.", "Push rice aside, scramble eggs, then fold together with scallion." ]),
    ("Cheesy Meat Bowl", "meat, rice, salt, and Hateno cheese", "melty ground meat rice bowl", "Serves: 2 | Time: 20 min | Difficulty: Easy", ["2 cups hot rice", "1/2 lb ground beef, pork, turkey, or mushrooms", "1 tsp soy sauce", "1/2 cup shredded cheese", "Salt and pepper", "Scallion"], ["Brown meat with salt and pepper.", "Add soy sauce and cook until glossy.", "Spoon over hot rice.", "Top with cheese, cover for 1 minute to melt, and finish with scallion." ]),
    ("Prime Cheesy Meat Bowl", "prime meat, rice, salt, and Hateno cheese", "sirloin cheese rice bowl", "Serves: 2 | Time: 25 min | Difficulty: Easy", ["10 oz sirloin or pork loin", "2 cups hot rice", "1 tbsp oil", "1 tbsp butter", "1/2 cup shredded cheese", "Salt and pepper"], ["Season and sear meat in oil.", "Rest, slice, and melt butter in the pan.", "Serve over rice with pan butter and cheese.", "Cover briefly so the cheese softens." ]),
    ("Gourmet Cheesy Meat Bowl", "gourmet meat, rice, salt, and Hateno cheese", "steakhouse cheese rice bowl", "Serves: 2 | Time: 30 min | Difficulty: Medium", ["12 oz steak", "2 cups hot rice", "1 tbsp oil", "1 tbsp butter", "3/4 cup sharp cheese", "Salt, pepper, and chives"], ["Sear steak to your liking and rest.", "Slice over rice.", "Add butter to the hot pan and spoon over the bowl.", "Top with cheese and chives." ]),
    ("Veggie Porridge", "milk, rice, and wild greens", "gentle green rice porridge", "Serves: 4 | Time: 35 min | Difficulty: Easy", ["1 cup rice", "4 cups vegetable stock", "1 cup milk", "2 cups chopped greens", "1 tbsp butter", "Salt and pepper"], ["Simmer rice in stock until very soft, 25–30 minutes.", "Stir in milk, greens, and butter.", "Cook until creamy and green-flecked.", "Season with salt and pepper." ]),
    ("Melty Cheesy Bread", "Hateno cheese and Tabantha wheat", "toasted cheese flatbread", "Serves: 2–4 | Time: 15 min | Difficulty: Easy", ["1 flatbread or small loaf split open", "1 cup shredded cheese", "1 tbsp butter", "Pinch garlic powder", "Parsley"], ["Butter the bread and sprinkle with garlic powder.", "Pile on cheese.", "Bake at 425°F / 220°C until melted and browned.", "Finish with parsley and cut into wedges." ]),
    ("Hylian Tomato Pizza", "Hateno cheese, Hylian tomato, and wheat", "tomato cheese skillet pizza", "Makes: 1 small pizza | Time: 35 min | Difficulty: Easy", ["1 pizza dough or flatbread", "2 tomatoes, sliced", "1 cup shredded mozzarella or farmer cheese", "1 tbsp olive oil", "Salt", "Basil"], ["Heat oven to 475°F / 245°C.", "Stretch dough and brush with oil.", "Top with tomatoes, cheese, and salt.", "Bake until the crust is browned and cheese bubbles.", "Finish with basil." ]),
    ("Cheesy Tomato", "Hateno cheese and Hylian tomato", "broiled cheese tomatoes", "Serves: 2–3 | Time: 12 min | Difficulty: Easy", ["3 tomatoes, halved", "3/4 cup shredded cheese", "1 tsp olive oil", "Pinch of salt", "Black pepper", "Basil or oregano"], ["Place tomatoes cut-side up on a tray.", "Season with oil, salt, pepper, and herbs.", "Cover with cheese.", "Broil until bubbling and browned at the edges." ]),
    ("Cheesy Baked Fish", "Hateno cheese and fish", "baked fish with cheese crust", "Serves: 4 | Time: 25 min | Difficulty: Easy", ["4 white fish fillets", "1/2 cup shredded cheese", "1/4 cup breadcrumbs", "1 tbsp butter, melted", "Salt and pepper", "Lemon wedges"], ["Heat oven to 400°F / 200°C.", "Season fish and place in a baking dish.", "Mix cheese, crumbs, and butter; press over fish.", "Bake 12–15 minutes until fish flakes and topping browns." ]),
    ("Cheesy Omelet", "egg, cheese, butter, salt, and vegetables", "soft cheese-and-greens omelet", "Serves: 1–2 | Time: 12 min | Difficulty: Easy", ["3 eggs", "1 tbsp butter", "1/2 cup shredded cheese", "1/2 cup sautéed mushrooms or greens", "Salt and pepper"], ["Beat eggs with salt and pepper.", "Melt butter in a nonstick pan.", "Add eggs and stir gently until soft curds form.", "Add cheese and vegetables, fold, and serve while melty." ]),
    ("Cheesecake", "Hateno cheese, wheat, sugar, and goat butter", "small farmer-cheese cheesecake", "Makes: 8 slices | Time: 1 hr plus chilling | Difficulty: Medium", ["1 cup graham crumbs or crushed biscuits", "3 tbsp melted butter", "12 oz cream cheese or farmer cheese", "1/2 cup sugar", "2 eggs", "1 tsp vanilla", "Pinch salt"], ["Heat oven to 325°F / 160°C.", "Mix crumbs with butter and press into a small pan.", "Beat cheese, sugar, eggs, vanilla, and salt until smooth.", "Bake 35–40 minutes until barely set.", "Chill before slicing." ]),
    ("Noble Pursuit", "palm fruit, hydromelon, voltfruit, and rock salt", "citrus-melon mocktail with a salted rim", "Makes: 2 drinks | Time: 10 min | Difficulty: Easy", ["1 cup watermelon or cantaloupe", "1/2 cup pineapple or mango", "1/2 cup coconut water", "Juice of 1 lime", "Sparkling water", "Pinch of salt", "Ice"], ["Blend melon, pineapple, coconut water, lime, and salt.", "Strain if desired.", "Pour over ice and top with sparkling water.", "Serve with a lightly salted rim." ]),
    ("Dark Stew", "dark clump, fish, and meat", "black garlic surf-and-turf stew", "Serves: 4 | Time: 1 hr | Difficulty: Medium", ["3/4 lb beef or sausage", "3/4 lb white fish or shrimp", "1 onion, diced", "2 cups stock", "1 cup crushed tomatoes", "1 tsp black garlic paste or balsamic glaze", "Salt and pepper"], ["Brown meat with onion.", "Add stock, tomatoes, black garlic, salt, and pepper.", "Simmer 35 minutes.", "Add seafood and cook just until done." ]),
    ("Dark Soup", "dark clump, milk, wheat, and goat butter", "shadowy creamy mushroom soup", "Serves: 4 | Time: 35 min | Difficulty: Easy", ["1 lb mushrooms", "2 tbsp butter", "2 tbsp flour", "3 cups stock", "1 cup milk", "1 tsp black garlic or balsamic glaze", "Salt and pepper"], ["Brown mushrooms deeply in butter.", "Stir in flour, then stock.", "Simmer 15 minutes.", "Add milk and black garlic.", "Blend partly and season." ]),
    ("Dark Curry", "dark clump, Goron spice, and rice", "black garlic curry rice", "Serves: 4 | Time: 40 min | Difficulty: Easy", ["2 cups cooked rice", "1 onion, sliced", "2 carrots, chopped", "2 cups stock", "Japanese curry roux", "1 tsp black garlic paste or molasses", "Oil"], ["Cook onion in oil until deeply golden.", "Add carrots and stock; simmer until tender.", "Stir in curry roux and black garlic.", "Serve over rice." ]),
    ("Dark Rice Ball", "dark clump, salt, and rice", "black sesame rice balls", "Makes: 6 | Time: 25 min | Difficulty: Easy", ["3 cups cooked short-grain rice", "2 tbsp black sesame paste or crushed black sesame", "1 tsp soy sauce", "Pinch of salt", "Optional nori"], ["Mix hot rice with sesame paste, soy sauce, and salt until streaked dark.", "Wet your hands and shape into balls or triangles.", "Wrap with nori if desired." ]),
    ("Dark Cake", "dark clump, sugar, butter, and wheat", "black cocoa snack cake", "Makes: 8 slices | Time: 55 min | Difficulty: Easy", ["1 cup flour", "1/2 cup black cocoa", "3/4 cup sugar", "1 tsp baking powder", "1/2 tsp salt", "1 egg", "1/2 cup milk", "1/4 cup melted butter"], ["Heat oven to 350°F / 175°C and grease an 8-inch pan.", "Whisk dry ingredients.", "Add egg, milk, and butter; mix until smooth.", "Bake 28–34 minutes and cool before slicing." ]),
    ("Bright Elixir", "deep firefly and monster part", "glowing lemon-ginger tonic", "Makes: 2 drinks | Time: 10 min | Difficulty: Easy", ["2 cups sparkling water", "Juice of 1 lemon", "1 tbsp honey", "1/2 tsp grated ginger", "Pinch turmeric", "Ice"], ["Stir lemon, honey, ginger, and turmeric until dissolved.", "Pour over ice.", "Top with sparkling water and stir gently.", "Serve when you need a little cave-light courage." ]),
    ("Sticky Elixir", "sticky lizard or frog and monster part", "lime-chia grip tonic", "Makes: 2 drinks | Time: 10 min plus resting | Difficulty: Easy", ["2 cups coconut water or cold green tea", "Juice of 2 limes", "1 tbsp honey", "1 tbsp chia seeds", "Pinch of salt", "Ice"], ["Stir coconut water, lime, honey, salt, and chia.", "Rest 10 minutes so the chia lightly gels.", "Pour over ice and stir before drinking." ]),
]

DUPLICATE_NOTES = [
    "Honey Candy / Honey Crepe overlap with the existing Energizing Honey Candy and Energizing Honey Crepe pages.",
    "Milk overlaps with the existing Warm Milk page.",
    "Snail Chowder overlaps with the existing shellfish chowder adaptation.",
    "Sauteed Nuts, Herb Saute, Fragrant Mushroom Saute, and the Meuniere spellings overlap existing accent/spelling variants.",
]


def recipe_md(recipe):
    title, inspired, real, meta, ingredients, method = recipe
    lines = [f"### {title}", f"**Inspired by:** {inspired}  ", f"**Real-world version:** {real}  ", f"**{meta}**", "", "**Ingredients**"]
    lines += [f"- {item}" for item in ingredients]
    lines += ["", "**Method**"]
    lines += [f"{i}. {step}" for i, step in enumerate(method, 1)]
    lines += [""]
    return "\n".join(lines)


def recipe_xhtml(recipe):
    title, inspired, real, meta, ingredients, method = recipe
    html = [f"<h3>{escape(title)}</h3>", f"<p><strong>Inspired by:</strong> {escape(inspired)}<br/>", f"<strong>Real-world version:</strong> {escape(real)}<br/>", f"<strong>{escape(meta)}</strong></p>", "<p><strong>Ingredients</strong></p>", "<ul>"]
    html += [f"<li>{escape(item)}</li>" for item in ingredients]
    html += ["</ul>", "<p><strong>Method</strong></p>", "<ol>"]
    html += [f"<li>{escape(step)}</li>" for step in method]
    html += ["</ol>", "<hr/>"]
    return "\n".join(html)


def write_epub():
    title = "Chapter VI — Tears of the Kingdom Additions"
    body = ["<?xml version=\"1.0\" encoding=\"utf-8\"?>", "<!DOCTYPE html>", f"<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\"><head><title>{escape(title)}</title><link rel=\"stylesheet\" type=\"text/css\" href=\"styles/style.css\"/></head><body><main class=\"book\"><h1>{escape(title)}</h1>", "<p>These are original real-world adaptations for Tears of the Kingdom recipe names that do not already have an equivalent page in the Breath of the Wild manuscript.</p>", "<p><strong>Duplicate handling:</strong> near-identical honey, milk, sauté, meunière, and chowder variants were intentionally not repeated as full pages.</p>"]
    body += [recipe_xhtml(r) for r in RECIPES]
    body.append("</main></body></html>")
    (OEBPS / "chapter11.xhtml").write_text("\n".join(body), encoding="utf-8")

    nav = (OEBPS / "nav.xhtml").read_text(encoding="utf-8")
    if "chapter11.xhtml" not in nav:
        nav = nav.replace("<li><a href=\"chapter10.xhtml\">Appendix D — Frozen Food Checklist</a></li></ol>", "<li><a href=\"chapter10.xhtml\">Appendix D — Frozen Food Checklist</a></li>\n<li><a href=\"chapter11.xhtml\">Chapter VI — Tears of the Kingdom Additions</a></li></ol>")
        (OEBPS / "nav.xhtml").write_text(nav, encoding="utf-8")

    opf = (OEBPS / "content.opf").read_text(encoding="utf-8")
    opf = re.sub(r"<meta property=\"dcterms:modified\">.*?</meta>", f"<meta property=\"dcterms:modified\">{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>", opf)
    if "chapter11.xhtml" not in opf:
        opf = opf.replace("<item id=\"chap10\" href=\"chapter10.xhtml\" media-type=\"application/xhtml+xml\"/>", "<item id=\"chap10\" href=\"chapter10.xhtml\" media-type=\"application/xhtml+xml\"/>\n<item id=\"chap11\" href=\"chapter11.xhtml\" media-type=\"application/xhtml+xml\"/>")
        opf = opf.replace("<itemref idref=\"chap10\"/>", "<itemref idref=\"chap10\"/>\n<itemref idref=\"chap11\"/>")
    (OEBPS / "content.opf").write_text(opf, encoding="utf-8")


def update_manuscript():
    path = ROOT / "manuscript" / "The_Wild_Table_v0.5.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("**Status:** working manuscript / 128 full recipe pages drafted; all cooking pot meals and elixirs adapted", "**Status:** working manuscript / 160 full recipe pages drafted; Breath of the Wild set plus non-duplicate Tears of the Kingdom additions adapted")
    text = text.replace("## An Unofficial Real-World Cookbook Inspired by Breath of the Wild", "## An Unofficial Real-World Cookbook Inspired by Breath of the Wild and Tears of the Kingdom")
    if "# Chapter VI — Tears of the Kingdom Additions" not in text:
        addition = ["", "---", "", "# Chapter VI — Tears of the Kingdom Additions", "", "This chapter adds original real-world adaptations for Tears of the Kingdom recipe names that do not already duplicate a page in the earlier Breath of the Wild recipe set.", "", "**Source note:** Recipe names and ingredient categories were cross-checked against Game8's Tears of the Kingdom cooked-dish and elixir recipe lists. The recipes below are original adaptations, not copied game text.", "", "**Intentionally not repeated:**"]
        addition += [f"- {note}" for note in DUPLICATE_NOTES]
        addition += [""]
        addition += [recipe_md(r) + "---\n" for r in RECIPES]
        text += "\n".join(addition)
    path.write_text(text, encoding="utf-8")


def update_book_html():
    path = ROOT / "book" / "The_Wild_Table.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace("An Unofficial Real-World Cookbook Inspired by Breath of the Wild", "An Unofficial Real-World Cookbook Inspired by Breath of the Wild and Tears of the Kingdom")
    if "Chapter VI — Tears of the Kingdom Additions" not in text:
        chapter = ["<h1>Chapter VI — Tears of the Kingdom Additions</h1>", "<p>Original real-world adaptations for Tears of the Kingdom recipe names that do not already duplicate a page in the earlier recipe set.</p>"]
        chapter += [recipe_xhtml(r) for r in RECIPES]
        text = text.replace("</main></body></html>", "\n" + "\n".join(chapter) + "\n</main></body></html>")
    path.write_text(text, encoding="utf-8")


def update_readme():
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("inspired by Breath of the Wild cooking", "inspired by Breath of the Wild and Tears of the Kingdom cooking")
    text = text.replace("expanded literal book manuscript with all cooking pot meals and all elixirs adapted into full recipe pages.", "expanded literal book manuscript with the Breath of the Wild set plus non-duplicate Tears of the Kingdom additions adapted into full recipe pages.")
    text = text.replace("Catalogued 116 cooking pot meals, 12 elixirs, 46 roasted foods, and 13 frozen foods.\n- Drafted 128 full real-life recipe pages; all 116 cooking pot meals and all 12 elixirs are now adapted.", "Catalogued the original 116 cooking pot meals, 12 elixirs, 46 roasted foods, and 13 frozen foods, then cross-checked Tears of the Kingdom additions.\n- Drafted 160 full real-life recipe pages, including 32 non-duplicate Tears of the Kingdom additions.")
    if "data/totk_game8_recipes.json" not in text:
        text = text.replace("- `data/botw_food_source_extract.csv` — spreadsheet-friendly catalog.", "- `data/botw_food_source_extract.csv` — spreadsheet-friendly catalog.\n- `data/totk_game8_recipes.json` — scraped planning reference for Tears of the Kingdom cooked dishes and elixirs from Game8, used for duplicate screening.")
    path.write_text(text, encoding="utf-8")


def update_build_pages():
    path = ROOT / "build_pages.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("range(1, 11)", "range(1, 12)")
    text = text.replace("inspired by Breath of the Wild</p>", "inspired by Breath of the Wild and Tears of the Kingdom</p>")
    path.write_text(text, encoding="utf-8")


def rebuild_epub_file():
    epub = ROOT / "book" / "The_Wild_Table.epub"
    build = ROOT / "book" / "epub_build"
    if epub.exists():
        epub.unlink()
    with zipfile.ZipFile(epub, "w") as zf:
        zf.write(build / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for p in sorted(build.rglob("*")):
            if p.is_file() and p.name != "mimetype":
                zf.write(p, p.relative_to(build).as_posix(), compress_type=zipfile.ZIP_DEFLATED)


def main():
    update_manuscript()
    write_epub()
    update_book_html()
    update_readme()
    update_build_pages()
    rebuild_epub_file()
    # Build GitHub Pages output and copy updated epub into docs/book.
    import subprocess
    subprocess.run(["python3", "build_pages.py"], cwd=ROOT, check=True)
    shutil.copy2(ROOT / "book" / "The_Wild_Table.epub", ROOT / "docs" / "book" / "The_Wild_Table.epub")
    print(f"Added {len(RECIPES)} non-duplicate Tears of the Kingdom recipe pages.")


if __name__ == "__main__":
    main()
