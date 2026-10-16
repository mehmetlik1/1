#!/usr/bin/env python3
"""
Generates every JSON/PNG resource for Material Generators.
Run from the project root:   python3 tools/gen_resources.py
(needs Pillow:  pip install pillow)

To add a material: add a row to GENERATORS below AND to GeneratorDef.java.
"""
import json, os, random
from PIL import Image

MOD = "material_generators"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main")
ASSETS = os.path.join(ROOT, "resources", "assets", MOD)
DATA = os.path.join(ROOT, "resources", "data", MOD)

# id, display name, color, recipe corner item, recipe edge item, required mod (or None)
GENERATORS = [
    ("zinc",         "Zinc",         (150, 172, 160), "create:zinc_ingot",        "create:andesite_alloy", "create"),
    ("quartz",       "Quartz",       (235, 229, 220), "minecraft:quartz",         "minecraft:quartz_block", None),
    ("oak_log",      "Oak Log",      (162, 130, 78),  "minecraft:oak_sapling",    "minecraft:oak_log", None),
    ("spruce_log",   "Spruce Log",   (104, 78, 47),   "minecraft:spruce_sapling", "minecraft:spruce_log", None),
    ("birch_log",    "Birch Log",    (216, 205, 152), "minecraft:birch_sapling",  "minecraft:birch_log", None),
    ("jungle_log",   "Jungle Log",   (149, 108, 76),  "minecraft:jungle_sapling", "minecraft:jungle_log", None),
    ("acacia_log",   "Acacia Log",   (168, 90, 50),   "minecraft:acacia_sapling", "minecraft:acacia_log", None),
    ("dark_oak_log", "Dark Oak Log", (66, 43, 20),    "minecraft:dark_oak_sapling", "minecraft:dark_oak_log", None),
    ("mangrove_log", "Mangrove Log", (117, 54, 48),   "minecraft:mangrove_propagule", "minecraft:mangrove_log", None),
    ("cherry_log",   "Cherry Log",   (226, 177, 176), "minecraft:cherry_sapling", "minecraft:cherry_log", None),
    ("crimson_stem", "Crimson Stem", (130, 45, 80),   "minecraft:crimson_fungus", "minecraft:crimson_stem", None),
    ("warped_stem",  "Warped Stem",  (43, 120, 118),  "minecraft:warped_fungus",  "minecraft:warped_stem", None),
]

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(content, str):
            f.write(content)
        else:
            json.dump(content, f, indent=2)
            f.write("\n")

def clamp(v): return max(0, min(255, int(v)))
def shade(c, d): return tuple(clamp(x + d) for x in c)

def make_texture(path, color, tier, seed):
    rnd = random.Random(seed)
    frame = (74, 76, 84) if tier == 1 else (196, 158, 48)
    rivet = (150, 152, 160) if tier == 1 else (255, 226, 120)
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for y in range(16):
        for x in range(16):
            n = rnd.randint(-6, 6)
            edge = x in (0, 15) or y in (0, 15)
            if edge:
                px[x, y] = shade(frame, -22 + n) + (255,)
            elif 3 <= x <= 12 and 3 <= y <= 12:
                inner = 4 <= x <= 11 and 4 <= y <= 11
                base = color if inner else shade(color, -55)
                hl = 18 if (inner and (x == 4 or y == 4)) else (-18 if (inner and (x == 11 or y == 11)) else 0)
                px[x, y] = shade(base, hl + n) + (255,)
            else:
                px[x, y] = shade(frame, n) + (255,)
    for (x, y) in [(1, 1), (14, 1), (1, 14), (14, 14)]:
        px[x, y] = rivet + (255,)
    img.save(path)

def cube_model(texture):
    return {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MOD}:block/{texture}"}}

def loot(name):
    return {
        "type": "minecraft:block",
        "pools": [{
            "rolls": 1.0, "bonus_rolls": 0.0,
            "entries": [{"type": "minecraft:item", "name": f"{MOD}:{name}"}],
            "conditions": [{"condition": "minecraft:survives_explosion"}],
        }],
    }

def register_block(name, display, texture, lang, blocks):
    write(f"{ASSETS}/blockstates/{name}.json", {"variants": {"": {"model": f"{MOD}:block/{name}"}}})
    write(f"{ASSETS}/models/block/{name}.json", cube_model(texture))
    write(f"{ASSETS}/models/item/{name}.json", {"parent": f"{MOD}:block/{name}"})
    write(f"{DATA}/loot_tables/blocks/{name}.json", loot(name))
    lang[f"block.{MOD}.{name}"] = display
    blocks.append(f"{MOD}:{name}")

def main():
    lang = {f"itemGroup.{MOD}": "Material Generators"}
    blocks = []

    # --- generator core ---
    core_tex = os.path.join(ASSETS, "textures", "block", "generator_core.png")
    os.makedirs(os.path.dirname(core_tex), exist_ok=True)
    make_texture(core_tex, (190, 60, 50), 1, 999)
    register_block("generator_core", "Generator Core", "generator_core", lang, blocks)
    write(f"{DATA}/recipes/generator_core.json", {
        "type": "minecraft:crafting_shaped", "category": "misc",
        "pattern": ["aaa", "aba", "aaa"],
        "key": {"a": {"item": "minecraft:iron_ingot"}, "b": {"item": "minecraft:redstone"}},
        "result": {"item": f"{MOD}:generator_core", "count": 1},
    })

    # --- generators ---
    for i, (gid, disp, color, corner, edge, req) in enumerate(GENERATORS):
        t1, t2 = f"{gid}_generator", f"{gid}_generator_tier_ii"
        make_texture(os.path.join(ASSETS, "textures", "block", f"{t1}.png"), color, 1, i * 2 + 1)
        make_texture(os.path.join(ASSETS, "textures", "block", f"{t2}.png"), color, 2, i * 2 + 2)
        register_block(t1, f"{disp} Generator", t1, lang, blocks)
        register_block(t2, f"{disp} Generator Tier II", t2, lang, blocks)

        cond = {"conditions": [{"type": "forge:mod_loaded", "modid": req}]} if req else {}
        recipe1 = dict(cond)
        recipe1.update({
            "type": "minecraft:crafting_shaped", "category": "misc",
            "pattern": ["aba", "bcb", "aba"],
            "key": {"a": {"item": corner}, "b": {"item": edge}, "c": {"item": f"{MOD}:generator_core"}},
            "result": {"item": f"{MOD}:{t1}", "count": 1},
        })
        write(f"{DATA}/recipes/{t1}.json", recipe1)

        recipe2 = dict(cond)
        recipe2.update({
            "type": "minecraft:crafting_shaped", "category": "misc",
            "pattern": ["aba", "bcb", "aba"],
            "key": {"a": {"item": "minecraft:gold_block"}, "b": {"item": "minecraft:iron_block"},
                    "c": {"item": f"{MOD}:{t1}"}},
            "result": {"item": f"{MOD}:{t2}", "count": 1},
        })
        write(f"{DATA}/recipes/{t2}.json", recipe2)

    write(os.path.join(ROOT, "resources", "assets", MOD, "lang", "en_us.json"), lang)
    write(os.path.join(ROOT, "resources", "data", "minecraft", "tags", "blocks", "mineable", "pickaxe.json"),
          {"replace": False, "values": blocks})
    print(f"Generated {len(blocks)} blocks.")

if __name__ == "__main__":
    main()
