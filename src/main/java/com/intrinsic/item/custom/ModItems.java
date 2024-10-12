package com.intrinsic.item.custom;

import com.intrinsic.Intrinsic;
import net.minecraft.item.*;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import com.intrinsic.entity.ModEntityTypes;

public class ModItems {

    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, Intrinsic.MOD_ID);

    // Register the spawn egg with the correct name
    public static final RegistryObject<ModSpawnEggItem> HERBIVORE_SPAWN_EGG =
            ITEMS.register("herbivore_spawn_egg",
                    () -> new ModSpawnEggItem(ModEntityTypes.HERBIVORE,
                            0xFFFFFF, 0x000000,
                            new Item.Properties().tab(ItemGroup.TAB_MISC)));


    public static void register(IEventBus eventBus) {
        ITEMS.register(eventBus);
    }
}
