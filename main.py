import numpy as np
import cv2
import os
import argparse
import sys


'''This repository is heavily based on this implementation. https://blog.csdn.net/sinat_29047129/article/details/103642140'''

class SegmentationMetric(object):
    def __init__(self, numClass):
        self.confusion_matrix = None
        self.numClass = numClass
        self.confusionMatrix = np.zeros((self.numClass,) * 2)

    def pixelAccuracy(self):
        # return all class overall pixel accuracy
        #  PA = acc = (TP + TN) / (TP + TN + FP + TN)
        acc = np.diag(self.confusionMatrix).sum() / self.confusionMatrix.sum()
        return acc

    def classPixelAccuracy(self):
        # return each category pixel accuracy(A more accurate way to call it precision)
        # acc = (TP) / TP + FP
        classAcc = np.diag(self.confusionMatrix) / self.confusionMatrix.sum(axis=0)  # IMPORTANT: the axis must be 0 
        return classAcc  

    def meanPixelAccuracy(self):
        classAcc = self.classPixelAccuracy()
        meanAcc = np.nanmean(classAcc)  
        return meanAcc  

    def meanIntersectionOverUnion(self):
        # Intersection = TP Union = TP + FP + FN
        # IoU = TP / (TP + FP + FN)
        intersection = np.diag(self.confusionMatrix)  
        union = np.sum(self.confusionMatrix, axis=1) + np.sum(self.confusionMatrix, axis=0) - np.diag(
            self.confusionMatrix)  # axis = 1 -> row value； axis = 0 -> column value
        IoU = intersection / union  
        mIoU = np.nanmean(IoU) 
        return mIoU

    def genConfusionMatrix(self, imgPredict, imgLabel):
        # remove classes from unlabeled pixels in gt image and predict
        mask = (imgLabel >= 0) & (imgLabel < self.numClass)
        label = self.numClass * imgLabel[mask] + imgPredict[mask]
        count = np.bincount(label, minlength=self.numClass ** 2)
        confusionMatrix = count.reshape(self.numClass, self.numClass)
        return confusionMatrix

    def Frequency_Weighted_Intersection_over_Union(self):
        # FWIOU =     [(TP+FN)/(TP+FP+TN+FN)] *[TP / (TP + FP + FN)]
        freq = np.sum(self.confusion_matrix, axis=1) / np.sum(self.confusion_matrix)
        iu = np.diag(self.confusion_matrix) / (
                np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) -
                np.diag(self.confusion_matrix))
        FWIoU = (freq[freq > 0] * iu[freq > 0]).sum()
        return FWIoU

    def addBatch(self, imgPredict, imgLabel):
        assert imgPredict.shape == imgLabel.shape
        self.confusionMatrix += self.genConfusionMatrix(imgPredict, imgLabel)

    def reset(self):
        self.confusionMatrix = np.zeros((self.numClass, self.numClass))

def colorToGray(path):
    # color to grayscale and then flatten
    # for example, path = r'E:\Desktop\final.png'
    src = cv2.imread(path) # Ok
    Gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) # Ok
    _, thresh = cv2.threshold(Gray, 125, 1, cv2.THRESH_BINARY)
    thresh = thresh[:1020, :2040]
    Predict = thresh.flatten()
    return Predict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Input Parameters
    parser.add_argument('--pred', type=str, required=True) # the predicted outcome
    parser.add_argument('--gt', type=str, required=True)  # the gt label
    config = parser.parse_args()

    imgPredict = colorToGray(config.pred)  
    imgLabel = colorToGray(config.gt)  
    
    metric = SegmentationMetric(19)  # nums of classes, for cityscape it is 19
    metric.addBatch(imgPredict, imgLabel)

    mpa = metric.meanPixelAccuracy()
    mIoU = metric.meanIntersectionOverUnion()

    print('mpa is : %.4f' % mpa, file=open("output_pa.txt", "a"))
    print('mIoU is : %.4f' % mIoU, file=open("output_iou.txt", "a"))

