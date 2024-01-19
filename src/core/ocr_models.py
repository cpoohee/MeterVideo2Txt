det_models = {
    'MaskRCNN_IC15': 'models/mask-rcnn_resnet50_fpn_160e_icdar2015_20220826_154808-ff5c30bf.pth',
    'DBNetpp': 'models/dbnetpp_resnet50-oclip_fpnc_1200e_icdar2015_20221101_124139-4ecb39ac.pth',
    'FCENet': 'models/fcenet_resnet50-oclip_fpn_1500e_icdar2015_20221101_150145-5a6fc412.pth',
    'Fixed Area': ''
}
rec_models = {
    'svtr-base': 'models/svtr-base_20e_st_mj-ea500101.pth',
    'ABINet': 'models/abinet_20e_st-an_mj_20221005_012617-ead8c139.pth',
    # 'MAERec': 'models/maerec_b_union14m-4b98d1b4.pth'
    'SATRN_sm': 'models/satrn_shallow-small_5e_st_mj_20220915_152442-5591bf27.pth'
}
models = det_models | rec_models

models_url = {
    'MaskRCNN_IC15': 'https://download.openmmlab.com/mmocr/textdet/maskrcnn/mask-rcnn_resnet50_fpn_160e_icdar2015/mask-rcnn_resnet50_fpn_160e_icdar2015_20220826_154808-ff5c30bf.pth',
    'DBNetpp': 'https://download.openmmlab.com/mmocr/textdet/dbnetpp/dbnetpp_resnet50-oclip_fpnc_1200e_icdar2015/dbnetpp_resnet50-oclip_fpnc_1200e_icdar2015_20221101_124139-4ecb39ac.pth',
    'FCENet': 'https://download.openmmlab.com/mmocr/textdet/fcenet/fcenet_resnet50-oclip_fpn_1500e_icdar2015/fcenet_resnet50-oclip_fpn_1500e_icdar2015_20221101_150145-5a6fc412.pth',
    'svtr-base': 'https://download.openmmlab.com/mmocr/textrecog/svtr/svtr-base_20e_st_mj/svtr-base_20e_st_mj-ea500101.pth',
    'ABINet': 'https://download.openmmlab.com/mmocr/textrecog/abinet/abinet_20e_st-an_mj/abinet_20e_st-an_mj_20221005_012617-ead8c139.pth',
    # 'MAERec': 'https://download.openmmlab.com/mmocr/textrecog/mae/mae_union14m/maerec_b_union14m-4b98d1b4.pth'
    'SATRN_sm': 'https://download.openmmlab.com/mmocr/textrecog/satrn/satrn_shallow-small_5e_st_mj/satrn_shallow-small_5e_st_mj_20220915_152442-5591bf27.pth'
}

model_config = {
    'svtr-base': 'src/model_config/textrecog/svtr/svtr-base_20e_st_mj.py',
    'ABINet': 'src/model_config/textrecog/abinet/abinet_20e_st-an_mj.py',
    'SATRN_sm': 'src/model_config/textrecog/satrn/satrn_shallow-small_5e_st_mj.py'
}