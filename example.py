import os
from verifai_sdk import VerifaiService


# First we setup the class
service = VerifaiService(token='d67efa9f42810bf845ed25026ad014c4effbcc63')
service.add_clasifier_url('http://localhost:5000/api/classify/')

# Error for non existing
service.add_clasifier_url(
    'http://localhost:6000/api/classify/',
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

print(document.zones)

print(document.zones[0].title)
print(document.zones[0].side)

exit(0)
# ID Front + masking of all zones
document = service.classify_image_path('docs/sample_images/dutch-id-front-sample.jpg')

masked_image = document.mask_zones(document.zones)

# Save it
masked_image.save('masked.jpg')
