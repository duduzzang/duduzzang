import nibabel as nib
import matplotlib.pyplot as plt
from PIL import Image

# 1. Proxy 불러오기
proxy = nib.load('4.nii.gz')

# 2. Header 불러오기
header = proxy.header

# 3. 원하는 Header 불러오기 (내용이 문자열일 경우 숫자로 표현됨)
header_size = header['sizeof_hdr']

# 2. 전체 Image Array 불러오기
arr = proxy.get_fdata()

# 3. 원하는 Image Array 영역만 불러오기
sub_arr = proxy.dataobj[..., 0:5]
print(sub_arr.shape)
# print(sub_arr)
sub_arr = sub_arr.reshape(sub_arr.shape[0], sub_arr.shape[1])

img = Image.fromarray(sub_arr)
plt.imshow(img, 'gray')
plt.show()