
'''
utils.py

Some utility functions

'''

import scipy.ndimage as nd
import scipy.io as io
import matplotlib

from . import params
from .params import getDeviceType
from .models import GanGeneratedModel

if getDeviceType() != 'cpu':
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
import skimage.measure as sk
import matplotlib.gridspec as gridspec
import numpy as np
from torch.utils import data
import torch
import os


def getVoxelFromMat(path, cube_len=64):
    if cube_len == 32:
        voxels = io.loadmat(path)['instance'] # 30x30x30
        voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))

    else:
        voxels = io.loadmat(path)['instance'] # 30x30x30
        voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))
        voxels = nd.zoom(voxels, (2, 2, 2), mode='constant', order=0)
    # print (voxels.shape)
    return voxels


def getVFByMarchingCubes(voxels, threshold=0.5):
    v, f = sk.marching_cubes_classic(voxels, level=threshold)
    return v, f


def plotVoxelVisdom(voxels, visdom, title):
    v, f = getVFByMarchingCubes(voxels)
    visdom.mesh(X=v, Y=f, opts=dict(opacity=0.5, title=title))


def SavePloat_Voxels(voxels, path, iteration):
    voxels = voxels[:8].__ge__(0.5)
    fig = plt.figure(figsize=(32, 16))
    gs = gridspec.GridSpec(2, 4)
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(voxels):
        x, y, z = sample.nonzero()
        ax = plt.subplot(gs[i], projection='3d')
        ax.scatter(x, y, z, zdir='z', c='red')
        ax.set_xticklabels([])
        ax.set_yticklabels([])

    full_image_name = os.path.basename(path) + '/{}'.format(str(iteration).zfill(3))
    full_image_path = path + '/{}.png'.format(str(iteration).zfill(3)) # Path with iteration
    plt.savefig(full_image_path, bbox_inches='tight')
    plt.close()

    try:
        get_img = GanGeneratedModel.objects.get(name=full_image_name)
    except GanGeneratedModel.DoesNotExist:
        # create new records
        new_img = GanGeneratedModel()
        new_img.name = full_image_name
        new_img.generated_Img.delete()
        new_img.generated_Img.save(full_image_path, open(full_image_path, 'rb'))
    else:
        # update existing
        get_img.generated_Img.delete()
        get_img.generated_Img.save(full_image_path, open(full_image_path, 'rb'))

    # Save to db only if it doesn't already exist
    # if not GanGeneratedModel.objects.filter(name=full_image_name).exists():
    #     ggm = GanGeneratedModel()
    #     ggm.name = full_image_name
    #     ggm.generated_Img.save(full_image_path, open(full_image_path, 'rb'))


class ShapeNetDataset(data.Dataset):

    def __init__(self, root, args, train_or_val="train"):

        self.root = root
        self.listdir = os.listdir(self.root)

        data_size = len(self.listdir)
        self.listdir = self.listdir[0:int(data_size)]
        
        print ('data_size =', len(self.listdir))
        self.args = args

    def __getitem__(self, index):
        with open(self.root + self.listdir[index], "rb") as f:
            volume = np.asarray(getVoxelFromMat(f, params.cube_len), dtype=np.float32)
            # print (volume.shape)
        return torch.FloatTensor(volume)

    def __len__(self):
        return len(self.listdir)


def generateZ(batch):

    if params.z_dis == "norm":
        Z = torch.Tensor(batch, params.z_dim).normal_(0, 0.33).to(params.device)
    elif params.z_dis == "uni":
        Z = torch.randn(batch, params.z_dim).to(params.device).to(params.device)
    else:
        print("z_dist is not normal or uniform")

    return Z
