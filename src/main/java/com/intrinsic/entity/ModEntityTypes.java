package com.intrinsic.entity;

import com.intrinsic.Intrinsic;
import com.intrinsic.entity.custom.HerbivoreEntity;
import net.minecraft.entity.EntityClassification;
import net.minecraft.entity.EntityType;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

public class ModEntityTypes {
    public static DeferredRegister<EntityType<?>> ENTITY_TYPES
            = DeferredRegister.create(ForgeRegistries.ENTITIES, Intrinsic.MOD_ID);

    public static final RegistryObject<EntityType<HerbivoreEntity>> HERBIVORE =
            ENTITY_TYPES.register("herbivore",
                    () -> EntityType.Builder.of(HerbivoreEntity::new, EntityClassification.CREATURE).sized(1f, 3f)
                            .build(new ResourceLocation(Intrinsic.MOD_ID, "herbivore").toString()));

    public static void register(IEventBus eventBus) {
        ENTITY_TYPES.register(eventBus);
    }
}