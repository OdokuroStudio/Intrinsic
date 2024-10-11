package com.intrinsic.entity;

import com.intrinsic.Intrinsic;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.ai.goal.DefendVillageTargetGoal;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

public class ModEntityTypes {
    public static DeferredRegister<EntityType<?>> ENTITY_TYPES = DeferredRegister.create(ForgeRegistries.ENTITIES, Intrinsic.MOD_ID);


    public static void register(IEventBus eventBus) {
        ENTITY_TYPES.register(eventBus);
    }
}
