# PPOCR-ONNX

## 简介

利用 onnxruntime 及 PaddleOCR 提供的模型, 对图片中的文字进行检测与识别.

### 使用模型

- 文字检测: `ch_PP-OCRv2_det_infer`
- 方向分类: `cls mobile v2`
- 文字识别: `rec mobile v2`

## 安装

```shell
pip install ppocr-onnx
```

## 使用

### 识别分行的文本(每行一张图片, RGB 格式)

```python
from ppocronnx import TextSystem
import cv2

ts = TextSystem()
img = cv2.imread('test.png')
print(ts.ocr_lines([img]))
```

### 文本检测及识别

```python
from ppocronnx import TextSystem
import cv2

ts = TextSystem()
img = cv2.imread('test.png')
print(ts.detect_and_ocr(img))
```

## 参考

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [手把手教你使用ONNXRunTime部署PP-OCR](https://aistudio.baidu.com/aistudio/projectdetail/1479970)
- `ch_PP-OCRv2_det_infer` 模型来自 [RapidAI/RapidOCR](https://github.com/RapidAI/RapidOCR)
