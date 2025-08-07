import open3d as o3d
import numpy as np
import os
import random
from pathlib import Path
import argparse


def generate_random_sphere(radius_range=(0.5, 2.0), resolution=20):
    """生成随机球体"""
    radius = random.uniform(*radius_range)
    mesh = o3d.geometry.TriangleMesh.create_sphere(radius=radius, resolution=resolution)
    return mesh


def generate_random_cube(size_range=(1.0, 3.0)):
    """生成随机立方体"""
    size = random.uniform(*size_range)
    mesh = o3d.geometry.TriangleMesh.create_box(width=size, height=size, depth=size)
    return mesh


def generate_random_cylinder(radius_range=(0.3, 1.0), height_range=(1.0, 3.0), resolution=20):
    """生成随机圆柱体"""
    radius = random.uniform(*radius_range)
    height = random.uniform(*height_range)
    mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=height, resolution=resolution)
    return mesh


def generate_random_torus(radius_range=(1.0, 2.0), tube_radius_range=(0.2, 0.5), radial_resolution=30, tubular_resolution=20):
    """生成随机环面"""
    torus_radius = random.uniform(*radius_range)
    tube_radius = random.uniform(*tube_radius_range)
    mesh = o3d.geometry.TriangleMesh.create_torus(torus_radius=torus_radius, tube_radius=tube_radius, radial_resolution=radial_resolution, tubular_resolution=tubular_resolution)
    return mesh


def generate_random_cone(radius_range=(0.5, 1.5), height_range=(1.0, 3.0), resolution=20):
    """生成随机圆锥体"""
    radius = random.uniform(*radius_range)
    height = random.uniform(*height_range)
    mesh = o3d.geometry.TriangleMesh.create_cone(radius=radius, height=height, resolution=resolution)
    return mesh


def generate_random_octahedron(size_range=(1.0, 2.0)):
    """生成随机八面体"""
    size = random.uniform(*size_range)
    mesh = o3d.geometry.TriangleMesh.create_octahedron(radius=size)
    return mesh


def generate_random_icosahedron(size_range=(1.0, 2.0)):
    """生成随机二十面体"""
    size = random.uniform(*size_range)
    mesh = o3d.geometry.TriangleMesh.create_icosahedron(radius=size)
    return mesh


def generate_random_shape():
    """生成随机几何形状"""
    shapes = [
        generate_random_torus,
        generate_random_cone,
        generate_random_octahedron,
        generate_random_icosahedron
    ]
    
    # 随机选择一个形状生成函数
    shape_func = random.choice(shapes)
    mesh = shape_func()
    
    # 随机旋转
    angle_x = random.uniform(0, 2 * np.pi)
    angle_y = random.uniform(0, 2 * np.pi)
    angle_z = random.uniform(0, 2 * np.pi)
    
    # 创建旋转矩阵
    R = mesh.get_rotation_matrix_from_xyz((angle_x, angle_y, angle_z))
    mesh.rotate(R, center=(0, 0, 0))
    
    # 随机平移
    translation = np.random.uniform(-2, 2, 3)
    mesh.translate(translation)
    
    return mesh


def generate_multiple_shapes(num_shapes=5, output_dir="data/raw"):
    """生成多个随机形状的STL文件"""
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"生成 {num_shapes} 个随机形状的STL文件...")
    
    for i in range(num_shapes):
        # 生成随机形状
        mesh = generate_random_shape()
        
        # 确保网格是有效的
        mesh.compute_vertex_normals()
        
        # 生成文件名
        filename = f"random_shape_{i+1:03d}.stl"
        filepath = os.path.join(output_dir, filename)
        
        # 保存STL文件
        success = o3d.io.write_triangle_mesh(filepath, mesh)
        
        if success:
            print(f"✓ 生成: {filename}")
        else:
            print(f"✗ 失败: {filename}")
    
    print(f"\n完成！生成了 {num_shapes} 个STL文件到 {output_dir}")


def generate_for_subdirs(num_per_dir=3):
    """为feet和insoles子目录生成随机STL文件"""
    
    subdirs = ["feet", "insoles"]
    
    for subdir in subdirs:
        output_dir = os.path.join("data/raw", subdir)
        print(f"\n为 {subdir} 目录生成 {num_per_dir} 个随机形状...")
        generate_multiple_shapes(num_per_dir, output_dir)


def main():
    parser = argparse.ArgumentParser(description="生成随机形状的STL文件")
    parser.add_argument("--num_shapes", type=int, default=10, 
                       help="生成的文件数量 (默认: 5)")
    parser.add_argument("--output_dir", type=str, default="data/raw", 
                       help="输出目录 (默认: data/raw)")
    parser.add_argument("--subdirs", action="store_true", 
                       help="为feet和insoles子目录生成文件")
    parser.add_argument("--num_per_subdir", type=int, default=3, 
                       help="每个子目录生成的文件数量 (默认: 3)")
    
    args = parser.parse_args()
    
    if args.subdirs:
        generate_for_subdirs(args.num_per_subdir)
    else:
        generate_multiple_shapes(args.num_shapes, args.output_dir)


if __name__ == "__main__":
    main()
