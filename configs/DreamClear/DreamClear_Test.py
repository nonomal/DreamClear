_base_ = ['../PixArt_xl2_internal.py']
data_root = 'data'
image_list_json = ['data_info.json',]

data = dict(type='InternalDataHed', root='InternData', image_list_json=image_list_json, transform='default_train', load_vae_feat=True)
image_size = 1024

# model setting
model = 'PixArtMS_XL_2'
fp32_attention = False  # Set to True if you got NaN loss
load_from = '/mnt/bn/yiren-bytenas2/yuang.ai/exp/pixart/ckpt/PixArt-XL-2-1024-MS.pth'
window_block_indexes = []
window_size=0
use_rel_pos=False
lewei_scale = 2.0

# training setting
mixed_precision = "bf16"
full_mixed = False
num_workers=10
train_batch_size = 4 #  set the batch size according to your VRAM
num_epochs = 100 # 3
gradient_accumulation_steps = 1
grad_checkpointing = True
gradient_clip = 1.0
optimizer = dict(type='AdamW', lr=5e-5, weight_decay=1e-2, eps=1e-10)
lr_schedule_args = dict(num_warmup_steps=0)
save_model_epochs=1

log_interval = 20
eval_sampling_steps = 200
work_dir = 'validation'

# controlnet related params
copy_blocks_num = 28
class_dropout_prob = 0.5