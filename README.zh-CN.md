<div align="center">

# NB-PET

### 常规报告监督下儿童神经母细胞瘤 PET/CT 的多标签识别与报告引导三维定位

**常规报告监督 · 纯影像识别 · 报告条件定位**

[English README](README.md) · [论文结果](#论文结果) · [数据与评价](docs/data-and-evaluation.md) · [发布状态](docs/release-status.md)

</div>

## 项目简介

NB-PET 从常规中文 PET/CT 报告提取临床标签及粗解剖区域，用于监督儿童神经母细胞瘤全身 PET/CT 的多标签识别与三维空间响应建模。识别与定位是两个独立任务，推理输入不同。

![论文图 1：报告监督的纯影像识别与报告引导三维定位](assets/figures/paper-fig1-framework.png)

*论文图 1。报告结构化提供监督；纯影像识别与报告引导定位在推理时使用不同输入。*

## 方法与评价

| 任务 | 推理输入 | 输出 |
|---|---|---|
| 多标签识别 | PET/CT 影像，不输入当前病例报告 | 检查级临床标签分数 |
| 报告引导定位 | PET/CT 影像、当前报告标签及对应解剖区域 | 总体和标签特异性三维热图、候选区域排序 |

论文队列包含北京友谊医院 656 例和浙江大学医学院附属儿童医院 280 例。两中心各评价 26 个标签，跨中心识别限定于 25 个共享标签。定位评价的参考由报告衍生，不能将区域命中率等同于逐病灶定位准确率。

## 论文结果

<p align="center">
  <a href="assets/figures/paper-fig4-cross-center.jpg"><img src="assets/figures/paper-fig4-cross-center.jpg" alt="论文图 4：中心内校准、跨中心识别与少样本适应" width="840" /></a>
</p>

*论文图 4。a 为中心内留出预测的概率校准，b–d 展示双向跨中心识别与少样本适应。*

下表为论文表 3 中 NB-PET 的点估计：

| 队列 | Hit@1 ↑ | Hit@3 ↑ | WRMR ↑ | PULR ↓ | SUV-Enrichment ↑ | Components ↓ |
|---|---:|---:|---:|---:|---:|---:|
| 北京 | 0.9939 | 0.9954 | 0.9816 | 0.0093 | 6.7421 | 23.5078 |
| 浙江 | 0.8286 | 0.8571 | 0.7603 | 0.0060 | 1.6884 | 40.0571 |

[查看完整表 3（对照方法、区间和 P 值）](docs/paper-results.md#table-3--regional-agreement-and-spatial-distribution-of-report-guided-heatmaps)。

## 快速开始

下面仅运行**合成评分示例**，无需安装额外依赖，无需医院数据：

```bash
python3 scripts/run_synthetic_evaluation.py
python3 -m unittest discover -s tests -v
```

本仓库公开论文图 1、图 4、表 3 和合成评分示例，不提供完整模型、权重、患者数据或论文全文。
