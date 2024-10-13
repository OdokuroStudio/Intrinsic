package com.intrinsic.entity.custom;

import com.intrinsic.entity.ModEntityTypes;
import com.intrinsic.flora.CustomFlora;
import net.minecraft.block.BlockState;
import net.minecraft.entity.AgeableEntity;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.MobEntity;
import net.minecraft.entity.ai.attributes.AttributeModifierMap;
import net.minecraft.entity.ai.attributes.Attributes;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.passive.AnimalEntity;
import net.minecraft.entity.passive.SheepEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.DamageSource;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraft.world.server.ServerWorld;

import javax.annotation.Nullable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@SuppressWarnings("ALL")
public class HerbivoreEntity extends AnimalEntity {
    private int foodConsumed; // Track how much food has been consumed

    public HerbivoreEntity(EntityType<? extends AnimalEntity> type, World worldIn) {
        super(type, worldIn);
        this.foodConsumed = 0; // Initialize food consumed to 0
    }

    public static AttributeModifierMap.MutableAttribute setCustomAttributes() {
        return MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 3.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.25D);
    }

    @Override
    protected void registerGoals() {
        super.registerGoals();
        this.goalSelector.addGoal(0, new SwimGoal(this));
        this.goalSelector.addGoal(1, new PanicGoal(this, 1.25D));
        this.goalSelector.addGoal(2, new BreedGoal(this, 1.0D));
        this.goalSelector.addGoal(3, new EatCustomFloraGoal(this));
        this.goalSelector.addGoal(4, new WaterAvoidingRandomWalkingGoal(this, 1.0D));
        this.goalSelector.addGoal(5, new LookAtGoal(this, PlayerEntity.class, 6.0F));
        this.goalSelector.addGoal(6, new LookRandomlyGoal(this));
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.SHEEP_AMBIENT;
    }
    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
    }

    @Nullable
    @Override
    public AgeableEntity getBreedOffspring(ServerWorld serverWorld, AgeableEntity ageableEntity) {
        return ModEntityTypes.HERBIVORE.get().create(serverWorld); // Create and return a new instance of HerbivoreEntity
    }

    @Override
    public void aiStep() {
        super.aiStep(); // Call the parent method to retain normal behavior
        // Custom logic to ensure it does not try to eat grass
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.SHEEP_DEATH;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource damageSourceIn) {
        return SoundEvents.SHEEP_HURT;
    }

    @Override
    protected void playStepSound(BlockPos pos, BlockState blockIn) {
        this.playSound(SoundEvents.SHEEP_STEP, 0.15F, 1.0F);
    }

    // Custom goal for eating custom flora
    static class EatCustomFloraGoal extends Goal  {
        private final HerbivoreEntity entity;
        private BlockPos targetFloraPos;

        public EatCustomFloraGoal(HerbivoreEntity entity) {
            this.entity = entity;
        }

        private int searchCooldown = 0;

        @Override
        public boolean canUse() {
            if (searchCooldown > 0) {
                searchCooldown--;
                return false;
            }

            if (entity.getRandom().nextInt(5) == 0) {
                List<BlockPos> possiblePositions = new ArrayList<>();
                for (int x = -5; x <= 5; x++) {
                    for (int z = -5; z <= 5; z++) {
                        possiblePositions.add(entity.blockPosition().offset(x, 0, z));
                    }
                }

                Collections.shuffle(possiblePositions, entity.getRandom());

                for (BlockPos pos : possiblePositions) {
                    if (entity.level.getBlockState(pos).getBlock() instanceof CustomFlora) {
                        targetFloraPos = pos;
                        searchCooldown = 20; // Set cooldown for 1 second (20 ticks)
                        return true; // Found custom flora to eat
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
            if (targetFloraPos != null) {
                double distance = entity.distanceToSqr(targetFloraPos.getX(), targetFloraPos.getY(), targetFloraPos.getZ());
                if (distance > 3) {
                    entity.getNavigation().moveTo(targetFloraPos.getX(), targetFloraPos.getY(), targetFloraPos.getZ(), 1.0D);
                } else {
                    eatCustomFlora();
                    entity.getNavigation().stop();
                }
            }
        }
        @Override
        public boolean canContinueToUse() {
            return targetFloraPos != null && entity.level.getBlockState(targetFloraPos).getBlock() instanceof CustomFlora;
        }

        public AgeableEntity getBreedOffspring(ServerWorld world, AgeableEntity other) {
            return ModEntityTypes.HERBIVORE.get().create(world); // Create and return a new instance of HerbivoreEntity
        }

        private void eatCustomFlora() {
            if (entity.level.getBlockState(targetFloraPos).getBlock() instanceof CustomFlora) {
                entity.level.destroyBlock(targetFloraPos, true); // Remove the custom flora block
                entity.foodConsumed++; // Increment food consumed
                checkForBreeding(); // Check if the entity can breed
            } else {
                System.out.println("Target is not custom flora!");
            }
        }

        private void checkForBreeding() {
            if (entity.foodConsumed >= 3) { // Check if the herbivore has eaten enough
                entity.setInLove(null); // Set the herbivore in love to enable breeding
                entity.foodConsumed = 0; // Reset food consumed after breeding
            }
        }

    }
}
