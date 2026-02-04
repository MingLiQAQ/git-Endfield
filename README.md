# 终末地刷基质分析工具 / Endfield Weapon Matrix Analysis Tool

[English Version Below | 英文版本在下]

## 📖 简介

这是一个用于分析《终末地》游戏中武器刷取概率的工具。通过分析武器词条组合，帮助玩家找出特定武器与其他武器共享刷取词条的最优刷取策略。

## ✨ 功能特性

- 🔍 **武器查询分析**：输入目标武器名称，分析其在各地图的可刷取性
- 🗺️ **多地图支持**：自动识别并加载所有地图数据表
- ⭐ **星级筛选**：可按最低星级（4/5/6星）过滤显示结果
- 🎯 **词条组合分析**：
  - 固定第二词条分析
  - 固定第三词条分析
  - 显示共享词条的其他武器
- 📊 **数据可视化**：清晰展示武器词条组合关系
- 🖥️ **交互模式**：支持命令行交互操作

## 📁 项目结构

```
weapon-analyzer/
├── src/
│   └── weapon_analyzer.py     # 主程序文件
├── data/
│   └── 武器毕业基质表.xlsx     # 武器数据Excel文件
├── docs/
│   └── 使用说明.md            # 详细使用说明
├── requirements.txt           # 项目依赖
├── README.md                 # 本文件
└── .gitignore               # Git忽略文件
```

## ⚙️ 环境要求

- Python 3.8+
- 依赖库：
  - pandas
  - openpyxl
  - numpy（可选）

## 🔧 安装与使用

### 快速开始

1. **克隆仓库**
```bash
git clone [仓库地址]
cd weapon-analyzer
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行程序**
```bash
python src/weapon_analyzer.py
```

### 配置说明

程序支持两种使用方式：

#### 方式一：直接配置（修改代码）
```python
# 在代码开头配置区域设置
TARGET_WEAPON = "宏愿"     # 目标武器名称
SHOW_STAR = 1              # 1=显示星级，0=不显示
MIN_STAR = 5               # 最低显示星级（4/5/6）
SHOW_TYPE = 0              # 1=显示武器类型，0=不显示
```

#### 方式二：交互模式
将 `TARGET_WEAPON` 设为空字符串，程序将进入交互模式：
```
武器刷取分析工具
目标武器: 未设置（将进入交互模式）
...
请输入武器名称(输入q退出): 宏愿
```

## 📝 数据格式要求

### Excel文件结构：
- **Sheet1**：武器基础信息表
  - 必须包含列：`武器名称`、`第一词条`、`第二词条`、`第三词条`、`武器类型`、`武器星级`
- **其他Sheet**：各地图词条表
  - 必须包含列：`第一词条`、`第二词条`、`第三词条`
  - 每个Sheet代表一个地图

### 示例数据：
| 武器名称 | 第一词条 | 第二词条 | 第三词条 | 武器类型 | 武器星级 |
|----------|----------|----------|----------|----------|----------|
| 宏愿     | 攻击提升 | 爆伤提升 | 暴击提升 | 双手剑   | 6        |

## 📊 输出示例

```
武器刷取分析工具
目标武器: 宏愿
显示武器星级: 是
最低显示星级: 5星
显示武器类型: 否
============================================================

分析目标武器: 宏愿
武器信息: 攻击提升 | 爆伤提升 | 暴击提升
武器类型: 双手剑 | 星级: 6
------------------------------------------------------------
可在以下 3 个地图刷取: 地图A, 地图B, 地图C

【地图A】
  攻击+暴击       爆伤提升: 6星武器A, 5星武器B, 5星武器C
  攻击+精准       爆伤提升: 6星武器D, 5星武器E
```

## 🔄 更新日志

### v1.0 (2026-02-03)
- ✅ 初始版本发布
- ✅ 支持基本武器分析功能
- ✅ 支持多地图数据加载
- ✅ 实现交互式查询模式

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

感谢《终末地》游戏社区提供的武器数据支持。

---

# Endfield Weapon Matrix Analysis Tool

## 📖 Introduction

A tool for analyzing weapon drop probabilities in the game "Endfield". By analyzing weapon trait combinations, it helps players find optimal farming strategies for specific weapons that share traits with other weapons.

## ✨ Features

- 🔍 **Weapon Query Analysis**: Input target weapon name to analyze its farmability across maps
- 🗺️ **Multi-map Support**: Automatically identifies and loads all map data sheets
- ⭐ **Star Rating Filter**: Filter results by minimum star rating (4/5/6 stars)
- 🎯 **Trait Combination Analysis**:
  - Fixed 2nd trait analysis
  - Fixed 3rd trait analysis
  - Display other weapons sharing traits
- 📊 **Data Visualization**: Clear display of weapon trait relationships
- 🖥️ **Interactive Mode**: Supports command-line interactive operation

## ⚙️ Requirements

- Python 3.8+
- Dependencies:
  - pandas
  - openpyxl
  - numpy (optional)

## 🔧 Installation & Usage

### Quick Start

1. **Clone Repository**
```bash
git clone [repository-url]
cd weapon-analyzer
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run Program**
```bash
python src/weapon_analyzer.py
```

### Configuration

Two usage modes supported:

#### Method 1: Direct Configuration (Edit code)
```python
# Set in configuration section at top of code
TARGET_WEAPON = "宏愿"     # Target weapon name
SHOW_STAR = 1              # 1=Show star rating, 0=Hide
MIN_STAR = 5               # Minimum star rating to display (4/5/6)
SHOW_TYPE = 0              # 1=Show weapon type, 0=Hide
```

#### Method 2: Interactive Mode
Set `TARGET_WEAPON` to empty string to enter interactive mode:
```
武器刷取分析工具
目标武器: 未设置（将进入交互模式）
...
请输入武器名称(输入q退出): 宏愿
```

## 📝 Data Format Requirements

### Excel File Structure:
- **Sheet1**: Weapon basic information table
  - Required columns: `武器名称`, `第一词条`, `第二词条`, `第三词条`, `武器类型`, `武器星级`
- **Other Sheets**: Map trait tables
  - Required columns: `第一词条`, `第二词条`, `第三词条`
  - Each sheet represents one map

### Example Data:
| 武器名称 | 第一词条 | 第二词条 | 第三词条 | 武器类型 | 武器星级 |
|----------|----------|----------|----------|----------|----------|
| 宏愿     | 攻击提升 | 爆伤提升 | 暴击提升 | 双手剑   | 6        |

## 📊 Output Example

```
武器刷取分析工具
目标武器: 宏愿
显示武器星级: 是
最低显示星级: 5星
显示武器类型: 否
============================================================

分析目标武器: 宏愿
武器信息: 攻击提升 | 爆伤提升 | 暴击提升
武器类型: 双手剑 | 星级: 6
------------------------------------------------------------
可在以下 3 个地图刷取: 地图A, 地图B, 地图C

【地图A】
  攻击+暴击       爆伤提升: 6星武器A, 5星武器B, 5星武器C
  攻击+精准       爆伤提升: 6星武器D, 5星武器E
```

## 🔄 Changelog

### v1.0 (2026-02-03)
- ✅ Initial version released
- ✅ Basic weapon analysis functionality
- ✅ Multi-map data loading support
- ✅ Interactive query mode implemented

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## 🙏 Acknowledgments

Thanks to the Endfield game community for providing weapon data support.