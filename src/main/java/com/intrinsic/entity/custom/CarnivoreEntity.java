package com.intrinsic.entity.custom;

import net.minecraft.block.BlockState;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.ai.attributes.AttributeModifierMap;
import net.minecraft.entity.ai.attributes.Attributes;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.passive.SheepEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.passive.WolfEntity;
import net.minecraft.util.DamageSource;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@SuppressWarnings("ALL")
public class CarnivoreEntity extends WolfEntity {

    public CarnivoreEntity(EntityType<? extends WolfEntity> type, World worldIn) {
        super(type, worldIn);
    }

    public static AttributeModifierMap.MutableAttribute setCustomAttributes() {
        // Create an attribute map for the CarnivoreEntity
        return WolfEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 10.0D) // Set higher health
                .add(Attributes.MOVEMENT_SPEED, 0.35D) // Set faster movement speed
                .add(Attributes.ATTACK_DAMAGE, 5.0D); // Set higher attack damage
    }

    @Override
    protected void registerGoals() {
        super.registerGoals();
        this.goalSelector.addGoal(0, new SwimGoal(this)); // Swimming behavior
        this.goalSelector.addGoal(1, new PanicGoal(this, 1.25D)); // Panic behavior
        this.goalSelector.addGoal(2, new WaterAvoidingRandomWalkingGoal(this, 1.0D)); // Wandering behavior
        this.goalSelector.addGoal(3, new LookAtGoal(this, PlayerEntity.class, 6.0F)); // Look at players
        this.goalSelector.addGoal(4, new HuntHerbivoreGoal(this)); // Custom hunting behavior
        this.goalSelector.addGoal(7, new LookRandomlyGoal(this)); // Random looking behavior
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.WOLF_AMBIENT; // Ambient sound for wolf
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.WOLF_DEATH; // Death sound for wolf
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource damageSourceIn) {
        return SoundEvents.WOLF_HURT; // Hurt sound for wolf
    }

    @Override
    protected void playStepSound(BlockPos pos, BlockState blockIn) {
        this.playSound(SoundEvents.WOLF_STEP, 0.15F, 1.0F); // Step sound for wolf
    }

    // Custom goal for hunting herbivores
    static class HuntHerbivoreGoal extends Goal {
        private final CarnivoreEntity carnivore;
        private SheepEntity targetHerbivore;

        public HuntHerbivoreGoal(CarnivoreEntity carnivore) {
            this.carnivore = carnivore;
        }

        private int searchCooldown = 0;

        @Override
        public boolean canUse() {
            if (searchCooldown > 0) {
                searchCooldown--;
                return false;
            }

            // Random chance to start searching for herbivores
            if (carnivore.getRandom().nextInt(5) == 0) {
                // Search for nearby herbivores (e.g., SheepEntity)
                List<SheepEntity> nearbyHerbivores = carnivore.level.getEntitiesOfClass(SheepEntity.class, carnivore.getBoundingBox().inflate(10.0D, 3.0D, 10.0D));
                if (!nearbyHerbivores.isEmpty()) {
                    targetHerbivore = nearbyHerbivores.get(0); // Target the first herbivore found
                    searchCooldown = 20; // Set cooldown for 1 second (20 ticks)
                    return true; // Found herbivore to hunt
                }
            }

            // If no herbivore is found, return false
            return false;
        }

        @Override
        public void start() {
            if (targetHerbivore != null) {
                carnivore.getNavigation().moveTo(targetHerbivore, 1.2D);
            }
        }

        @Override
        public void tick() {
            // Continuously move towards the herbivore
            if (targetHerbivore != null) {
                double distance = carnivore.distanceToSqr(targetHerbivore);
                if (distance > 2) {
                    carnivore.getNavigation().moveTo(targetHerbivore, 1.2D);
                } else {
                    // Attack the herbivore when close enough
                    carnivore.doHurtTarget(targetHerbivore);
                }
            }
        }

        @Override
        public boolean canContinueToUse() {
            return targetHerbivore != null && targetHerbivore.isAlive();
        }
    }
}
