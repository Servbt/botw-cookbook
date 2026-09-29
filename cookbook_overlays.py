"""Authored content overlays: bespoke Skyrim methods/notes and serving notes.

These replace the templated Skyrim instruction blocks and add a line of voice
(the "serving note") that a cookbook needs to feel authored.
"""

# Skyrim: distinctive, real-cooking method per dish (replaces templated blocks).
SKYRIM_METHODS = {
    "Apple Cabbage Stew": [
        "Render a little bacon or butter in a heavy pot, then soften diced onion.",
        "Add shredded cabbage and cook until it wilts, 5 minutes.",
        "Stir in peeled diced apple, stock, and a pinch of salt; simmer 25 minutes.",
        "Finish with a knob of butter and plenty of black pepper."
    ],
    "Beef Stew": [
        "Brown cubed beef hard in batches so it develops a crust, then set aside.",
        "Sweat onion, carrot, and garlic; splash in a little ale to deglaze.",
        "Return the beef with stock and a bay leaf; simmer covered for 90 minutes.",
        "Add potatoes for the last 30 minutes, then season and rest."
    ],
    "Cabbage Potato Soup": [
        "Cook leek and cabbage in butter until sweet and soft, 8 minutes.",
        "Add diced potato and stock, simmering until the potato falls apart.",
        "Mash a few potatoes against the pot to thicken, leaving the rest whole.",
        "Season, then swirl in a spoonful of cream if you like."
    ],
    "Clam Chowder": [
        "Render bacon, then cook onion and celery in the fat until soft.",
        "Sprinkle in flour and cook 1 minute, then whisk in the clam liquor and milk.",
        "Add diced potato and simmer until tender, about 15 minutes.",
        "Fold in chopped clams and butter; warm gently without boiling."
    ],
    "Cooked Angelfish": [
        "Pat the fillets dry and salt them 10 minutes ahead.",
        "Sear skin-side down in a hot, lightly oiled pan until the skin crisps.",
        "Flip and finish 60 seconds with a knob of butter spooned over.",
        "Serve with lemon and the pan butter."
    ],
    "Cooked Angler": [
        "Cut the firm flesh into thick medallions and season well.",
        "Brown in butter over medium-high heat, resisting the urge to move them.",
        "Baste with foaming butter and a sprig of thyme for 1 minute.",
        "Rest 3 minutes so the juices settle before serving."
    ],
    "Cooked Angler Larvae": [
        "Rinse the larvae and pat completely dry.",
        "Toss in a little oil and salt, then spread in a single layer.",
        "Roast at 425°F / 220°C until crisp and golden, 12–15 minutes.",
        "Shower with lemon and eat hot like the Nordic snack they are."
    ],
    "Cooked Arctic Char": [
        "Season the char and lay it skin-side down in a cold, buttered pan.",
        "Bring the heat up slowly so the skin renders and crisps evenly.",
        "Flip once the flesh turns opaque and cook 2 minutes more.",
        "Finish with dill butter."
    ],
    "Cooked Arctic Grayling": [
        "Score the skin lightly and season inside and out.",
        "Grill over high heat, skin-side down first, until marked.",
        "Turn once and cook until it just flakes, about 3 minutes a side.",
        "Brush with browned butter and serve immediately."
    ],
    "Cooked Beef": [
        "Salt the beef and let it come to room temperature.",
        "Sear in a ripping-hot cast-iron pan to build a deep crust.",
        "Lower the heat, add butter and thyme, and baste to your preferred doneness.",
        "Rest on a board for at least 5 minutes before slicing against the grain."
    ],
    "Cooked Boar Meat": [
        "Marinate the boar in ale, garlic, and juniper for a few hours to tame it.",
        "Sear the meat hard, then lower the heat to cook it through gently.",
        "Add a splash of the marinade and reduce to a glossy sauce.",
        "Slice thinly and spoon the pan sauce over."
    ],
    "Cooked Brook Bass": [
        "Season the whole fish and stuff the cavity with lemon and herbs.",
        "Pan-fry in butter until the skin blisters and crisps.",
        "Carefully turn and cook until the eye goes white and flesh flakes.",
        "Serve with the pan butter poured over."
    ],
    "Cooked Carp": [
        "Score the thick fillets so they cook evenly.",
        "Fry in a shallow layer of hot oil until golden and crisp at the edges.",
        "Drain briefly, then season while still hot.",
        "Serve with a sharp vinegar dip to cut the richness."
    ],
    "Cooked Catfish": [
        "Soak the fillets in milk 20 minutes to mellow the flavour.",
        "Dredge in seasoned cornmeal or flour.",
        "Fry in hot oil until deeply golden and cooked through.",
        "Drain on a rack so the crust stays crisp."
    ],
    "Cooked Cod": [
        "Pat the cod dry and season generously with salt.",
        "Roast at 400°F / 200°C until the flakes separate, 12–15 minutes.",
        "Spoon over a little melted butter with parsley.",
        "Break into large flakes to serve."
    ],
    "Cooked Direfish": [
        "Season the steaks and sear in a hot, oiled skillet.",
        "Add butter and a crushed garlic clove, basting continuously.",
        "Cook to just opaque in the centre, then pull off the heat.",
        "Squeeze lemon over and rest 2 minutes."
    ],
    "Cooked Glass Catfish": [
        "Handle gently — the flesh is delicate — and season lightly.",
        "Steam over simmering water with ginger and scallion, 6–8 minutes.",
        "Dress with hot oil poured over the aromatics.",
        "Finish with soy and a whisper of sesame."
    ],
    "Cooked Glassfish": [
        "Dust the small fish in seasoned flour.",
        "Fry briefly in hot oil until crisp and just cooked.",
        "Lift out and salt immediately.",
        "Eat whole, bones and all, while hot."
    ],
    "Cooked Goldfish": [
        "Scale and clean the fish, then score the skin.",
        "Fry in a generous layer of oil until crisp and golden.",
        "Drain, then dress with a sweet-sour ginger sauce.",
        "Serve with the sauce clinging to the crisp skin."
    ],
    "Cooked Juvenile Mudcrab": [
        "Boil the small crabs in well-salted water until they turn bright.",
        "Toss hot in melted butter, garlic, and a pinch of chili.",
        "Crack the shells slightly so the butter gets in.",
        "Serve with bread for mopping."
    ],
    "Cooked Lyretail Anthias": [
        "Season the fillets and cook skin-side down in hot oil.",
        "Do not turn until the skin releases by itself and is crisp.",
        "Flip briefly to finish, then baste with butter.",
        "Plate skin-up with charred citrus."
    ],
    "Cooked Nix-Hound Meat": [
        "Trim and cube the meat, then marinate in spice and oil.",
        "Sear over high heat for colour, then lower to cook through.",
        "Add onion and pepper and a splash of stock to glaze.",
        "Finish with fresh herbs."
    ],
    "Cooked Pearlfish": [
        "Season the delicate fillets and dust lightly with flour.",
        "Pan-fry in browned butter for 2 minutes a side.",
        "Add capers and a squeeze of lemon to the pan.",
        "Spoon the caper butter over and serve."
    ],
    "Cooked Pogfish": [
        "Score the skin and season the whole fish.",
        "Grill or broil close to the heat until charred and crisp.",
        "Turn once and brush with herb oil.",
        "Serve with a wedge of lemon."
    ],
    "Cooked Pygmy Sunfish": [
        "Clean the tiny fish and toss in seasoned flour.",
        "Flash-fry in hot oil until shatteringly crisp, about 2 minutes.",
        "Drain and salt at once.",
        "Pile onto bread for a Nordic fish sandwich."
    ],
    "Cooked Scorpion Fish": [
        "Cut thick fillets and season; handle the spines with care.",
        "Sear in a hot pan until well coloured on both sides.",
        "Baste with butter, garlic, and thyme.",
        "Finish in a hot oven for 3 minutes if needed."
    ],
    "Cooked Spadefish": [
        "Season the fillets and let them sit 10 minutes.",
        "Cook in a very hot skillet with a thin film of oil.",
        "Turn once and cook until just firm, not flaking apart.",
        "Dress simply with lemon and good salt."
    ],
    "Cooked Tripod Spiderfish": [
        "Season the meaty fillets and score the thicker parts.",
        "Roast at 425°F / 220°C with sliced potato and herbs.",
        "Baste once with garlic butter halfway through.",
        "Serve straight from the roasting tray."
    ],
    "Cooked Vampire Fish": [
        "Marinate the dark flesh in citrus and garlic 30 minutes.",
        "Sear hard, then lower the heat to cook through.",
        "Deglaze the pan with a little wine or stock.",
        "Spoon the pan sauce over and garnish with parsley."
    ],
    "Crab Stew": [
        "Sweat garlic, potato, and leek in butter until starting to soften.",
        "Add stock and simmer until the potato is nearly tender.",
        "Fold in picked crab meat and a splash of milk.",
        "Warm through gently and season; do not boil the crab."
    ],
    "Creamy Crab Bisque": [
        "Cook flour in melted butter into a pale roux.",
        "Whisk in stock and a little cream, then simmer until smooth.",
        "Add picked crab meat and warm through.",
        "Blend half for body, then season and finish with butter."
    ],
    "Elsweyr Fondue": [
        "Warm ale gently in a heavy pot — never let it boil.",
        "Add the cheese by handfuls, stirring until each melts before the next.",
        "Sweeten with a spoon of brown sugar or honey to round the sharpness.",
        "Serve hot with bread, apples, and roasted vegetables for dipping."
    ],
    "Grilled Chicken Breast": [
        "Butterfly the breast and pound to even thickness.",
        "Marinate in oil, garlic, and herbs for 30 minutes.",
        "Grill over medium-high heat, turning once, until just cooked.",
        "Rest 5 minutes so it stays juicy, then slice."
    ],
    "Horker and Ash Yam Stew": [
        "Brown the meat, then soften garlic and diced ash yam.",
        "Add stock and simmer until the yam is tender.",
        "Return the meat and simmer until it shreds at a touch.",
        "Season boldly with salt and warm spice."
    ],
    "Horker Loaf": [
        "Chop the cooked meat finely and mix with salt, butter, and a little stock.",
        "Press into a small loaf tin or shape by hand.",
        "Bake at 375°F / 190°C until browned and set, about 30 minutes.",
        "Rest 10 minutes so it slices cleanly."
    ],
    "Horker Stew": [
        "Sear the horker in its own fat until well browned.",
        "Add garlic, tomato, and lavender; cook until fragrant.",
        "Cover with stock and simmer slowly until the meat is spoon-tender.",
        "Skim the fat, season, and serve with bread."
    ],
    "Horse Haunch": [
        "Salt the haunch generously and let it come to room temperature.",
        "Roast at 400°F / 200°C, searing the surface first in a pan.",
        "Baste with butter and herbs, cooking to your preferred doneness.",
        "Rest 10 minutes, then carve against the grain."
    ],
    "Ironwood Soup": [
        "Simmer the firm fruit in stock until it softens and sweetens.",
        "Add charred aromatics and simmer 15 minutes more.",
        "Season with salt and a hint of smoke or char.",
        "Serve hot as a warming, mildly medicinal bowl."
    ],
    "Leg of Goat Roast": [
        "Rub the leg with oil, salt, garlic, and rosemary.",
        "Sear on all sides in a heavy pan.",
        "Roast at 350°F / 175°C, basting occasionally, until tender.",
        "Rest before carving and spoon the pan juices over."
    ],
    "Mammoth Steak": [
        "Salt the thick steak well and let it sit 30 minutes.",
        "Sear in a very hot pan to build a dark crust.",
        "Lower the heat and baste with butter until cooked to taste.",
        "Rest thoroughly, then slice against the grain."
    ],
    "Pheasant Roast": [
        "Truss the bird and season inside and out with salt and thyme.",
        "Roast at 400°F / 200°C, basting with butter, until the juices run clear.",
        "Rest under foil 10 minutes.",
        "Carve and serve with the buttery pan juices."
    ],
    "Potato Crab Chowder": [
        "Cook onion in butter, then add diced potato and stock.",
        "Simmer until the potato is tender, then mash a few for body.",
        "Stir in milk, butter, and picked crab meat.",
        "Warm gently and season; finish with black pepper."
    ],
    "Potato Soup": [
        "Soften onion in butter, then add potato and stock.",
        "Simmer until the potato collapses, about 20 minutes.",
        "Mash roughly for a rustic texture, or blend smooth.",
        "Season, then finish with butter or a swirl of cream."
    ],
    "Rabbit Haunch": [
        "Marinate the rabbit in oil, garlic, and herbs for a few hours.",
        "Sear in a hot pan, then lower the heat to cook through gently.",
        "Baste with butter and add a splash of stock to keep it moist.",
        "Rest briefly and serve with the pan sauce."
    ],
    "Roasted Tomato Crab Bisque": [
        "Roast the tomatoes with oil and salt until sweet and blistered.",
        "Cook butter and flour into a roux, then whisk in the roasted tomatoes.",
        "Add stock and simmer until thickened, then blend smooth.",
        "Fold in picked crab meat and season; serve with buttered bread."
    ],
    "Salmon Steak": [
        "Season the steak and let it sit 10 minutes.",
        "Sear skin-side down in hot oil until the skin crisps.",
        "Turn and cook to just under your preferred doneness.",
        "Rest briefly and finish with lemon and butter."
    ],
    "Steamed Mudcrab Legs": [
        "Steam the legs over salted water with a bay leaf, 8 minutes.",
        "Melt butter with garlic and a squeeze of lemon.",
        "Crack the legs and toss in the butter.",
        "Serve hot with extra butter for dipping."
    ],
    "Tomato Soup": [
        "Soften garlic and leek in butter without colouring.",
        "Add chopped tomato and stock; simmer 20 minutes.",
        "Blend smooth and season, adding a pinch of sugar if sharp.",
        "Finish with a swirl of cream or a knob of butter."
    ],
    "Vegetable Soup": [
        "Sweat cabbage, leek, and potato in butter until glossy.",
        "Add tomato and enough stock to cover; simmer until tender.",
        "Season well and let it bubble a little longer for depth.",
        "Serve chunky and hot with crusty bread."
    ],
    "Venison Chop": [
        "Bring the chop to room temperature and season boldly.",
        "Sear in a hot pan, basting with butter and thyme.",
        "Cook to medium-rare, then rest on a warm plate.",
        "Slice and spoon over the rested pan juices."
    ],
    "Venison Stew": [
        "Brown the venison hard, then set aside.",
        "Sweat leek and potato, then deglaze with a little ale.",
        "Return the meat with stock and simmer until tender.",
        "Season deeply and serve with a hunk of bread."
    ],
}

