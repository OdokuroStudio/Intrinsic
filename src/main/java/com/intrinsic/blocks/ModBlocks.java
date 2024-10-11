package com.intrinsic.blocks;

import com.intrinsic.flora.CustomFlora;
import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraftforge.event.RegistryEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.DeferredRegister;

public class ModBlocks {
    // Deferred Register for blocks and items
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, "intrinsic");
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, "intrinsic");

    // Block registration
    public static final Block CUSTOM_FLORA = registerBlock("custom_flora", new CustomFlora());

    private static Block registerBlock(String name, Block block) {
        BLOCKS.register(name, () -> block);
        ITEMS.register(name, () -> new BlockItem(block, new Item.Properties()));
        return block;
    }

    @SubscribeEvent
    public static void onRegisterItems(RegistryEvent.Register<Item> event) {
        event.getRegistry().registerAll(
                new BlockItem(CUSTOM_FLORA, new Item.Properties()).setRegistryName("intrinsic", "custom_flora")
        );
    }


    // Register blocks during the registry event
    @SubscribeEvent
    public static void onRegisterBlocks(RegistryEvent.Register<Block> event) {
        event.getRegistry().registerAll(
                CUSTOM_FLORA.setRegistryName("intrinsic", "custom_flora")
        );
    }
}
