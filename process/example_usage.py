#!/usr/bin/env python3
"""
STL到点云转换示例脚本
"""

import subprocess
import sys
import os

def run_stl_conversion():
    """运行STL到点云转换的示例"""
    
    print("=== STL到点云转换示例 ===\n")
    
    # 检查输入目录是否存在
    if not os.path.exists("data/raw"):
        print("错误: data/raw 目录不存在")
        print("请确保您的STL文件放在 data/raw/feet/ 或 data/raw/insoles/ 目录中")
        return
    
    # 示例1: 默认处理所有子目录（推荐）
    print("示例1: 默认处理所有子目录 (feet 和 insoles)")
    print("命令: python process/stl_to_pointcloud.py")
    print("这将从 data/raw/feet/ 转换到 data/pointcloud/feet/")
    print("这将从 data/raw/insoles/ 转换到 data/pointcloud/insoles/")
    print()
    
    try:
        result = subprocess.run([
            sys.executable, "process/stl_to_pointcloud.py"
        ], capture_output=True, text=True)
        
        print("输出:")
        print(result.stdout)
        if result.stderr:
            print("错误:")
            print(result.stderr)
            
    except Exception as e:
        print(f"运行出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 示例2: 只处理feet目录
    print("示例2: 只处理feet目录")
    print("命令: python process/stl_to_pointcloud.py --subdir feet")
    print("这将从 data/raw/feet/ 转换到 data/pointcloud/feet/")
    print()
    
    try:
        result = subprocess.run([
            sys.executable, "process/stl_to_pointcloud.py", 
            "--subdir", "feet"
        ], capture_output=True, text=True)
        
        print("输出:")
        print(result.stdout)
        if result.stderr:
            print("错误:")
            print(result.stderr)
            
    except Exception as e:
        print(f"运行出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 示例3: 只处理insoles目录
    print("示例3: 只处理insoles目录")
    print("命令: python process/stl_to_pointcloud.py --subdir insoles")
    print("这将从 data/raw/insoles/ 转换到 data/pointcloud/insoles/")
    print()
    
    try:
        result = subprocess.run([
            sys.executable, "process/stl_to_pointcloud.py", 
            "--subdir", "insoles"
        ], capture_output=True, text=True)
        
        print("输出:")
        print(result.stdout)
        if result.stderr:
            print("错误:")
            print(result.stderr)
            
    except Exception as e:
        print(f"运行出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 示例4: 自定义参数
    print("示例4: 使用自定义参数")
    print("命令: python process/stl_to_pointcloud.py --num_points 1024 --sampling_method poisson")
    print()
    
    try:
        result = subprocess.run([
            sys.executable, "process/stl_to_pointcloud.py", 
            "--num_points", "1024",
            "--sampling_method", "poisson"
        ], capture_output=True, text=True)
        
        print("输出:")
        print(result.stdout)
        if result.stderr:
            print("错误:")
            print(result.stderr)
            
    except Exception as e:
        print(f"运行出错: {e}")


if __name__ == "__main__":
    run_stl_conversion() 