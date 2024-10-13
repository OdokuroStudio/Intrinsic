package com.intrinsic.entity.render;

import com.intrinsic.entity.custom.CarnivoreEntity; // Make sure to import your carnivore entity class
import com.intrinsic.entity.model.CarnivoreModel; // Make sure to import your carnivore model class
import net.minecraft.client.renderer.entity.EntityRendererManager;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.util.ResourceLocation;

public class CarnivoreEntityRenderer extends MobRenderer<CarnivoreEntity, CarnivoreModel<CarnivoreEntity>> {
    private static final ResourceLocation TEXTURE = new ResourceLocation("intrinsic", "textures/entity/carnivore.png"); // Change to your texture path

    public CarnivoreEntityRenderer(EntityRendererManager renderManager) {
        super(renderManager, new CarnivoreModel<>(), 0.5F); // Adjust the shadow size as needed
    }

    @Override
    public ResourceLocation getTextureLocation(CarnivoreEntity entity) {
        return TEXTURE;
    }
}
