from mmocr.apis import MMOCRInferencer
ocr = MMOCRInferencer(det='MaskRCNN_IC15', rec='abinet_20e_st-an_mj')
ocr('./data/pic.jpg', show=True, print_result=True)


# import mmcv
# import matplotlib.pyplot as plt
#
# predicted_img = mmcv.imread('./data/pic.jpg')
#
# plt.imshow(mmcv.bgr2rgb(predicted_img))
# plt.show()