package com.intrinsic; // Update this to your package

import com.intrinsic.blocks.ModBlocks;
import com.intrinsic.entity.ModEntityTypes;
import com.intrinsic.entity.custom.HerbivoreEntity;
import com.intrinsic.entity.render.HerbivoreEntityRenderer;
import com.intrinsic.item.custom.ModSpawnEggItem;
import com.intrinsic.item.custom.ModItems;
import net.minecraft.block.Blocks;
import net.minecraft.entity.EntityClassification;
import net.minecraft.entity.EntityType;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.RegistryEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.InterModComms;
import net.minecraftforge.fml.client.registry.RenderingRegistry;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.event.lifecycle.InterModEnqueueEvent;
import net.minecraftforge.fml.event.lifecycle.InterModProcessEvent;
import net.minecraftforge.fml.event.server.FMLServerStartingEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.RenderTypeLookup;


import java.util.stream.Collectors;

// Change the mod ID here
@Mod("intrinsic")
public class Intrinsic
{
    public static final String MOD_ID = "intrinsic";
    // Directly reference a log4j logger.
    private static final Logger LOGGER = LogManager.getLogger();

    public Intrinsic() {
        IEventBus eventbus = FMLJavaModLoadingContext.get().getModEventBus();

        // Register the setup methods for modloading
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::setup);
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::doClientStuff);

        // Register ModBlocks for block and item registration
        ModBlocks.BLOCKS.register(FMLJavaModLoadingContext.get().getModEventBus());
        ModBlocks.ITEMS.register(FMLJavaModLoadingContext.get().getModEventBus());


        // Register ourselves for server and other game events we are interested in
        MinecraftForge.EVENT_BUS.register(this);

        IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();
        ModEntityTypes.ENTITY_TYPES.register(modEventBus);
        ModItems.ITEMS.register(modEventBus);

    }

    private void setup(final FMLCommonSetupEvent event) {
        // Some pre-initialization code
        LOGGER.info("HELLO FROM PREINIT");
        LOGGER.info("DIRT BLOCK >> {}", Blocks.DIRT.getRegistryName());

    }

    private void doClientStuff(final FMLClientSetupEvent event) {
        // Register custom_flora block with the CUTOUT render type for transparency
        RenderTypeLookup.setRenderLayer(ModBlocks.CUSTOM_FLORA, RenderType.cutout());

        RenderingRegistry.registerEntityRenderingHandler(ModEntityTypes.HERBIVORE.get(), HerbivoreEntityRenderer::new);
    }

    private void enqueueIMC(final InterModEnqueueEvent event)
    {
        // Example code to dispatch IMC to another mod
        InterModComms.sendTo("intrinsic", "helloworld", () -> {
            LOGGER.info("Hello world from the MDK");
            return "Hello world";
        });
    }

    private void processIMC(final InterModProcessEvent event)
    {
        // Example code to receive and process InterModComms from other mods
        LOGGER.info("Got IMC {}", event.getIMCStream().
                map(m -> m.getMessageSupplier().get()).
                collect(Collectors.toList()));
    }

    @SubscribeEvent
    public void onServerStarting(FMLServerStartingEvent event) {
        // Do something when the server starts
        LOGGER.info("HELLO from server starting");
    }

    @SubscribeEvent
    public static void onCommonSetup(FMLCommonSetupEvent event) {
        event.enqueueWork(() -> {
            ModSpawnEggItem.initSpawnEggs();

        });

    }

    @SubscribeEvent
    public static void registerEntityTypes(RegistryEvent.Register<EntityType<?>> event) {
        event.getRegistry().registerAll(
                EntityType.Builder.of(HerbivoreEntity::new, EntityClassification.CREATURE)
                        .sized(0.6F, 0.8F) // Adjust size as necessary
                        .build("intrinsic:herbivore") // Use the full registry name directly here
        );
    }
}

