import open3d as o3d
import numpy as np
import os
import glob
from pathlib import Path
import argparse


def pointcloud_to_stl(npy_file_path, output_path, method="poisson", radius=0.1):
    """
    从点云数据(.npy)重建STL网格并保存
    
    Args:
        npy_file_path (str): .npy点云文件路径
        output_path (str): 输出STL文件路径
        method (str): 重建方法: "ball_pivoting", "alpha_shape", "poisson"
        radius (float): 重建参数（球半径或alpha值）
    """
    try:
        # 读取点云数据
        point_cloud_data = np.load(npy_file_path)
        
        # 检查数据格式
        if point_cloud_data.shape[1] >= 3:
            # 提取点坐标（前3列）
            points = point_cloud_data[:, :3]
            
            # 如果有法向量（后3列），也提取出来
            normals = None
            if point_cloud_data.shape[1] >= 6:
                normals = point_cloud_data[:, 3:6]
        else:
            print(f"错误: {npy_file_path} 数据格式不正确，需要至少3列坐标数据")
            return False
        
        # 创建Open3D点云对象
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        
        if normals is not None:
            pcd.normals = o3d.utility.Vector3dVector(normals)
        else:
            # 如果没有法向量，计算法向量
            pcd.estimate_normals()
        
        print(f"点云数据形状: {point_cloud_data.shape}")
        print(f"点数量: {len(points)}")
        
        # 根据选择的方法重建网格
        mesh = None
        
        if method == "ball_pivoting":
            # 球旋转算法
            radii = [radius, radius * 2, radius * 4]
            mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
                pcd, o3d.utility.DoubleVector(radii))
            
        elif method == "alpha_shape":
            # Alpha形状算法
            mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, radius)
            
        elif method == "poisson":
            # 泊松重建
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                pcd, depth=9, width=0, scale=1.1, linear_fit=False)
            
        else:
            print(f"不支持的重建方法: {method}")
            return False
        
        # 检查重建结果
        if not mesh.has_vertices() or not mesh.has_triangles():
            print(f"警告: 无法从点云重建有效网格，尝试其他参数")
            return False
        
        # 清理网格（移除重复顶点、面等）
        mesh.remove_duplicated_vertices()
        mesh.remove_duplicated_triangles()
        mesh.remove_degenerate_triangles()
        mesh.remove_unreferenced_vertices()
        
        # 计算法向量
        mesh.compute_vertex_normals()
        
        # 保存为STL文件
        o3d.io.write_triangle_mesh(output_path, mesh)
        
        print(f"成功处理: {npy_file_path} -> {output_path}")
        print(f"重建网格 - 顶点数: {len(mesh.vertices)}, 面数: {len(mesh.triangles)}")
        print(f"重建方法: {method}")
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"处理文件 {npy_file_path} 时出错: {str(e)}")
        return False


def process_directory(input_dir, output_dir, method="poisson", radius=0.1):
    """
    处理目录中的所有.npy点云文件
    
    Args:
        input_dir (str): 输入目录路径
        output_dir (str): 输出目录路径
        method (str): 重建方法
        radius (float): 重建参数
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 查找所有.npy文件
    npy_files = []
    for file in os.listdir(input_dir):
        if file.lower().endswith('.npy'):
            npy_files.append(os.path.join(input_dir, file))
    
    if not npy_files:
        print(f"在目录 {input_dir} 中没有找到.npy文件")
        return
    
    print(f"找到 {len(npy_files)} 个点云文件")
    
    success_count = 0
    for npy_file in npy_files:
        # 生成输出文件名
        filename = Path(npy_file).stem
        output_file = os.path.join(output_dir, f"{filename}.stl")
        
        # 处理文件
        if pointcloud_to_stl(npy_file, output_file, method, radius):
            success_count += 1
    
    print(f"处理完成: {success_count}/{len(npy_files)} 个文件成功转换")


def main():
    parser = argparse.ArgumentParser(description="从点云数据(.npy)重建STL网格")
    parser.add_argument("--input_dir", type=str, default="output/pointcloud", 
                       help="输入目录路径 (默认: output/pointcloud)")
    parser.add_argument("--output_dir", type=str, default="output/raw", 
                       help="输出目录路径 (默认: output/raw)")
    parser.add_argument("--method", type=str, default="poisson", 
                       choices=["ball_pivoting", "alpha_shape", "poisson"], 
                       help="重建方法 (默认: poisson)")
    parser.add_argument("--radius", type=float, default=0.1, 
                       help="重建参数半径/alpha值 (默认: 0.1)")
    parser.add_argument("--subdir", type=str, choices=["feet", "insoles"], 
                       help="只处理指定的子目录")
    parser.add_argument("--main_dir_only", action="store_true", 
                       help="只处理主目录，不处理子目录")
    
    args = parser.parse_args()
    
    if args.subdir:
        # 只处理指定的子目录
        input_subdir = os.path.join(args.input_dir, args.subdir)
        output_subdir = os.path.join(args.output_dir, args.subdir)
        
        if os.path.exists(input_subdir):
            print(f"\n处理子目录: {args.subdir}")
            process_directory(input_subdir, output_subdir, args.method, args.radius)
        else:
            print(f"子目录不存在: {input_subdir}")
    elif args.main_dir_only:
        # 只处理主目录
        process_directory(args.input_dir, args.output_dir, args.method, args.radius)
    else:
        # 默认处理所有子目录
        for subdir in ["feet", "insoles"]:
            input_subdir = os.path.join(args.input_dir, subdir)
            output_subdir = os.path.join(args.output_dir, subdir)
            
            if os.path.exists(input_subdir):
                print(f"\n处理子目录: {subdir}")
                process_directory(input_subdir, output_subdir, args.method, args.radius)
            else:
                print(f"子目录不存在: {input_subdir}")


if __name__ == "__main__":
    main()
