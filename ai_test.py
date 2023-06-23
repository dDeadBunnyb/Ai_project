from tensorflow.keras.models import load_model # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import urllib.request
from  matplotlib import pyplot as plt
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

urllib.request.urlretrieve(
  'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Various_kimchi.jpg/640px-Various_kimchi.jpg',
   "kimchi.png")

np.set_printoptions(suppress=True)

# 모델 로드
model = load_model("keras_model.h5", compile=False)
# 레이블 로드
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model

# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# 테스트할 이미지 파일명을 입력
image = Image.open('kimchi.png').convert("RGB")

# resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

# turn the image into a numpy array
image_array = np.asarray(image)

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

# Load the image into the array
data[0] = normalized_image_array

# Predicts the model
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]


plt.imshow(image)
plt.show()
print(len(prediction))
print(index)
print(class_names)
print(prediction[0])