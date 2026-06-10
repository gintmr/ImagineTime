# Can Image Models Imagine Time?

This repository hosts the public release materials for the paper **“Can Image Models Imagine Time? ImageTime: A Novel Benchmark for Probing Visual World Modeling Through Spatiotemporal Consistency”**

- Paper: [arXiv:2606.10620](https://arxiv.org/abs/2606.10620)
- Dataset: [Xin-Rui/ImageTime_Benchmark](https://huggingface.co/datasets/Xin-Rui/ImageTime_Benchmark)

<p align="center">
  <img src="assets/Intro.png" alt="ImagineTime Intro" width="95%">
</p>

## Overview

**ImagineTime** is a benchmark for evaluating whether image generation models can produce temporally ordered 2x2 motion sheets with coherent entities, spatial relations, state transitions, and causal constraints.

This GitHub repository contains the lightweight public materials for the paper:

- evaluation prompts and scoring rubrics;
- C and D capability/diagnostic criteria;
- one representative prompt example for each of the 22 domains;
- pointers to the full benchmark release on Hugging Face.

The full benchmark package is available on Hugging Face Datasets and includes 750 cases, prompt-only generations from eight models, VLM score files, aggregate summaries, reference images, and scaffold templates.

## Resources

- Paper: https://arxiv.org/abs/2606.10620
- Hugging Face dataset: https://huggingface.co/datasets/Xin-Rui/ImageTime_Benchmark

## Repository Layout

```text
assets/
  Intro figure for the paper and benchmark.

evaluation_prompt/
  Public VLM-as-judge prompt and C0-C9 ability rubric.

examples_by_domain/
  One representative prompt example for each benchmark domain.
```

## Citation

If you use ImagineTime, please cite the paper:

```bibtex
@misc{imagetime2026,
  title        = {Can Image Models Imagine Time?},
  year         = {2026},
  eprint       = {2606.10620},
  archivePrefix = {arXiv},
  primaryClass = {cs.CV},
  url          = {https://arxiv.org/abs/2606.10620}
}
```
