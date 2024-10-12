package com.intrinsic.entity.render;

import com.intrinsic.entity.custom.HerbivoreEntity;
import com.intrinsic.entity.model.HerbivoreModel;
import net.minecraft.client.renderer.entity.EntityRendererManager;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.util.ResourceLocation;

public class HerbivoreEntityRenderer extends MobRenderer<HerbivoreEntity, HerbivoreModel<HerbivoreEntity>> {
    private static final ResourceLocation TEXTURE = new ResourceLocation("intrinsic", "textures/entity/herbivore.png"); // Change to your texture path

    public HerbivoreEntityRenderer(EntityRendererManager renderManager) {
        super(renderManager, new HerbivoreModel<>(), 0.5F); // Adjust the shadow size as needed
    }

    @Override
    public ResourceLocation getTextureLocation(HerbivoreEntity entity) {
        return TEXTURE;
    }
}
