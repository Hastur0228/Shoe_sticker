#!/usr/bin/env python3
"""
测试目录对应关系的脚本
"""

import os
import glob
from pathlib import Path

def test_directory_mapping():
    """测试目录对应关系"""
    
    print("=== 测试目录对应关系 ===\n")
    
    # 检查输入目录
    raw_feet_dir = "data/raw/feet"
    raw_insoles_dir = "data/raw/insoles"
    
    # 检查输出目录
    pointcloud_feet_dir = "data/pointcloud/feet"
    pointcloud_insoles_dir = "data/pointcloud/insoles"
    
    print("输入目录检查:")
    if os.path.exists(raw_feet_dir):
        stl_files = glob.glob(os.path.join(raw_feet_dir, "*.stl"))
        stl_files.extend(glob.glob(os.path.join(raw_feet_dir, "*.STL")))
        print(f"  ✓ {raw_feet_dir}: 找到 {len(stl_files)} 个STL文件")
        for file in stl_files[:5]:  # 只显示前5个文件
            print(f"    - {Path(file).name}")
        if len(stl_files) > 5:
            print(f"    ... 还有 {len(stl_files) - 5} 个文件")
    else:
        print(f"  ✗ {raw_feet_dir}: 目录不存在")
    
    if os.path.exists(raw_insoles_dir):
        stl_files = glob.glob(os.path.join(raw_insoles_dir, "*.stl"))
        stl_files.extend(glob.glob(os.path.join(raw_insoles_dir, "*.STL")))
        print(f"  ✓ {raw_insoles_dir}: 找到 {len(stl_files)} 个STL文件")
        for file in stl_files[:5]:  # 只显示前5个文件
            print(f"    - {Path(file).name}")
        if len(stl_files) > 5:
            print(f"    ... 还有 {len(stl_files) - 5} 个文件")
    else:
        print(f"  ✗ {raw_insoles_dir}: 目录不存在")
    
    print("\n输出目录检查:")
    if os.path.exists(pointcloud_feet_dir):
        npy_files = glob.glob(os.path.join(pointcloud_feet_dir, "*.npy"))
        print(f"  ✓ {pointcloud_feet_dir}: 找到 {len(npy_files)} 个NPY文件")
        for file in npy_files[:5]:  # 只显示前5个文件
            print(f"    - {Path(file).name}")
        if len(npy_files) > 5:
            print(f"    ... 还有 {len(npy_files) - 5} 个文件")
    else:
        print(f"  ✗ {pointcloud_feet_dir}: 目录不存在")
    
    if os.path.exists(pointcloud_insoles_dir):
        npy_files = glob.glob(os.path.join(pointcloud_insoles_dir, "*.npy"))
        print(f"  ✓ {pointcloud_insoles_dir}: 找到 {len(npy_files)} 个NPY文件")
        for file in npy_files[:5]:  # 只显示前5个文件
            print(f"    - {Path(file).name}")
        if len(npy_files) > 5:
            print(f"    ... 还有 {len(npy_files) - 5} 个文件")
    else:
        print(f"  ✗ {pointcloud_insoles_dir}: 目录不存在")
    
    print("\n目录对应关系验证:")
    
    # 验证feet目录对应关系
    if os.path.exists(raw_feet_dir) and os.path.exists(pointcloud_feet_dir):
        raw_files = set([Path(f).stem for f in glob.glob(os.path.join(raw_feet_dir, "*.stl"))])
        raw_files.update([Path(f).stem for f in glob.glob(os.path.join(raw_feet_dir, "*.STL"))])
        npy_files = set([Path(f).stem for f in glob.glob(os.path.join(pointcloud_feet_dir, "*.npy"))])
        
        converted = raw_files.intersection(npy_files)
        not_converted = raw_files - npy_files
        
        print(f"  Feet目录:")
        print(f"    原始STL文件: {len(raw_files)} 个")
        print(f"    已转换NPY文件: {len(converted)} 个")
        if not_converted:
            print(f"    未转换文件: {len(not_converted)} 个")
            for file in list(not_converted)[:3]:
                print(f"      - {file}.stl")
            if len(not_converted) > 3:
                print(f"      ... 还有 {len(not_converted) - 3} 个文件")
    
    # 验证insoles目录对应关系
    if os.path.exists(raw_insoles_dir) and os.path.exists(pointcloud_insoles_dir):
        raw_files = set([Path(f).stem for f in glob.glob(os.path.join(raw_insoles_dir, "*.stl"))])
        raw_files.update([Path(f).stem for f in glob.glob(os.path.join(raw_insoles_dir, "*.STL"))])
        npy_files = set([Path(f).stem for f in glob.glob(os.path.join(pointcloud_insoles_dir, "*.npy"))])
        
        converted = raw_files.intersection(npy_files)
        not_converted = raw_files - npy_files
        
        print(f"  Insoles目录:")
        print(f"    原始STL文件: {len(raw_files)} 个")
        print(f"    已转换NPY文件: {len(converted)} 个")
        if not_converted:
            print(f"    未转换文件: {len(not_converted)} 个")
            for file in list(not_converted)[:3]:
                print(f"      - {file}.stl")
            if len(not_converted) > 3:
                print(f"      ... 还有 {len(not_converted) - 3} 个文件")


if __name__ == "__main__":
    test_directory_mapping()
