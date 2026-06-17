# All ingredient names are lowercased for matching
HIDDEN_SUGARS = [
    "maltodextrin", "dextrose", "glucose syrup", "glucose", "corn syrup",
    "high fructose corn syrup", "fructose", "sucrose", "cane sugar",
    "brown sugar", "raw sugar", "invert sugar", "fruit juice concentrate",
    "fruit puree concentrate", "agave nectar", "honey", "maple syrup",
    "molasses", "barley malt", "rice syrup", "brown rice syrup",
    "caramel", "diastatic malt", "ethyl maltol", "treacle",
    "coconut sugar", "date syrup", "palm sugar", "lactose", "maltose",
    "galactose", "polydextrose", "sorbitol", "mannitol", "xylitol",
    "isomalt", "maltitol syrup"
]

# Maps each allergen category to its aliases that may appear on labels
ALLERGEN_MAP = {
    "peanut":    ["peanut", "arachis hypogaea", "groundnut", "peanut oil"],
    "tree_nut":  ["almond", "cashew", "walnut", "pistachio", "pecan",
                  "hazelnut", "macadamia", "brazil nut", "pine nut"],
    "gluten":    ["wheat", "triticum vulgare", "barley", "hordeum vulgare",
                  "rye", "secale", "spelt", "kamut", "triticale", "gluten"],
    "dairy":     ["milk", "casein", "caseinate", "whey", "lactose",
                  "ghee", "butter", "cream", "cheese", "yogurt", "curd",
                  "milk solids", "skimmed milk"],
    "soy":       ["soybean", "soya", "soy lecithin", "tofu", "edamame",
                  "miso", "tempeh", "soy protein"],
    "egg":       ["egg", "albumin", "globulin", "livetin", "lysozyme",
                  "ovalbumin", "ovomucin", "ovomucoid", "vitellin",
                  "egg white", "egg yolk"],
    "sesame":    ["sesame", "sesamum indicum", "tahini", "sesame oil"],
    "seafood":   ["shrimp", "prawn", "crab", "lobster", "fish sauce",
                  "bonito", "surimi", "anchovy", "tuna", "salmon"],
    "mustard":   ["mustard", "mustard seed", "mustard oil"],
    "sulphite":  ["sulphite", "sulfite", "sulphur dioxide", "sodium metabisulphite"]
}

# WHO daily limits (adults)
DAILY_LIMITS = {
    "sugar_g": 25,      # WHO added sugar limit (25g = 5% of 2000 kcal)
    "sodium_g": 2,      # WHO sodium limit (2g)
    "saturated_fat_g": 20,
    "calories": 2000,
}
