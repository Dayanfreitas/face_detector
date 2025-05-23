from typing import Tuple, Union
import math
import cv2
import numpy as np
import os

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 2
FONT_THICKNESS = 1
TEXT_COLOR = (0, 255, 0) 

# Configuração do caminho das imagens
FOTOS_DIR = 'fotos'

def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    # TODO: Draw coordinates even if it's outside of the image bounds.
    return None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px


def visualize(
    image,
    detection_result
) -> np.ndarray:
  """Draws bounding boxes and keypoints on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  annotated_image = image.copy()
  height, width, _ = image.shape

  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(annotated_image, start_point, end_point, TEXT_COLOR, 3)

    # Draw keypoints
    for keypoint in detection.keypoints:
      keypoint_px = _normalized_to_pixel_coordinates(keypoint.x, keypoint.y,
                                                     width, height)
      color, thickness, radius = (0, 255, 0), 2, 2
      cv2.circle(annotated_image, keypoint_px, thickness, color, radius)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    category_name = '' if category_name is None else category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (MARGIN + bbox.origin_x,
                     MARGIN + ROW_SIZE + bbox.origin_y)
    cv2.putText(annotated_image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

  return annotated_image


# import cv2

# img = cv2.imread(IMAGE_FILE)
# cv2.imshow('Imagem', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# STEP 2: Create an FaceDetector object.
base_options = python.BaseOptions(model_asset_path='detector.tflite')
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

list_without_face = []

# STEP 3: Processar todas as imagens no diretório
for filename in os.listdir(FOTOS_DIR):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(FOTOS_DIR, filename)
        print(f"Processando imagem: {filename}")
        
        # Carregar a imagem
        image = mp.Image.create_from_file(image_path)
        
        # Detectar faces na imagem
        detection_result = detector.detect(image)
        
        # Adicionar informações de debug
        print(f"Número de faces detectadas em {filename}: {len(detection_result.detections)}")
        if len(detection_result.detections) == 0:
          list_without_face.append(filename)
        
        # Processar o resultado da detecção
        image_copy = np.copy(image.numpy_view())
        annotated_image = visualize(image_copy, detection_result)
        rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        
        # Mostrar a imagem processada
        cv2.imshow(f'Imagem: {filename}', rgb_annotated_image)
        print(f"Pressione qualquer tecla para continuar...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def save_list_to_file(list, filename):
  with open(filename, 'w') as f:
    for filename in list:
      f.write(filename + '\n')

print(f"Imagens sem faces: {list_without_face}")
save_list_to_file(list_without_face, 'imagens_sem_face.txt')
