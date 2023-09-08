/usr/local/python/3.11.5/bin/python3.11 -u  finetune.py \
    --dataset_path "../../../data/dataset/dataset_title_train_and_valid" \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 16 \
    --gradient_accumulation_steps 1 \
    --num_train_epochs 1 \
    --save_steps 100 \
    --save_total_limit 5 \
    --learning_rate 1e-6 \
    --fp16 \
    --remove_unused_columns false \
    --logging_steps 10 \
    --eval_steps 100 \
    --load_best_model_at_end true \
    --evaluation_strategy "steps" \
    --output_dir "../../../output"  > train.log 2>&1