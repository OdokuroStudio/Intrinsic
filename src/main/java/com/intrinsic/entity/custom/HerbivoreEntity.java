package com.intrinsic.entity.custom;

import com.intrinsic.flora.CustomFlora;
import net.minecraft.block.BlockState;
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

@SuppressWarnings("ALL")
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
        private BlockPos targetFloraPos;

        public EatCustomFloraGoal(HerbivoreEntity entity) {
            this.entity = entity;
        }

        @Override
        public boolean canUse() {
            // Random chance to eat and check for nearby custom flora
            if (entity.getRandom().nextInt(2) == 0) {
                // Look for custom flora within a certain radius
                for (int x = -5; x <= 5; x++) {
                    for (int z = -5; z <= 5; z++) {
                        BlockPos pos = entity.blockPosition().offset(x, 0, z);
                        if (entity.level.getBlockState(pos).getBlock() instanceof CustomFlora) {
                            targetFloraPos = pos; // Set target flora position
                            return true; // Found custom flora to eat
                        }
                    }
                }
            }
            return false; // No custom flora found
        }

        @Override
        public void start() {
            if (targetFloraPos != null) {
                entity.getNavigation().moveTo(targetFloraPos.getX(), targetFloraPos.getY(), targetFloraPos.getZ(), 1.0D);
            }
        }

        @Override
        public void tick() {
            // Continuously move towards the custom flora
            if (targetFloraPos != null) {
                double distance = entity.distanceToSqr(targetFloraPos.getX(), targetFloraPos.getY(), targetFloraPos.getZ());
                if (distance > 3) {
                    // Keep navigating towards the target
                    entity.getNavigation().moveTo(targetFloraPos.getX(), targetFloraPos.getY(), targetFloraPos.getZ(), 1.0D);
                } else {
                    // Close enough to eat
                    eatCustomFlora();
                    entity.getNavigation().stop(); // Stop navigation after eating
                }
            }
        }

        private void eatCustomFlora() {
            // Check if the block is the custom flora
            if (entity.level.getBlockState(targetFloraPos).getBlock() instanceof CustomFlora) {
                entity.level.destroyBlock(targetFloraPos, true); // Remove the custom flora block
                // Optional: play a sound or restore health
            } else {
                System.out.println("Target is not custom flora!");
            }
        }

        @Override
        public boolean canContinueToUse() {
            return targetFloraPos != null && entity.level.getBlockState(targetFloraPos).getBlock() instanceof CustomFlora;
        }
    }
}
