_base_ = [
    '../_base_/models/RMT_Swin_upper.py', 
    '../_base_/datasets/ade20k_uper.py',
    '../_base_/default_runtime.py', 
    '../_base_/schedules/schedule_160k.py'
]

# model.pretrained is actually loaded by backbone, see
# https://github.com/open-mmlab/mmsegmentation/blob/186572a3ce64ac9b6b37e66d58c76515000c3280/mmseg/models/segmentors/encoder_decoder.py#L32

model=dict(
    pretrained=None, 
    backbone=dict(
        embed_dims=[96, 192, 384, 768],
        depths=[2, 2, 18, 2],
        num_heads=[6, 6, 12, 24],
        init_values=[2, 2, 2, 2],
        heads_ranges=[6, 6, 6, 6],
        mlp_ratios=[4, 4, 4, 4],
        drop_path_rate=0.4,
        chunkwise_recurrents=[True, True, True, False],
        layerscales=[False, False, True, True],
        layer_init_values=1e-6,
        out_indices = (0, 1, 2, 3)), # it seems that, upernet requires a larger dpr
    decode_head=dict(
        in_channels=[96, 192, 384, 768],
        num_classes=150),
    auxiliary_head=dict(
        in_channels=384,
        num_classes=150))


############## below we strictly follow uniformer & cswin ####################################
# https://github.com/Sense-X/UniFormer/blob/main/semantic_segmentation/exp/upernet_global_small/config.py
# https://github.com/microsoft/CSWin-Transformer/blob/main/segmentation/configs/cswin/upernet_cswin_tiny.py
##############################################################################################
# AdamW optimizer, no weight decay for position embedding & layer norm in backbone

optimizer = dict(_delete_=True, type='AdamW', lr=0.00006, betas=(0.9, 0.999), weight_decay=0.01,
                 paramwise_cfg=dict(custom_keys={'absolute_pos_embed': dict(decay_mult=0.),
                                                 'relative_position_bias_table': dict(decay_mult=0.),
                                                 'norm': dict(decay_mult=0.)}))
lr_config = dict(_delete_=True, policy='poly',
                 warmup='linear',
                 warmup_iters=1500,
                 warmup_ratio=1e-6,
                 power=1.0, min_lr=0.0, by_epoch=False)

data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2
)
#############################################################################
runner = dict(max_iters=160000, work_dir='/mnt/bn/fqh-bytenas-data3/RMT_Uper_Swin_S_2x')
checkpoint_config = dict(max_keep_ckpts=1, interval=8000)
evaluation = dict(interval=8000, save_best='mIoU')

# NOTE: True is conflict with checkpoint 
# https://github.com/allenai/longformer/issues/63#issuecomment-648861503
find_unused_parameters=False

# place holder for new verison mmseg compatiability
resume_from=None
device='cuda'

# fp32 training (choose this if nan loss occurs)->
# optimizer_config = dict()

# AMP (faster but may meet nan loss) ->
optimizer_config = dict(type='Fp16OptimizerHook', loss_scale=512.)
fp16 = dict()
