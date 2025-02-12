# tsr/models/isosurface.py
import torch
import numpy as np
from skimage.measure import marching_cubes  # Using scikit-image's marching_cubes

class MarchingCubeHelper:
    def __init__(self, resolution, level=0.5):
        """
        Initialize the helper with the desired resolution and isosurface level.
        Assumes a cubic volume with coordinates ranging from -1 to 1.
        Also computes a grid of vertices covering the volume.
        """
        self.resolution = resolution
        self.level = level
        # Define the coordinate range for the grid.
        self.points_range = [-1.0, 1.0]
        # Compute spacing for the marching cubes grid.
        self.spacing = ((self.points_range[1] - self.points_range[0]) / (resolution - 1),) * 3

        # Compute a grid of vertices covering the volume.
        x = np.linspace(self.points_range[0], self.points_range[1], resolution)
        y = np.linspace(self.points_range[0], self.points_range[1], resolution)
        z = np.linspace(self.points_range[0], self.points_range[1], resolution)
        grid = np.stack(np.meshgrid(x, y, z, indexing='ij'), axis=-1)  # shape (res, res, res, 3)
        self.grid_vertices = torch.tensor(grid.reshape(-1, 3), dtype=torch.float32)

    def __call__(self, density):
        """
        Run marching cubes on the provided density volume.
        :param density: A torch.Tensor or numpy array representing the density volume.
                        Expected shape: (resolution, resolution, resolution), but may come with extra singleton dimensions
                        or as a flattened 1D array of size resolution^3.
        :return: (verts, faces) where:
            verts is a torch.FloatTensor of shape (num_verts, 3)
            faces is a torch.LongTensor of shape (num_faces, 3)
        """
        # Convert density to a numpy array if needed.
        if isinstance(density, torch.Tensor):
            density_np = density.cpu().numpy()
        else:
            density_np = density

        # Remove extra singleton dimensions.
        density_np = np.squeeze(density_np)
        
        # If the density is 1D and its size matches resolution^3, reshape it.
        if density_np.ndim == 1 and density_np.size == self.resolution ** 3:
            density_np = density_np.reshape((self.resolution, self.resolution, self.resolution))
        
        if density_np.ndim != 3:
            raise ValueError(f"After processing, density volume must be 3D, got shape {density_np.shape}")

        # Run scikit-image's marching_cubes.
        verts, faces, normals, values = marching_cubes(
            volume=density_np, level=self.level, spacing=self.spacing
        )
        # Adjust vertex positions: add the lower bound of points_range.
        verts += self.points_range[0]
        # Convert outputs to torch tensors with positive strides.
        verts = torch.tensor(verts.copy(), dtype=torch.float32)
        faces = torch.tensor(faces.copy(), dtype=torch.int64)
        return verts, faces
