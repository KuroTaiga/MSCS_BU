# My implementation of Conjugrate Gradient Descent
# This is meant as a optimizer class similar to aviable ones on pytorch
# Written by Jiankun Dong in April 2024, all rights reserved
# used scipy and pytorch documents, as well as chatgpt for help

import torch
from torch.optim.optimizer import Optimizer, required

class CGD(Optimizer):
    def __init__(self, params, lr=required):
        if lr is not required and lr < 0.0:
            raise ValueError("Invalid learning rate: {}".format(lr))
        defaults = dict(lr=lr)
        super(CGD, self).__init__(params, defaults)

    def step(self, closure=None):
        """Performs a single optimization step.
        
        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                                          and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad.data
                if grad.is_sparse:
                    raise RuntimeError('ConjugateGradientDescent does not support sparse gradients')

                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    state['step'] = 0
                    state['old_grad'] = torch.zeros_like(p.data)
                    state['search_direction'] = -grad

                old_grad = state['old_grad']
                search_direction = state['search_direction']
                beta = grad.dot(grad) / old_grad.dot(old_grad)
                search_direction = -grad + beta * search_direction

                # Update parameters
                p.data.add_(search_direction, alpha=group['lr'])

                # Update state
                state['old_grad'] = grad
                state['search_direction'] = search_direction
                state['step'] += 1

        return loss
