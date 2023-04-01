from django.test import TestCase

# Create your tests here.
import shortuuid
print(shortuuid.ShortUUID().random(length=34))