# STL到点云转换工具 - 使用总结

## 快速开始

1. **安装依赖**：
   ```bash
   pip install open3d numpy
   ```

2. **准备数据**：
   - 将STL文件放在 `data/raw/feet/` 目录中
   - 将STL文件放在 `data/raw/insoles/` 目录中

3. **运行转换**：
   ```bash
   python process/stl_to_pointcloud.py
   ```

## 默认行为

脚本默认会：
- 自动处理 `data/raw/feet/` 中的所有STL文件，转换到 `data/pointcloud/feet/`
- 自动处理 `data/raw/insoles/` 中的所有STL文件，转换到 `data/pointcloud/insoles/`
- 每个STL文件生成对应的.npy文件（包含点云坐标和法向量）

## 常用命令

```bash
# 默认处理所有子目录
python process/stl_to_pointcloud.py

# 只处理feet目录
python process/stl_to_pointcloud.py --subdir feet

# 只处理insoles目录
python process/stl_to_pointcloud.py --subdir insoles

# 自定义采样点数量
python process/stl_to_pointcloud.py --num_points 1024

# 使用泊松盘采样
python process/stl_to_pointcloud.py --sampling_method poisson
```

## 输出格式

每个.npy文件包含：
- 形状: (N, 6)，其中N是采样点数量（默认2048）
- 前3列: 点的3D坐标 (x, y, z)
- 后3列: 法向量 (nx, ny, nz)

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

## 注意事项

- 确保STL文件格式正确
- 脚本会自动创建输出目录
- 如果STL文件无效，会跳过并继续处理其他文件
- 建议采样点数量在1024-4096之间