SKYRIM_NOTES = {
    "Apple Cabbage Stew": "Nordic home cooking at its plainest — sweet, sour, and deeply warming.",
    "Beef Stew": "The longer it simmers, the better it is the next morning.",
    "Cabbage Potato Soup": "Cheap, filling, and better than its ingredients suggest.",
    "Clam Chowder": "A coastal tavern bowl; the clam liquor is the whole point.",
    "Cooked Angelfish": "Best when the skin is crisp enough to crackle.",
    "Cooked Angler": "A firm fish that takes to butter and thyme.",
    "Cooked Angler Larvae": "Think of them as tiny crisp fish snacks and they make sense.",
    "Cooked Arctic Char": "Cold-water char is close to salmon; treat it the same way.",
    "Cooked Arctic Grayling": "Delicate and quick — pull it the moment it flakes.",
    "Cooked Beef": "The crust is the reward; never rush the rest.",
    "Cooked Boar Meat": "Ale and juniper turn strong meat into something you crave.",
    "Cooked Brook Bass": "A whole fish, a hot pan, and nothing else needed.",
    "Cooked Carp": "Fry it hard and serve it with something sharp.",
    "Cooked Catfish": "Milk first, cornmeal second — that's the secret.",
    "Cooked Cod": "Flakes apart into big sweet petals; keep it simple.",
    "Cooked Direfish": "A meaty fish that stands up to garlic butter.",
    "Cooked Glass Catfish": "Steam it gently so its delicate flesh holds together.",
    "Cooked Glassfish": "Eat it whole while it's crackling hot.",
    "Cooked Goldfish": "A sweet-sour glaze rescues the humblest fish.",
    "Cooked Juvenile Mudcrab": "Small enough to eat by the handful.",
    "Cooked Lyretail Anthias": "Crisp skin, moist flesh, charred citrus.",
    "Cooked Nix-Hound Meat": "Spiced and seared like a good sausage.",
    "Cooked Pearlfish": "Capers and butter make it feel far fancier than it is.",
    "Cooked Pogfish": "Grilled close to the fire until the skin blisters.",
    "Cooked Pygmy Sunfish": "Crisp little fish piled onto rye bread.",
    "Cooked Scorpion Fish": "Handle the spines with care; the flesh is excellent.",
    "Cooked Spadefish": "Keep it simple: good salt, hot pan, lemon.",
    "Cooked Tripod Spiderfish": "Roasts beautifully with potato and herbs.",
    "Cooked Vampire Fish": "Marinate it — the citrus wakes up the dark flesh.",
    "Crab Stew": "Sweet crab in a creamy, potato-thick broth.",
    "Creamy Crab Bisque": "A roux, good crab, and restraint.",
    "Elsweyr Fondue": "A pot of cheese and ale for sharing on a long winter night.",
    "Grilled Chicken Breast": "Rest it or lose the juice; that's the whole lesson.",
    "Horker and Ash Yam Stew": "Sweet yam against rich meat — a proper northern bowl.",
    "Horker Loaf": "Cold-sliced the next day, it makes a fine hunting lunch.",
    "Horker Stew": "Spoon-tender meat and a broth the colour of dusk.",
    "Horse Haunch": "A feast cut; carve it thin and pile it high.",
    "Ironwood Soup": "A strange, almost medicinal soup that grows on you.",
    "Leg of Goat Roast": "Rosemary and garlic against the strong, sweet meat.",
    "Mammoth Steak": "A huge cut that rewards patience and a very hot pan.",
    "Pheasant Roast": "A game bird for a small feast; the pan juices are gold.",
    "Potato Crab Chowder": "Comfort in a bowl, with crab for the lucky.",
    "Potato Soup": "The plainest, best thing to eat after a long day.",
    "Rabbit Haunch": "Lean, so keep it moist with butter and a quick hand.",
    "Roasted Tomato Crab Bisque": "Roasting the tomatoes is what makes this sing.",
    "Salmon Steak": "Make sure the skin crisps before you turn it.",
    "Steamed Mudcrab Legs": "The most direct route from crab to butter to you.",
    "Tomato Soup": "A tavern staple; a pinch of sugar balances the acid.",
    "Vegetable Soup": "Whatever the garden gave you, simmered into a bowl.",
    "Venison Chop": "Serve it pink; overcooking venison is a small tragedy.",
    "Venison Stew": "The stew that tastes like coming in from the snow.",
}

