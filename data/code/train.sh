python  train.py \
    --model_name_or_path $1 \
    --data_path $2 \
    --bf16 True \
    --output_dir $3 \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 16 \
    --gradient_accumulation_steps 4 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_total_limit 10 \
    --learning_rate 2e-5 \
    --logging_steps 10 \
    --tf32 False \
    --save_steps 5000