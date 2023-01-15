
from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="paratools",
    version="0.0.1",
    author="wangguojim",
    author_email="862876363@qq.com",
    description="A light implementation for transformers and distributed training",
    keywords="NLP deep learning transformer pytorch deepspeed BERT GPT GPT-2 T5 model parallel data parallel",
    license="MIT",
    url="https://github.com/wangguojim/LightTransformers/",
    packages=find_packages(),
    install_requires=required,
    python_requires=">=3.6.0",
)


