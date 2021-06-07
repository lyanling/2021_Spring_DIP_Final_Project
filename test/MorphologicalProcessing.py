import numpy as np
import cv2 as cv

class MorphologicalProcessing:
    def __init__(self, img, t = 127):
        self.img = np.where(img > t, False, True)
        self.img_uint8 = np.where(img > t, 0, 255).astype(np.uint8)
        self.img_check = np.where(img > t, 255, 0).astype(np.uint8)
        return
    def boolToUint8(self, img):
        img_ret = np.where(img==True, 255, 0)
        img_ret = img_ret.astype(np.uint8)
        return img_ret
    def getStructuringElement(self, type):
        if type == 'boundary extraction' or type == '8-connectivity object counting':
            H = np.ones((3, 3))
            C_x = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
            C_y = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        elif type == 'hole filling' or type == '4-connectivity object counting':
            H = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
            C_x = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
            C_y = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        
        return H, C_x, C_y
    def Erosion(self, img, H, C_x, C_y):
        m, n = img.shape
        s1, s2 = H.shape
        img_ret = np.ones_like(img)
        for x in range(s1):
            for y in range(s2):
                if H[x, y]:
                    img_ret[max(C_x[x, y], 0):min(m+C_x[x, y], m), max(C_y[x, y], 0):min(n+C_y[x, y], n)] = np.logical_and(img_ret[max(C_x[x, y], 0):min(m+C_x[x, y], m), max(C_y[x, y], 0):min(n+C_y[x, y], n)], img[max(-C_x[x, y], 0):min(m-C_x[x, y], m), max(-C_y[x, y], 0):min(n-C_y[x, y], n)])
        return img_ret
    def Dilation(self, img, H, C_x, C_y):
        m, n = img.shape
        s1, s2 = H.shape
        img_ret = np.zeros_like(img)
        for x in range(s1):
            for y in range(s2):
                if H[x, y]:
                    img_ret[max(C_x[x, y], 0):min(m+C_x[x, y], m), max(C_y[x, y], 0):min(n+C_y[x, y], n)] = np.logical_or(img_ret[max(C_x[x, y], 0):min(m+C_x[x, y], m), max(C_y[x, y], 0):min(n+C_y[x, y], n)], img[max(-C_x[x, y], 0):min(m-C_x[x, y], m), max(-C_y[x, y], 0):min(n-C_y[x, y], n)])
        return img_ret
    def boundaryExtraction(self):
        H, C_x, C_y = self.getStructuringElement('boundary extraction')
        img_erosion = self.Erosion(self.img, H, C_x, C_y)
        img_erosion = self.boolToUint8(img_erosion)
        img_ret = self.img_uint8 - img_erosion
        img_ret = np.where(img_ret < 0, 0, img_ret)
        return img_ret
    def holeFilling(self):
        H, C_x, C_y  = self.getStructuringElement('hole filling')
        G = np.zeros_like(self.img)
        G[0, :] = True
        G[-1, :] = True
        G[:, 0] = True
        G[:, -1] = True
        F_c = np.logical_not(self.img)
        while(1):
            G_new = self.Dilation(G, H, C_x, C_y )
            G_new = np.logical_and(G_new, F_c)
            if (G_new == G).all():
                break
            G = G_new
        img_ret = self.boolToUint8(np.logical_not(G_new))
        return img_ret
    def objectCounting(self, connectivity=8):
        # print('connectivity: ', connectivity)
        count = 0
        img_hole_filled = self.holeFilling()
        img_labeled = np.zeros_like(self.img)
        img_label = np.zeros(self.img.shape)
        m, n = self.img.shape
        if connectivity==8:
            H, C_x, C_y = self.getStructuringElement('8-connectivity object counting')
        elif connectivity==4:
            H, C_x, C_y = self.getStructuringElement('4-connectivity object counting')
        for x in range(m):
            for y in range(n):
                if not img_labeled[x, y] and img_hole_filled[x, y]:
                    img_labeled[x, y] = True
                    # dilation until converge
                    while(True):
                        img_dilated = self.Dilation(img_labeled, H, C_x, C_y)
                        img_labeled_new = np.logical_and(img_dilated, img_hole_filled)
                        if (img_labeled_new == img_labeled).all():
                            break
                        img_label[img_labeled_new != img_labeled] = count+1
                        img_labeled = img_labeled_new
                    count += 1
        img_ret = img_label.astype(np.uint8)
        return count, img_ret