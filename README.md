# Material Generators (Forge 1.20.1)

A "Tiered Generators"-style mod. Place a generator and it slowly fills its own inventory with one material.

| Generator | Produces | Tier I recipe (corners / edges / centre) |
|---|---|---|
| Zinc | `create:zinc_ingot` | Zinc Ingot / Andesite Alloy / Generator Core *(needs Create)* |
| Quartz | Nether Quartz | Quartz / Quartz Block / Generator Core |
| Oak, Spruce, Birch, Jungle, Acacia, Dark Oak, Mangrove, Cherry Log; Crimson, Warped Stem | that log | matching Sapling (Propagule / Fungus) / matching Log / Generator Core |

* **Generator Core:** 8 iron ingots around 1 redstone.
* **Tier II:** 4 gold blocks (corners) + 4 iron blocks (edges) around the Tier I generator. Twice as fast.
* **Speeds:** Tier I = 1 item / 20 ticks, Tier II = 1 item / 10 ticks. Change them in `config/material_generators.toml`.
* **Use:** right-click to open the 27-slot inventory. Hoppers, pipes and funnels can pull items out (but can't insert).
  When the inventory is full the generator pauses.
* **Create is optional.** Without it, zinc generators exist but do nothing and their recipes are disabled.

## Build (easiest: no installs, GitHub does it)
1. Create a free GitHub account and a new empty repository.
2. Upload the *contents* of this folder (about 15 files; make sure the `.github` folder is included) and commit.
3. Open the **Actions** tab -> "Build mod jar" -> wait ~3-5 minutes -> download the `material_generators-jar` artifact.
4. Unzip it and put `material_generators-1.0.0.jar` in your `mods/` folder (Forge 1.20.1, 47.x).
   If you want zinc, install Create 0.5.1 as well.

## Build locally instead
0. Generate the resources first: `pip install pillow` then `python3 tools/gen_resources.py` (GitHub does this step automatically).
Requires JDK 17.

1. Get a Gradle wrapper: copy `gradlew`, `gradlew.bat` and the `gradle/` folder from the official Forge 1.20.1 MDK
   (https://files.minecraftforge.net/ -> 1.20.1 -> "Mdk"), or run `gradle wrapper --gradle-version 8.1.1` if you have Gradle installed.
2. `./gradlew build`
3. The mod jar is in `build/libs/material_generators-1.0.0.jar`. Drop it in `mods/`.

For testing: `./gradlew runClient`. You can also import the folder into IntelliJ / Eclipse as a Gradle project.

## Changing things
* Add / remove a material: edit `GeneratorDef.java` **and** the `GENERATORS` list in `tools/gen_resources.py`,
  then run `python3 tools/gen_resources.py` (regenerates models, textures, recipes, loot tables, language file).
* Textures are simple generated placeholders; replace any PNG in `src/main/resources/assets/material_generators/textures/block/`.
