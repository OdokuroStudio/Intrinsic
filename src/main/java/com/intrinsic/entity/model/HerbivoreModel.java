package com.intrinsic.entity.model;

import com.mojang.blaze3d.matrix.MatrixStack;
import com.mojang.blaze3d.vertex.IVertexBuilder;
import net.minecraft.client.renderer.model.ModelRenderer;
import net.minecraft.client.renderer.entity.model.EntityModel;
import net.minecraft.entity.passive.AnimalEntity;


public class HerbivoreModel<T extends AnimalEntity> extends EntityModel<T> {
	private final ModelRenderer bone;
	private final ModelRenderer cube_r1;
	private final ModelRenderer cube_r2;
	private final ModelRenderer cube_r3;
	private final ModelRenderer rightear_r1;
	private final ModelRenderer leftear_r1;
	private final ModelRenderer bone2;
	private final ModelRenderer bone3;
	private final ModelRenderer bone4;
	private final ModelRenderer bone5;
	private final ModelRenderer tail;
	private final ModelRenderer cube_r4;
	private final ModelRenderer bb_main;

	public HerbivoreModel() {
		int textureWidth = 128;
		int textureHeight = 128;

		bone = new ModelRenderer(this);
		bone.setTexSize(textureWidth, textureHeight);
		bone.setPos(-18.0F, 1.2856F, 4.0F);
		setRotationAngle(bone, 0.0F, 0.0F, -0.3491F);
		bone.texOffs(0, 22).addBox(-4.2447F, -10.6F, -2.0F, 7.0F, 11.0F, 4.0F, 0.0F, false);
		bone.texOffs(22, 22).addBox(-4.2447F, -14.6F, -3.0F, 7.0F, 5.0F, 6.0F, 0.0F, false);
		bone.texOffs(48, 22).addBox(-9.2447F, -14.6F, -2.0F, 5.0F, 5.0F, 4.0F, 0.0F, false);
		bone.texOffs(48, 48).addBox(1.7553F, -19.6F, -3.0F, 1.0F, 5.0F, 1.0F, 0.0F, false);
		bone.texOffs(48, 48).addBox(1.7553F, -19.6F, 2.0F, 1.0F, 5.0F, 1.0F, 0.0F, false);

		cube_r1 = new ModelRenderer(this);
		cube_r1.setTexSize(textureWidth, textureHeight);
		cube_r1.setPos(-0.2447F, -19.6F, 3.0F);
		bone.addChild(cube_r1);
		setRotationAngle(cube_r1, 0.0F, 0.0F, -0.6545F);
		cube_r1.texOffs(4, 52).addBox(4.0F, -3.0F, -1.0F, 1.0F, 4.0F, 1.0F, 0.0F, false);
		cube_r1.texOffs(4, 52).addBox(4.0F, -4.0F, -6.0F, 1.0F, 5.0F, 1.0F, 0.0F, false);

		cube_r2 = new ModelRenderer(this);
		cube_r2.setTexSize(textureWidth, textureHeight);
		cube_r2.setPos(-2.0F, -15.1856F, 3.0F);
		bone.addChild(cube_r2);
		setRotationAngle(cube_r2, 0.0F, 0.0F, -0.6545F);
		cube_r2.texOffs(16, 44).addBox(3.7553F, -2.4144F, -1.0F, 1.0F, 4.0F, 1.0F, 0.0F, false);
		cube_r2.texOffs(16, 44).addBox(3.7553F, -1.4144F, -6.0F, 1.0F, 3.0F, 1.0F, 0.0F, false);

		cube_r3 = new ModelRenderer(this);
		cube_r3.setTexSize(textureWidth, textureHeight);
		cube_r3.setPos(-0.9F, -23.53F, 3.0F);
		bone.addChild(cube_r3);
		setRotationAngle(cube_r3, 0.0F, 0.0F, 0.7854F);
		cube_r3.texOffs(0, 52).addBox(4.6553F, -4.07F, -1.0F, 1.0F, 5.0F, 1.0F, 0.0F, false);
		cube_r3.texOffs(0, 52).addBox(4.6553F, -4.07F, -6.0F, 1.0F, 5.0F, 1.0F, 0.0F, false);

		rightear_r1 = new ModelRenderer(this);
		rightear_r1.setTexSize(textureWidth, textureHeight);
		rightear_r1.setPos(-2.2447F, -12.6F, 2.0F);
		bone.addChild(rightear_r1);
		setRotationAngle(rightear_r1, -1.0472F, 0.0F, 0.0F);
		rightear_r1.texOffs(42, 48).addBox(4.0F, -4.0F, -1.0F, 1.0F, 5.0F, 2.0F, 0.0F, false);

		leftear_r1 = new ModelRenderer(this);
		leftear_r1.setTexSize(textureWidth, textureHeight);
		leftear_r1.setPos(-2.2447F, -12.6F, -2.0F);
		bone.addChild(leftear_r1);
		setRotationAngle(leftear_r1, 1.0472F, 0.0F, 0.0F);
		leftear_r1.texOffs(16, 37).addBox(4.0F, -4.0F, -1.0F, 1.0F, 5.0F, 2.0F, 0.0F, false);

		bone2 = new ModelRenderer(this);
		bone2.setTexSize(textureWidth, textureHeight);
		bone2.setPos(-20.0F, 9.5F, 1.0F);
		bone2.texOffs(22, 31).addBox(-2.0F, -1.5F, -2.0F, 4.0F, 13.0F, 4.0F, 0.0F, false);

		bone3 = new ModelRenderer(this);
		bone3.setTexSize(textureWidth, textureHeight);
		bone3.setPos(-2.0F, 9.5F, 7.0F);
		bone3.texOffs(16, 46).addBox(-2.0F, -1.5F, -2.0F, 4.0F, 13.0F, 4.0F, 0.0F, false);

		bone4 = new ModelRenderer(this);
		bone4.setTexSize(textureWidth, textureHeight);
		bone4.setPos(-2.0F, 9.5F, 1.0F);
		bone4.texOffs(0, 35).addBox(-2.0F, -1.5F, -2.0F, 4.0F, 13.0F, 4.0F, 0.0F, false);

		bone5 = new ModelRenderer(this);
		bone5.setTexSize(textureWidth, textureHeight);
		bone5.setPos(-20.0F, 7.5F, 7.0F);
		bone5.texOffs(38, 31).addBox(-2.0F, 0.5F, -2.0F, 4.0F, 13.0F, 4.0F, 0.0F, false);

		tail = new ModelRenderer(this);
		tail.setTexSize(textureWidth, textureHeight);
		tail.setPos(-0.3931F, -1.0782F, 4.0F);

		cube_r4 = new ModelRenderer(this);
		cube_r4.setPos(0.3931F, 0.0782F, -1.0F);
		tail.addChild(cube_r4);
		setRotationAngle(cube_r4, 0.0F, 0.0F, 0.3927F);
		cube_r4.texOffs(32, 48).addBox(-2.0F, -8.0F, -0.5F, 2.0F, 8.0F, 3.0F, 0.0F, false);


		bb_main = new ModelRenderer(this);
		bb_main.setTexSize(textureWidth, textureHeight);
		bb_main.setPos(0.0F, 24.0F, 0.0F);
		bb_main.texOffs(0, 0).addBox(-22.0F, -26.0F, -1.0F, 22.0F, 12.0F, 10.0F, 0.0F, false);
	}

	@Override
	public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
		this.bone.xRot = (float) Math.cos(limbSwing * 0.6662F) * 1.4F * limbSwingAmount;
		this.bone2.xRot = (float) Math.cos(limbSwing * 0.6662F + (float) Math.PI) * 1.4F * limbSwingAmount;
		this.tail.yRot = (float) Math.cos(ageInTicks * 0.3F) * 0.25F;
	}


	@Override
	public void renderToBuffer(MatrixStack matrixStack, IVertexBuilder buffer, int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {
		bone.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
		bone2.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
		bone3.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
		bone4.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
		bone5.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
		tail.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
		bb_main.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
	}

	public void setRotationAngle(ModelRenderer modelRenderer, float x, float y, float z) {
		modelRenderer.xRot = x;
		modelRenderer.yRot = y;
		modelRenderer.zRot = z;
	}
}