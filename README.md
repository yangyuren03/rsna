### RSNA Intracranial Hemorrhage Detection
  
[Hosted on Kaggle](https://www.kaggle.com/c/rsna-intracranial-hemorrhage-detection/overview)  
[Sponsored by RSNA](https://www.rsna.org/)   
   
![Frontpage](https://www.researchgate.net/profile/Sandiya_Bindroo/publication/326537078/figure/fig1/AS:650818105663489@1532178536539/Magnetic-resonance-imaging-MRI-of-the-brain-showing-scattered-punctate-infarcts-in-the.png) . 

#### Results

| Model          |Image Size|Epochs|Bag|TTA |Fold|Val     |LB    |Comment                          |
| ---------------|----------|------|---|----|----|--------|------|---------------------------------|
| ResNeXt-101 32x8d |256       |7     |5X |None|0   |0.06489 |0.070 | Weighted `[0.6, 1.8, 0.6]` rolling mean win3, transpose, `submission_v4.py` |
| ResNeXt-101 32x8d |256       |7     |5X |None|0   |0.06582 |0.070 |Rolling mean window 3, transpose, `submission_v3.py` |
| ResNeXt-101 32x8d |256       |4     |3X |None|0   |0.06874 |0.074 |Rolling mean window 3, transpose, `submission_v3.py` |
| EfficientnetV0 |256       |6     |3X |None|0   |0.07416 |0.081 |Rolling mean window 3, no transpose, `submission_v2.py` |
| EfficientnetV0 |384       |4     |2X |None|0   |0.07661 |0.085 |With transpose augmentation      |
| EfficientnetV0 |384       |2     |1X |None|0   |0.07931 |0.088 |With transpose augmentation      |
| EfficientnetV0 |384       |11    |2X |None|0   |0.08330 |0.093 |With transpose augmentation      |
| EfficientnetV0 |224       |4     |2X |None|0   |0.08047 |????  |Without transpose augmentation   |
| EfficientnetV0 |224       |4     |2X |None|0   |0.08267 |????  |With transpose augmentation      |
| EfficientnetV0 |224       |2     |1X |None|0   |0.08519 |????  |With transpose augmentation      |
| EfficientnetV0 |224       |11    |2X |None|0   |0.08607 |????  |With transpose augmentation      |

#### Experiment Results
1. Cropping image gives approx 0.04. 
2. Mix up improves about 0.03 on EfficientnetV0, but obviously takes longer to converge. Convergence time on same model about 20 epochs instead of 5 without mixup. 
3. Remove the transpose on augmentation gets a 0.02 improvement. 

#### Experiments
1. Best training augmentation so far... [linky](https://github.com/darraghdog/rsna/blob/a3a50331955be5f3443e548e692a29d041d24cfe/scripts/efficientnetb0v7/trainorig.py#L210)
```
transform_train = Compose([
    HorizontalFlip(p=0.5),
    ShiftScaleRotate(shift_limit=0.1, scale_limit=0.01, 
                         rotate_limit=30, p=0.7, border_mode = cv2.BORDER_REPLICATE),
    ToTensor()
])
```

#### Does not work
1. Downsampling patients with no conditions. 