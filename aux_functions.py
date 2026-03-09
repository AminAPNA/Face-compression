
import numpy as np

def computeSVD(frame: np.ndarray) -> list:
    frameR = frame[:,:,0]
    frameG = frame[:,:,1]
    frameB = frame[:,:,2]

    UR, SR, VtR = np.linalg.svd(frameR)
    UG, SG, VtG = np.linalg.svd(frameG)
    UB, SB, VtB = np.linalg.svd(frameB)

    return UR, SR, VtR, UG, SG, VtG, UB, SB, VtB

def addCompressedFactorsSVD(frameSVD: list, frame_compress: np.ndarray, nsvalsStart:int, nsvalsEnd: int) -> np.ndarray:
    UR, SR, VtR, UG, SG, VtG, UB, SB, VtB = frameSVD

    frame_compress[:,:,0] += (UR[:,nsvalsStart:nsvalsEnd] @ np.diag(SR[nsvalsStart:nsvalsEnd]) @ VtR[nsvalsStart:nsvalsEnd,:])
    frame_compress[:,:,1] += (UG[:,nsvalsStart:nsvalsEnd] @ np.diag(SG[nsvalsStart:nsvalsEnd]) @ VtG[nsvalsStart:nsvalsEnd,:])
    frame_compress[:,:,2] += (UB[:,nsvalsStart:nsvalsEnd] @ np.diag(SB[nsvalsStart:nsvalsEnd]) @ VtB[nsvalsStart:nsvalsEnd,:])
    
    return frame_compress

def SVD_compress(frame: np.ndarray, nsvals: int) -> np.ndarray:    
    frameSVD = computeSVD(frame)

    frame_compress = np.zeros_like(frame, dtype=np.float64)
    frame_compress = addCompressedFactorsSVD(frameSVD, frame_compress, 0, nsvals)

    return frame_compress.clip(0, 255).astype(np.uint8)