package com.example.materialgenerators;

import java.util.HashMap;
import java.util.Map;

import net.minecraftforge.common.ForgeConfigSpec;

/** Ticks between produced items. Edit config/material_generators.toml (20 ticks = 1 second). */
public final class GeneratorConfig {
    public static final ForgeConfigSpec SPEC;
    private static final Map<String, ForgeConfigSpec.IntValue> SPEEDS = new HashMap<>();

    static {
        ForgeConfigSpec.Builder b = new ForgeConfigSpec.Builder();
        b.comment("Ticks between each produced item (20 ticks = 1 second).").push("speeds");
        for (GeneratorDef d : GeneratorDef.ALL) {
            SPEEDS.put(d.id() + ":1", b.defineInRange(d.id() + "_speed", 20, 1, 1_000_000));
            SPEEDS.put(d.id() + ":2", b.defineInRange(d.id() + "_tier2_speed", 10, 1, 1_000_000));
        }
        b.pop();
        SPEC = b.build();
    }

    private GeneratorConfig() {}

    public static int interval(GeneratorDef def, int tier) {
        try {
            return SPEEDS.get(def.id() + ":" + tier).get();
        } catch (IllegalStateException notLoadedYet) {
            return tier == 1 ? 20 : 10;
        }
    }
}
