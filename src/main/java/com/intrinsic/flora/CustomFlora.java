package com.intrinsic.flora;

import net.minecraft.block.BushBlock;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.block.SoundType;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.material.Material;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.IBlockReader;
import net.minecraft.world.server.ServerWorld;
import net.minecraft.util.math.MathHelper;
import net.minecraft.world.World;

import java.util.Random;

public class CustomFlora extends BushBlock {

    public CustomFlora() {
        super(AbstractBlock.Properties.of(Material.PLANT)
                .noCollission()      // No collision to prevent jumping
                .noOcclusion()       // No shadow casting
                .instabreak()        // Instantly breakable
                .sound(SoundType.GRASS) // Plant-like sound
                .randomTicks()       // Enable random ticking for spread
        );
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, IBlockReader worldIn, BlockPos pos) {
        // Can only place on grass, dirt, or farmland
        return state.is(Blocks.GRASS_BLOCK) || state.is(Blocks.DIRT) || state.is(Blocks.FARMLAND);
    }

    @Override
    public void randomTick(BlockState state, ServerWorld worldIn, BlockPos pos, Random random) {
        super.randomTick(state, worldIn, pos, random);

        // Chance for the flora to spread (e.g. 1 in 4 chance)
        if (random.nextInt(2) == 0) {
            BlockPos targetPos = pos.offset(MathHelper.nextInt(random, -3, 3), MathHelper.nextInt(random, -1, 1), MathHelper.nextInt(random, -3, 3));
            BlockState blockBelow = worldIn.getBlockState(targetPos.below());

            if (worldIn.isEmptyBlock(targetPos) && this.mayPlaceOn(blockBelow, worldIn, targetPos.below())) {
                worldIn.setBlockAndUpdate(targetPos, this.defaultBlockState());
            }
        }
    }

    public boolean propagatesSkylightDown(BlockState state, IBlockReader worldIn, BlockPos pos) {
        return true;  // Ensures light passes through, no shadow casting
    }
}
