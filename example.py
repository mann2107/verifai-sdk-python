import os
from verifai_sdk import VerifaiService


# First we setup the class
service = VerifaiService(token='<API KEY IN HERE>')
service.add_clasifier_url('http://localhost:5000/api/')

# Error for non existing
service.add_clasifier_url(
    'http://localhost:6000/api/',
    skip_unreachable=True
)

# By path to the JPEG
sample_dir = 'docs/sample_images/'
image_path = os.path.join(sample_dir, 'dutch-id-front-sample.jpg')
document = service.classify_image_path(image_path)
print(document)
print("Classified as", document.id_uuid)
print(document.model)
print(document.country)
print(document.position_in_image)
