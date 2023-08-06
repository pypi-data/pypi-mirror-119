.. _examples:

Examples
========

In the following example we will create a forward controller and apply it to the rocketball gym environment.
We will perform retrospective context inference to infer which type of rocket is currently controlled.
Furthermore, we will perform prospective action inference to infer which actions are suitable in order for the rocket to reach a certain target.

Let's start with some imports:

.. code-block:: python

    >>> import numpy as np
    >>> import torch
    >>> import gym
    >>> from reprise.action_inference import ActionInference
    >>> from reprise.context_inference import ContextInference
    >>> from reprise.gym.rocketball.agent import Agent

We want to be able to reproduce this example:

.. code-block:: python

    >>> np.random.seed(123)
    >>> torch.manual_seed(123)  # doctest: +ELLIPSIS
    <torch._C.Generator object at ...>

Set context size which is the number of contexts neurons our neural network will have.
Furthermore set the sizes of an action and an observation, which are 4 and 2 for the rocketball environment, respectively (4 thrusts on each rocket, x and y coordinates).
Since our neural network will be a forward controller, its input size is given by the sum of the context, action, and observation size.
Its output size is determined by the observation size.
We want our neural network to have a hidden size of 8.

.. code-block:: python

    >>> context_size = 2
    >>> action_size = 4
    >>> observation_size = 2
    >>> input_size = context_size + action_size + observation_size
    >>> hidden_size = 8

Now we define our neural network.
In this case, we will use a very simple definition for an LSTM:

.. code-block:: python

    >>> class LSTM(torch.nn.Module):
    ...     def __init__(self, input_size, hidden_size,
    ...                  num_layers, observation_size):
    ...         super(LSTM, self).__init__()
    ...         self.lstm = torch.nn.LSTM(
    ...             input_size=input_size,
    ...             hidden_size=hidden_size,
    ...             num_layers=num_layers)
    ...         self.fc = torch.nn.Linear(hidden_size, observation_size)
    ...
    ...     def forward(self, x, state=None):
    ...         x, state = self.lstm(x, state)
    ...         x = self.fc(x)
    ...         return x, state

We can already create an instance of it together with some initial hidden and cell states.
We create a second pair of hidden and cell states for context inference.
This could also be the time to load saved weights into the model, which we will skip here.

.. code-block:: python

    >>> model = LSTM(input_size, hidden_size, 1, observation_size)
    >>> lstm_h = torch.zeros(1, 1, hidden_size)
    >>> lstm_c = torch.zeros(1, 1, hidden_size)
    >>> lstm_state = [lstm_h, lstm_c]
    >>> lstm_state_ci = [lstm_h.clone(), lstm_c.clone()]

Before we create the action and context inference objects, we need to define proper loss functions.
During context inference, we will compare past predictions with actual past observations.
During action inference, we will compare future predictions with our desired target.
In this example, we assume that the model was trained on deltas of observations.
Therefore, the inputs and outputs of the model are deltas and we need to accumulate the outputs in the loss function for action inference:

.. code-block:: python

    >>> criterion = torch.nn.MSELoss()
    >>>
    >>> def ci_loss(outputs, observations):
    ...     return criterion(torch.cat(outputs, dim=0),
    ...                      torch.cat(observations, dim=0))
    >>>
    >>> def ai_loss(outputs, targets):
    ...     return criterion(torch.cumsum(
    ...         torch.cat(outputs, dim=0), dim=0), targets)

Now we can create an action inference object.
We first define an initial policy and the optimizer which shall be used to optimize this policy.
Together with the action inference loss function, this these objects are passed to the action inference constructor.

.. code-block:: python

    >>> ai_horizon = 10
    >>> policy = torch.rand([ai_horizon, 1, action_size])
    >>> optimizer = torch.optim.Adam(
    ...     [policy], lr=0.1, betas=(0.9, 0.999))
    >>> ai = ActionInference(
    ...     model=model,
    ...     policy=policy,
    ...     optimizer=optimizer,
    ...     inference_cycles=3,
    ...     criterion=ai_loss)

Initialization of context inference works similar.
First, we create an intial context.
Usually, during context inference, also the hidden state furthest in the past is adapted.
The opt accessor function tells the context inference algorithm, which parts of the state should be optimized exactly.
Here, we only use the hidden state ([state[0]]), but we could also optimize the hidden and cell state ([state[0], state[1]]).
After creating the optimizer, we pass everything to the context inference constructor.

.. code-block:: python

    >>> context = torch.zeros([1, 1, context_size])
    >>> def opt_accessor(state):
    ...     return [state[0]]
    >>> params = [{'params': [context], 'lr': 0.1},
    ...           {'params': opt_accessor(lstm_state), 'lr': 0.0001}]
    >>> optimizer = torch.optim.Adam(params)
    >>> ci = ContextInference(
    ...     model=model,
    ...     initial_model_state=lstm_state_ci,
    ...     context=context,
    ...     optimizer=optimizer,
    ...     inference_length=5,
    ...     inference_cycles=5,
    ...     criterion=ci_loss,
    ...     opt_accessor=opt_accessor)

Now we define an initial position, delta, and a tensor representing the randomly chosen target of an agent.
We use gym to create the environment and add our agent.

.. code-block:: python

    >>> position = torch.Tensor([[[0, 1]]])
    >>> targets = torch.cat(
    ...     ai_horizon *
    ...     [torch.Tensor(
    ...          [[np.random.uniform(-1.5, 1.5),
    ...            np.random.uniform(0, 2)]])])
    >>> targets = targets[:, None, :]
    >>> delta = torch.zeros([1, 1, 2])

    >>> env = gym.make('reprise.gym:rocketball-v0')
    >>> env.reset()
    >>> agent = Agent(id='foo', mode=0, init_pos=np.array([0, 1]), color='black')
    >>> agent.update_target(targets[0][0].numpy())
    >>> env.add_agent(agent)

    >>> action = torch.zeros([4])

Now everything is in place and we can actually loop over the environment to control our rocket.

.. code-block:: python

    >>> for t in range(50):
    ...     observation = env.step([action.numpy()])
    ...     position_old = position.clone()
    ...     position = torch.Tensor(observation[0][0][1])
    ...     position = position[None, None, :]
    ...     delta_old = delta.clone()
    ...     delta = position - position_old
    ...
    ...     x_t = torch.zeros([1, 1, input_size])
    ...     x_t[0, 0, :context_size] = context.detach()
    ...     x_t[0, 0, context_size:context_size + action_size] = action
    ...     x_t[0, 0, -observation_size:] = delta_old
    ...
    ...     with torch.no_grad():
    ...         y_t, lstm_state = model.forward(x_t, lstm_state)
    ...     context, _, states = ci.infer_contexts(
    ...         x_t[:, :, context_size:], delta)
    ...     lstm_state = (
    ...         states[-1][0].clone().detach(),
    ...         states[-1][1].clone().detach())
    ...     policy, _, _ = ai.infer_actions(
    ...         delta, lstm_state, context.clone().detach().repeat(
    ...             policy.shape[0], 1, 1), targets - position)
    ...     action = policy[0][0].detach()


To look into the context and policy of the last time step you can do:

.. code-block:: python

    >>> print(context)  # doctest: +ELLIPSIS
    tensor([[[7.8..., 9.1...]]], requires_grad=True)

    >>> print(policy)  # doctest: +ELLIPSIS
    tensor([[[ 6..., -7..., -6...,  7...]],
    ...
    ...     [[ 4..., -7..., -6...,  7...]]], grad_fn=<CloneBackward>)
