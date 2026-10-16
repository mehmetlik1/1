package com.example.materialgenerators;

import java.util.List;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraftforge.registries.ForgeRegistries;

/**
 * One kind of generator. "id" is used for block names, config keys and textures:
 *   block ids:   {id}_generator   and   {id}_generator_tier_ii
 *   config keys: {id}_speed       and   {id}_tier2_speed
 *
 * To add a new material, add a line to ALL and (re)run tools/gen_resources.py.
 */
public record GeneratorDef(String id, String displayName, ResourceLocation output) {

    private static GeneratorDef of(String id, String displayName, String namespace, String path) {
        return new GeneratorDef(id, displayName, new ResourceLocation(namespace, path));
    }

    public static final List<GeneratorDef> ALL = List.of(
            // Create (optional dependency, looked up by registry name at runtime)
            of("zinc", "Zinc", "create", "zinc_ingot"),
            // Vanilla
            of("quartz", "Quartz", "minecraft", "quartz"),
            of("oak_log", "Oak Log", "minecraft", "oak_log"),
            of("spruce_log", "Spruce Log", "minecraft", "spruce_log"),
            of("birch_log", "Birch Log", "minecraft", "birch_log"),
            of("jungle_log", "Jungle Log", "minecraft", "jungle_log"),
            of("acacia_log", "Acacia Log", "minecraft", "acacia_log"),
            of("dark_oak_log", "Dark Oak Log", "minecraft", "dark_oak_log"),
            of("mangrove_log", "Mangrove Log", "minecraft", "mangrove_log"),
            of("cherry_log", "Cherry Log", "minecraft", "cherry_log"),
            of("crimson_stem", "Crimson Stem", "minecraft", "crimson_stem"),
            of("warped_stem", "Warped Stem", "minecraft", "warped_stem")
    );

    /** Returns the item this generator makes, or AIR if its mod (Create) is not installed. */
    public Item resolveOutput() {
        Item item = ForgeRegistries.ITEMS.getValue(output);
        return item == null ? Items.AIR : item;
    }

    public String blockName(int tier) {
        return id + (tier == 1 ? "_generator" : "_generator_tier_ii");
    }
}
