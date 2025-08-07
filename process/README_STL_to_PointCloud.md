# STL到点云转换工具

这个工具使用Open3D库从STL文件中采样点云数据，并保存为.npy格式，方便后续的机器学习处理。

## 功能特点

- 支持从STL文件中均匀采样或泊松盘采样点云
- 自动计算并保存法向量信息
- 支持批量处理多个STL文件
- 自动处理子目录结构
- 可自定义采样点数量

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

默认处理所有子目录（推荐）：
```bash
python process/stl_to_pointcloud.py
```

只处理feet目录：
```bash
python process/stl_to_pointcloud.py --subdir feet
```

只处理insoles目录：
```bash
python process/stl_to_pointcloud.py --subdir insoles
```

只处理主目录：
```bash
python process/stl_to_pointcloud.py --main_dir_only
```

### 高级用法

自定义参数：
```bash
python process/stl_to_pointcloud.py --num_points 1024 --sampling_method poisson
```

### 参数说明

- `--input_dir`: 输入目录路径（默认: data/raw）
- `--output_dir`: 输出目录路径（默认: data/pointcloud）
- `--num_points`: 采样点数量（默认: 2048）
- `--sampling_method`: 采样方法，可选 "uniform" 或 "poisson"（默认: uniform）
- `--subdir`: 只处理指定的子目录，可选 "feet" 或 "insoles"
- `--main_dir_only`: 只处理主目录，不处理子目录

## 目录结构

```
data/
├── raw/           # 原始STL文件
│   ├── feet/      # 脚部STL文件
│   └── insoles/   # 鞋垫STL文件
└── pointcloud/    # 转换后的点云文件
    ├── feet/      # 脚部点云文件（.npy格式）
    └── insoles/   # 鞋垫点云文件（.npy格式）
```

## 输出格式

每个.npy文件包含以下数据：
- 形状: (N, 6)，其中N是采样点数量
- 前3列: 点的3D坐标 (x, y, z)
- 后3列: 法向量 (nx, ny, nz)

## 示例

运行示例脚本：
```bash
python process/example_usage.py
```

## 注意事项

1. 确保STL文件格式正确且包含有效的几何数据
2. 采样点数量建议在1024-4096之间，根据您的具体需求调整
3. 均匀采样适合大多数情况，泊松盘采样可能在某些特殊情况下效果更好
4. 处理大量文件时，建议先在小数据集上测试

## 错误处理

脚本会自动处理以下情况：
- 无效的STL文件
- 缺少顶点数据的文件
- 文件读取错误
- 输出目录不存在（自动创建）

如果遇到问题，请检查：
1. STL文件是否完整且格式正确
2. 是否有足够的磁盘空间
3. Open3D库是否正确安装
