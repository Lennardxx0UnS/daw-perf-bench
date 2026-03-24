# 🎹 DAW Performance Benchmark (v1.0)

**PROJECT ※ UNAMED • SPACE** | *DAW Performance Research Initiative*
*co-designed with Google Gemini*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/badge/release-v1.0-brightgreen.svg)]()

> 彻底打破“唯多核跑分论”，专为数字音频工作站（DAW）与现代音乐制作环境打造的**底层算力与 UX 体验量化评估系统**。

## 💡 项目简介 (Introduction)

传统的数码评测（如 3D 渲染、光线追踪测试）与 DAW（如 Cubase, Studio One, Ableton Live）中 **强制串行、极低延迟、极度吃缓存** 的真实物理计算需求存在严重脱节。

本项目基于 **Cinebench** 与 **Geekbench 6** 的底层算法映射，结合 **柯布-道格拉斯 (Cobb-Douglas) 几何加权** 与 **S型曲线 (Sigmoid) 动态阈值映射**，实现了从冷冰冰的硬件跑分到编曲人真实体感（UX 流程度）的精准预测。

### 核心特性 (Key Features)
- **🧠 抛弃光追，引入 AVX 代理**：通过 `GB6 背景模糊` 分数精准代理 CPU 的 AVX-512 / AMX 矢量算力，还原真实 DSP 连乘性能。
- **📦 L3 / SLC 缓存惩罚机制**：完美量化 ASIO Guard 等预渲染缓冲对 L3 缓存与内存带宽的贪婪渴求。
- **⚖️ 动态工程权重 (木桶效应)**：支持自定义三大音频场景权重（多轨管弦、单轨混音、低延迟实录），任何单一维度的短板都将引发 UX 分数断崖式下跌。

## 🚀 快速开始 (Quick Start)

### 1. 环境依赖
本项目核心脚本仅依赖 Python 3 标准库，无需安装任何第三方包：
```bash
python --version  # 需确保 Python 3.8 或以上版本