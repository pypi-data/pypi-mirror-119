# -*- coding: utf-8 -*-

import numpy as np

from brainpy import errors, math
from brainpy.simulation.brainobjects.neuron import NeuGroup
from brainpy.simulation.utils import size2len

__all__ = [
  'section_input',
  'constant_input',
  'spike_input',
  'ramp_input',

  'constant_current',
  'spike_current',
  'ramp_current',

  'SpikeTimeInput',
  'PoissonInput',
]


def section_input(values, durations, dt=None, return_length=False):
  """Format an input current with different sections.

  For example:

  If you want to get an input where the size is 0 bwteen 0-100 ms,
  and the size is 1. between 100-200 ms.
  >>> import numpy as np
  >>> section_input(values=[0, 1],
  >>>               durations=[100, 100])

  Parameters
  ----------
  values : list, np.ndarray
      The current values for each period duration.
  durations : list, np.ndarray
      The duration for each period.
  dt : float
      Default is None.
  return_length : bool
      Return the final duration length.

  Returns
  -------
  current_and_duration : tuple
      (The formatted current, total duration)
  """
  assert len(durations) == len(values), f'"values" and "durations" must be the same length, while ' \
                                        f'we got {len(values)} != {len(durations)}.'

  dt = math.get_dt() if dt is None else dt

  # get input current shape, and duration
  I_duration = sum(durations)
  I_shape = ()
  for val in values:
    shape = math.shape(val)
    if len(shape) > len(I_shape):
      I_shape = shape

  # get the current
  start = 0
  I_current = math.zeros((int(np.ceil(I_duration / dt)),) + I_shape, dtype=math.float_)
  for c_size, duration in zip(values, durations):
    length = int(duration / dt)
    I_current[start: start + length] = c_size
    start += length

  if return_length:
    return I_current, I_duration
  else:
    return I_current


def constant_input(I_and_duration, dt=None):
  """Format constant input in durations.

  For example:

  If you want to get an input where the size is 0 bwteen 0-100 ms,
  and the size is 1. between 100-200 ms.
  >>> import numpy as np
  >>> constant_input([(0, 100), (1, 100)])
  >>> constant_input([(np.zeros(100), 100), (np.random.rand(100), 100)])

  Parameters
  ----------
  I_and_duration : list
      This parameter receives the current size and the current
      duration pairs, like `[(Isize1, duration1), (Isize2, duration2)]`.
  dt : float
      Default is None.

  Returns
  -------
  current_and_duration : tuple
      (The formatted current, total duration)
  """
  dt = math.get_dt() if dt is None else dt

  # get input current dimension, shape, and duration
  I_duration = 0.
  I_shape = ()
  for I in I_and_duration:
    I_duration += I[1]
    shape = math.shape(I[0])
    if len(shape) > len(I_shape):
      I_shape = shape

  # get the current
  start = 0
  I_current = math.zeros((int(np.ceil(I_duration / dt)),) + I_shape, dtype=math.float_)
  for c_size, duration in I_and_duration:
    length = int(duration / dt)
    I_current[start: start + length] = c_size
    start += length
  return I_current, I_duration


constant_current = constant_input


def spike_input(points, lengths, sizes, duration, dt=None):
  """Format current input like a series of short-time spikes.

  For example:

  If you want to generate a spike train at 10 ms, 20 ms, 30 ms, 200 ms, 300 ms,
  and each spike lasts 1 ms and the spike current is 0.5, then you can use the
  following funtions:

  >>> spike_input(points=[10, 20, 30, 200, 300],
  >>>             lengths=1.,  # can be a list to specify the spike length at each point
  >>>             sizes=0.5,  # can be a list to specify the current size at each point
  >>>             duration=400.)

  Parameters
  ----------
  points : list, tuple
      The spike time-points. Must be an iterable object.
  lengths : int, float, list, tuple
      The length of each point-current, mimicking the spike durations.
  sizes : int, float, list, tuple
      The current sizes.
  duration : int, float
      The total current duration.
  dt : float
      The default is None.

  Returns
  -------
  current_and_duration : tuple
      (The formatted current, total duration)
  """
  dt = math.get_dt() if dt is None else dt
  assert isinstance(points, (list, tuple))
  if isinstance(lengths, (float, int)):
    lengths = [lengths] * len(points)
  if isinstance(sizes, (float, int)):
    sizes = [sizes] * len(points)

  current = math.zeros(int(np.ceil(duration / dt)), dtype=math.float_)
  for time, dur, size in zip(points, lengths, sizes):
    pp = int(time / dt)
    p_len = int(dur / dt)
    current[pp: pp + p_len] = size
  return current


