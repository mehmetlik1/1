package com.example.materialgenerators;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class ModRegistry {
    public static final DeferredRegister<Block> BLOCKS =
            DeferredRegister.create(ForgeRegistries.BLOCKS, MaterialGenerators.MOD_ID);
    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, MaterialGenerators.MOD_ID);
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES =
            DeferredRegister.create(ForgeRegistries.BLOCK_ENTITY_TYPES, MaterialGenerators.MOD_ID);
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MaterialGenerators.MOD_ID);

    /** Crafting ingredient for every generator. */
    public static final RegistryObject<Block> GENERATOR_CORE = BLOCKS.register("generator_core",
            () -> new Block(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.METAL).strength(3.5F, 6.0F).sound(SoundType.METAL)));
    public static final RegistryObject<Item> GENERATOR_CORE_ITEM = ITEMS.register("generator_core",
            () -> new BlockItem(GENERATOR_CORE.get(), new Item.Properties()));

    public static final List<RegistryObject<Block>> GENERATOR_BLOCKS = new ArrayList<>();

    static {
        for (GeneratorDef def : GeneratorDef.ALL) {
            for (int tier = 1; tier <= 2; tier++) {
                final int t = tier;
                String name = def.blockName(tier);
                RegistryObject<Block> block = BLOCKS.register(name, () -> new GeneratorBlock(def, t));
                ITEMS.register(name, () -> new BlockItem(block.get(), new Item.Properties()));
                GENERATOR_BLOCKS.add(block);
            }
        }
    }

    public static final RegistryObject<BlockEntityType<GeneratorBlockEntity>> GENERATOR_BE =
            BLOCK_ENTITIES.register("generator", () -> BlockEntityType.Builder
                    .of(GeneratorBlockEntity::new,
                            GENERATOR_BLOCKS.stream().map(RegistryObject::get).toArray(Block[]::new))
                    .build(null));

    public static final RegistryObject<CreativeModeTab> TAB = TABS.register("main",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup." + MaterialGenerators.MOD_ID))
                    .icon(() -> new ItemStack(GENERATOR_CORE_ITEM.get()))
                    .displayItems((params, output) ->
                            ITEMS.getEntries().forEach(item -> output.accept(item.get())))
                    .build());

    private ModRegistry() {}
}