# Serving notes for the Zelda chapters (curated for the hero dishes; others get
# a short, recipe-specific line generated by the builder if none is given).
ZELDA_NOTES = {
    "Apple Pie": "Worth the wait — eat it warm with cold cream.",
    "Clam Chowder": "Pepper it hard, the way a harbour cook would.",
    "Crab Risotto": "Stir it patiently; risotto waits for no hero.",
    "Monster Cake": "Glaze it until it drips dramatically down the sides.",
    "Carrot Cake": "Add cream cheese frosting for the stable-inn version.",
    "Curry Rice": "The leftovers are arguably better the next day.",
    "Fried Wild Greens": "Fast, sharp, and better than a vitamin pill.",
    "Fruit Pie": "Whatever fruit is in season — it never disappoints.",
    "Nutcake": "Brown the butter first; it's what makes it taste expensive.",
    "Pumpkin Pie": "Test with a slight wobble in the middle — that's perfect.",
    "Salmon Meunière": "Spoon the foaming butter over until it smells like a celebration.",
    "Seafood Paella": "Let the bottom crisp into socarrat — that's the prize.",
    "Wheat Bread": "Better with a long, slow rise and a very hot oven.",
    "Chilly Elixir": "Drink it before crossing any desert, real or emotional.",
    "Energizing Honey Candy": "Dust well or you'll be prying it off the tray.",
    "Noble Pursuit": "A salted rim makes it feel like a proper drink.",
    "Steamed Tomatoes": "A five-minute bowl that tastes like summer.",
    "Cheesecake": "Chill it overnight for the cleanest slice.",
}