spike_current = spike_input


def ramp_input(c_start, c_end, duration, t_start=0, t_end=None, dt=None):
  """Get the gradually changed input current.

  Parameters
  ----------
  c_start : float
      The minimum (or maximum) current size.
  c_end : float
      The maximum (or minimum) current size.
  duration : int, float
      The total duration.
  t_start : float
      The ramped current start time-point.
  t_end : float
      The ramped current end time-point. Default is the None.
  dt : float, int, optional
      The numerical precision.

  Returns
  -------
  current_and_duration : tuple
      (The formatted current, total duration)
  """
  dt = math.get_dt() if dt is None else dt
  t_end = duration if t_end is None else t_end

  current = math.zeros(int(np.ceil(duration / dt)), dtype=math.float_)
  p1 = int(np.ceil(t_start / dt))
  p2 = int(np.ceil(t_end / dt))
  current[p1: p2] = math.array(math.linspace(c_start, c_end, p2 - p1), dtype=math.float_)
  return current


ramp_current = ramp_input


class SpikeTimeInput(NeuGroup):
  """The input neuron group characterized by spikes emitting at given times.

  >>> # Get 2 neurons, firing spikes at 10 ms and 20 ms.
  >>> SpikeTimeInput(2, times=[10, 20])
  >>> # or
  >>> # Get 2 neurons, the neuron 0 fires spikes at 10 ms and 20 ms.
  >>> SpikeTimeInput(2, times=[10, 20], indices=[0, 0])
  >>> # or
  >>> # Get 2 neurons, neuron 0 fires at 10 ms and 30 ms, neuron 1 fires at 20 ms.
  >>> SpikeTimeInput(2, times=[10, 20, 30], indices=[0, 1, 0])
  >>> # or
  >>> # Get 2 neurons; at 10 ms, neuron 0 fires; at 20 ms, neuron 0 and 1 fire;
  >>> # at 30 ms, neuron 1 fires.
  >>> SpikeTimeInput(2, times=[10, 20, 20, 30], indices=[0, 0, 1, 1])

  Parameters
  ----------
  size : int, tuple, list
      The neuron group geometry.
  indices : int, list, tuple
      The neuron indices at each time point to emit spikes.
  times : list, np.ndarray
      The time points which generate the spikes.
  monitors : list, tuple
      The targets for monitoring.
  name : str
      The group name.
  """
  def __init__(self, size, times, indices, need_sort=True, **kwargs):
    if len(indices) != len(times):
      raise errors.BrainPyError(f'The length of "indices" and "times" must be the same. '
                                 f'However, we got {len(indices)} != {len(times)}.')

    # data about times and indices
    self.idx = 0
    self.times = math.asarray(times, dtype=math.float_)
    self.indices = np.asarray(indices, dtype=math.int_)
    self.num_times = len(times)
    if need_sort:
      sort_idx = np.argsort(times)
      self.indices = self.indices[sort_idx]
    self.spike = math.zeros(size2len(size), dtype=bool)

    super(SpikeTimeInput, self).__init__(size=size, **kwargs)

  def update(self, _t, _i):
    self.spike[:] = False
    while self.idx < self.num_times and _t >= self.times[self.idx]:
      self.spike[self.indices[self.idx]] = 1.
      self.idx += 1


class PoissonInput(NeuGroup):
  def __init__(self, size, freqs, seed=None, **kwargs):
    super(PoissonInput, self).__init__(size=size, **kwargs)

    self.freqs = freqs
    self.dt = math.get_dt() / 1000.
    self.size = (size,) if isinstance(size, int) else tuple(size)
    self.spike = math.Variable(math.zeros(self.num, dtype=bool))
    self.t_last_spike = math.Variable(math.ones(self.num) * -1e7)
    self.rng = math.random.RandomState(seed=seed)

  def update(self, _t, _i):
    self.spike[:] = self.rng.random(self.num) <= self.freqs * self.dt
    self.t_last_spike[:] = math.where(self.spike, _t, self.t_last_spike)
