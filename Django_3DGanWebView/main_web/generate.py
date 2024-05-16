'''
generate.py

Apply trained 3d gan models and generate 3dgan models
'''
import pickle
import visdom
import os
import torch
from .utils import *
from .model import net_G, net_D
from .models import Voxel
from .params import *


def generate(model_name='dcgan_pretrained', logs='first_test', obj_count=9):
    print('Entering Generate')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    image_saved_path = params.output_dir + '/' + model_name + '/' + logs + '/test_outputs'
    if not os.path.exists(image_saved_path):
        os.makedirs(image_saved_path)

    save_file_path = params.output_dir + '/' +model_name
    pretrained_file_path_G = save_file_path + '/' + logs + '/models/G.pth'
    pretrained_file_path_D = save_file_path + '/' + logs + '/models/D.pth'

    print(pretrained_file_path_G)

    D = net_D()
    G = net_G()

    if not torch.cuda.is_available():
        G.load_state_dict(torch.load(pretrained_file_path_G, map_location={'cuda:0': 'cpu'}))
        D.load_state_dict(torch.load(pretrained_file_path_D, map_location={'cuda:0': 'cpu'}))
    else:
        G.load_state_dict(torch.load(pretrained_file_path_G))
        D.load_state_dict(torch.load(pretrained_file_path_D, map_location={'cuda:0': 'cpu'}))

    print('visualizing model')


    G.to(device)
    D.to(device)
    G.eval()
    D.eval()


    for i in range(obj_count):
        sample_name = 'tester_' + str(i)

        z = generateZ(1)

        generated = G(z)
        samples = generated.unsqueeze(dim=0).detach().cpu().numpy()

        save_sample_to_db(samples, sample_name)

        y_prob = D(generated)
        y_real = torch.ones_like(y_prob)

        # visualization
        SavePloat_Voxels(samples, image_saved_path, sample_name)  # norm_

    return True

# sends data to visdom server
def render_generated():
    vis = visdom.Visdom()

    all_voxels = read_all_samples_from_db()

    # Accessing name and data columns of each instance
    for sample in all_voxels:
        name = sample.model
        data = pickle.loads(sample.data)
        plotVoxelVisdom(data[0, :], vis, name)


def save_sample_to_db(data_sample, sample_name):
    # Serialize using pickle
    serialized_data_sample = pickle.dumps(data_sample)

    check_present = Voxel.objects.filter(model=sample_name).exists()

    if not check_present:
        # create new
        voxel = Voxel()
        voxel.model=sample_name
        voxel.data=serialized_data_sample
        voxel.save()

    else:
        # update
        to_upd = Voxel.objects.filter(model=sample_name)
        to_upd.data = serialized_data_sample

def read_all_samples_from_db():
    # Retrieve all voxels from db
    all_voxels = Voxel.objects.all()

    return all_voxels



