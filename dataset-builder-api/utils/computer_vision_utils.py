import cv2
import numpy as np
from skimage.measure import shannon_entropy

def compute_entropy(file_path):
  grey_image = cv2.imread(file_path, cv2.COLOR_BGR2GRAY)
  return shannon_entropy(grey_image)

def compute_edge_density(file_path):
  grey_image = cv2.imread(file_path, cv2.COLOR_BGR2GRAY)
  edges = cv2.Canny(grey_image, 100, 200)
  edge_pixels = np.sum(edges > 0)
  total_edge_pixels = edges.size
  return edge_pixels / total_edge_pixels