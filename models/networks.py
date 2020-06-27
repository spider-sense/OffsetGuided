import logging

import os
import torch
import torch.nn as nn
from models import Hourglass104, Hourglass4Stage

LOG = logging.getLogger(__name__)


def load_model(model, ckpt_path, optimizer=None, drop_layers=True,
               resume_optimizer=True, optimizer2cuda=True):
    """
    Load pre-trained model and optimizer checkpoint.

    Args:
        model: 
        ckpt_path: 
        optimizer: 
        drop_layers (bool): drop pre-trained params of the output layers, etc 
        resume_optimizer: 
        optimizer2cuda (bool): move optimizer statues to cuda
    """

    start_epoch = 0
    if not os.path.isfile(ckpt_path):
        print(f'WARRRING!!! \t Current checkpoint file {ckpt_path} DOSE NOT exist!!')
        print("############# No pre-trained parameters are loaded! #############\n"
              "######## Please make sure you initialize the model randomly! #####")
        # return without loading
        return model, None, start_epoch

    checkpoint = torch.load(ckpt_path, map_location=torch.device('cpu'))
    LOG.info('Loading pre-trained model %s, checkpoint at epoch %d', ckpt_path,
             checkpoint['epoch'])
    state_dict_ = checkpoint['model_state_dict']  # type: dict

    from collections import OrderedDict
    state_dict = OrderedDict()  # loaded pre-trained model weight

    # convert parallel/distributed model to single model
    for k, v in state_dict_.items():  # Fixme: keep consistent with our model
        if ('before_regression' in k or 'offset' in k) and drop_layers:  #
            continue
        if k.startswith('module') and not k.startswith('module_list'):
            name = k[7:]  # remove prefix 'module.'
            # name = 'module.' + k  # add prefix 'module.'
            state_dict[name] = v
        else:
            name = k
            state_dict[name] = v
    model_state_dict = model.state_dict()  # newly built model

    # check loaded parameters and created model parameters
    msg = 'If you see this, your model does not fully load the ' + \
          'pre-trained weight. Please make sure ' + \
          'you have correctly specified the output or regression layers.'
    for k in state_dict:
        if k in model_state_dict:
            if state_dict[k].shape != model_state_dict[k].shape:
                LOG.debug(
                    'Skip loading pre-trained parameter %s, current model '
                    'required shape %s, loaded shape %s. %s',
                    k, model_state_dict[k].shape, state_dict[k].shape, msg)
                state_dict[k] = model_state_dict[k]  # fix bad params
        else:
            LOG.debug('Drop pre-trained parameter %s which current model dose '
                      'not have. %s', k, msg)
    for k in model_state_dict:
        if not (k in state_dict):
            LOG.debug('No param in pre-trained model %s. %s', k, msg)
            state_dict[k] = model_state_dict[k]  # append missing params
    model.load_state_dict(state_dict, strict=False)
    print('Network weights have been resumed from checkpoint.')

    # resume optimizer parameters
    if optimizer is not None and resume_optimizer:
        if 'optimizer_state_dict' in checkpoint:
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

            # Here, we must convert the resumed state data of optimizer to gpu.
            # In this project, we use map_location to map the state tensors to cpu.
            # In the training process, we need cuda version of state tensors,
            # so we have to convert them to gpu.
            if torch.cuda.is_available() and optimizer2cuda:
                for state in optimizer.state.values():
                    for k, v in state.items():
                        if torch.is_tensor(v):
                            state[k] = v.cuda()

            start_epoch = checkpoint['epoch'] + 1
            # param_group['lr'] will be instead set in a separate fun: adjust_learning_rate()
            print('Optimizer has been resumed from the checkpoint at epoch {}.'
                  .format(start_epoch - 1))
        else:
            print('No pre-trained optimizer weights in current checkpoint.')

    if optimizer is not None and resume_optimizer:
        return model, optimizer, start_epoch
    else:
        return model, None, start_epoch,


def save_model(path, epoch, train_loss, model, optimizer=None):
    from apex.parallel import DistributedDataParallel
    if isinstance(model, (torch.nn.DataParallel, DistributedDataParallel)):
        state_dict = model.module.state_dict()  # remove prefix 'module.'
    else:
        state_dict = model.state_dict()

    data = {'epoch': epoch,
            'train_loss': train_loss,
            'model_state_dict': state_dict}
    if not (optimizer is None):
        data['optimizer_state_dict'] = optimizer.state_dict()
    torch.save(data, path)


def initialize_weights(model):
    """Initialize model randomly.

    Args:
        model (nn.Module): input Pytorch model

    Returns: initialized model

    """
    for m in model.modules():
        if isinstance(m, nn.Conv2d):
            m.weight.data.normal_(0, 0.001)
            if m.bias is not None:  # bias are not used when we use BN layers
                m.bias.data.zero_()

        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()

        elif isinstance(m, nn.Linear):
            # torch.nn.init.normal_(m.weight.data, 0, 0.01)
            m.weight.data.normal_(0, 0.01)
            m.bias.data.zero_()
    return model


class NetworkWrap(torch.nn.Module):
    """Wrap the basenet and headnets into a single module."""
    def __init__(self, basenet, headnets):
        super(NetworkWrap, self).__init__()
        self.basenet = basenet
        # Notice!  subnets in list or dict must be warped
        # by ModuleList to register trainable params
        self.headnets = torch.nn.ModuleList(headnets)

    def forward(self, img_tensor):
        # Batch will be divided and Parallel Model
        # will call this forward on every GPU
        feature_tuple = self.basenet(img_tensor)
        head_outputs = [hn(feature_tuple) for hn in self.headnets]

        return head_outputs


def basenet_factory(basenet_name):
    """
    Args:
        basenet_name:

    Returns:
    tuple: BaseNetwork, n_stacks, stride, oup_dim

    """
    assert basenet_name in ['hourglass104', 'hourglass4stage'], \
        f'{basenet_name} is not implemented.'

    if 'hourglass104' in basenet_name:
        model = Hourglass104(None, 2)
        return model, 2, 4, 256

    if 'hourglass4stage' in basenet_name:
        class IMHNOpt:
            nstack = 4  # stacked number of hourglass
            hourglass_inp_dim = 256
            increase = 128  # increased channels once down-sampling through networks
        net_opt = IMHNOpt()
        out_dim = 50
        raise Exception('Unknown base network in {}'.format(basenet_name))
