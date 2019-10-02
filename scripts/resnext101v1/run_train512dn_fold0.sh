N_GPU=1
WDIR='resnext101v1'
FOLD=0
SIZE='512'


bsub  -q lowpriority -gpu "num=$N_GPU:mode=exclusive_process" -app gpu -n =$N_GPU  -env LSB_CONTAINER_IMAGE=darraghdog/kaggle:apex_build \
            -n 1 -R "span[ptile=4]" -o log_train_%J  sh -c "cd /share/dhanley2/rsna/scripts/$WDIR  && python3 traindn.py  \
            --logmsg Rsna-densenet121-$SIZE-fp16 --epochs 10 --fold $FOLD  --lr 0.00002 --batchsize 16  --workpath scripts/$WDIR  \
            --imgpath data/mount/512X512X6/ --weightsname weights/model_512_densenet121$FOLD.bin"