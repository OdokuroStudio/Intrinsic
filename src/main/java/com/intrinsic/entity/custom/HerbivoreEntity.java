package com.intrinsic.entity.custom;

import com.intrinsic.flora.CustomFlora;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.MobEntity;
import net.minecraft.entity.ai.attributes.AttributeModifierMap;
import net.minecraft.entity.ai.attributes.Attributes;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.passive.SheepEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.DamageSource;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;

public class HerbivoreEntity extends SheepEntity {

    public HerbivoreEntity(EntityType<? extends SheepEntity> type, World worldIn) {
        super(type, worldIn);
    }

    public static AttributeModifierMap.MutableAttribute setCustomAttributes() {
        // Create an attribute map for the HerbivoreEntity
        return MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 3.0D) // Set health
                .add(Attributes.MOVEMENT_SPEED, 0.25D); // Set movement speed
    }

    @Override
    protected void registerGoals() {
        super.registerGoals();
        this.goalSelector.addGoal(0, new SwimGoal(this)); // Swimming behavior
        this.goalSelector.addGoal(1, new PanicGoal(this, 1.25D)); // Panic behavior
        this.goalSelector.addGoal(2, new WaterAvoidingRandomWalkingGoal(this, 1.0D)); // Wandering behavior
        this.goalSelector.addGoal(3, new LookAtGoal(this, PlayerEntity.class, 6.0F)); // Look at players
        this.goalSelector.addGoal(4, new EatCustomFloraGoal(this)); // Custom eating behavior
        this.goalSelector.addGoal(7, new LookRandomlyGoal(this)); // Random looking behavior
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.SHEEP_AMBIENT; // Ambient sound for sheep
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.SHEEP_DEATH; // Death sound for sheep
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource damageSourceIn) {
        return SoundEvents.SHEEP_HURT; // Hurt sound for sheep
    }

    @Override
    protected void playStepSound(BlockPos pos, BlockState blockIn) {
        this.playSound(SoundEvents.SHEEP_STEP, 0.15F, 1.0F); // Step sound for sheep
    }

    // Custom goal for eating custom flora
    static class EatCustomFloraGoal extends Goal {
        private final HerbivoreEntity entity;

        public EatCustomFloraGoal(HerbivoreEntity entity) {
            this.entity = entity;
        }

        @Override
        public boolean canUse() {
            return entity.getRandom().nextInt(10) == 0; // Random chance to eat
        }

    }
}
