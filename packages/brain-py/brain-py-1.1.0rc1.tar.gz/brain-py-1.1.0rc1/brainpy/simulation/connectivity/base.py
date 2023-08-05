# -*- coding: utf-8 -*-

import abc
import logging

import numpy as np

from brainpy import errors, math

try:
  import numba as nb
except ModuleNotFoundError:
  nb = None


logger = logging.getLogger('brainpy.simulation.connectivity')


__all__ = [
  'ij2mat',
  'mat2ij',
  'pre2post',
  'post2pre',
  'pre2syn',
  'post2syn',
  'pre_slice',
  'post_slice',

  'Connector',
  'TwoEndConnector',
]


def _numba_backend():
  r = math.get_backend_name().startswith('numpy')
  return r and (nb is not None)


def ij2mat(i, j, num_pre=None, num_post=None):
  """Convert i-j connection to matrix connection.

  Parameters
  ----------
  i : list, np.ndarray
      Pre-synaptic neuron index.
  j : list, np.ndarray
      Post-synaptic neuron index.
  num_pre : int
      The number of the pre-synaptic neurons.
  num_post : int
      The number of the post-synaptic neurons.

  Returns
  -------
  conn_mat : np.ndarray
      A 2D ndarray connectivity matrix.
  """
  if len(i) != len(j):
    raise errors.BrainPyError('"i" and "j" must be the equal length.')
  if num_pre is None:
    logger.warning('"num_pre" is not provided, the result may not be accurate.')
    num_pre = math.max(i)
  if num_post is None:
    logger.warning('"num_post" is not provided, the result may not be accurate.')
    num_post = math.max(j)
  conn_mat = math.zeros((num_pre, num_post))
  conn_mat[i, j] = 1.
  return conn_mat


def mat2ij(conn_mat):
  """Get the i-j connections from connectivity matrix.

  Parameters
  ----------
  conn_mat : np.ndarray
      Connectivity matrix with `(num_pre, num_post)` shape.

  Returns
  -------
  conn_tuple : tuple
      (Pre-synaptic neuron indexes,
       post-synaptic neuron indexes).
  """
  if len(math.shape(conn_mat)) != 2:
    raise errors.BrainPyError('Connectivity matrix must be in the '
                              'shape of (num_pre, num_post).')
  pre_ids, post_ids = math.where(conn_mat > 0)
  return math.array(pre_ids, dtype=math.int_), math.array(post_ids, dtype=math.int_)


def pre2post(i, j, num_pre=None):
  """Get pre2post connections from `i` and `j` indexes.

  Parameters
  ----------
  i : list, np.ndarray
      The pre-synaptic neuron indexes.
  j : list, np.ndarray
      The post-synaptic neuron indexes.
  num_pre : int, None
      The number of the pre-synaptic neurons.

  Returns
  -------
  conn : list
      The conn list of pre2post.
  """
  if len(i) != len(j):
    raise errors.BrainPyError('The length of "i" and "j" must be the same.')
  if num_pre is None:
    logger.warning('"num_pre" is not provided, the result may not be accurate.')
    num_pre = math.max(i)

  pre2post_list = [[] for _ in range(num_pre)]
  for pre_id, post_id in zip(i, j):
    pre2post_list[pre_id].append(post_id)
  pre2post_list = [math.array(l, dtype=math.int_) for l in pre2post_list]

  if _numba_backend():
    pre2post_list_nb = nb.typed.List()
    for pre_id in range(num_pre):
      pre2post_list_nb.append(pre2post_list[pre_id])
    pre2post_list = math.Variable(math.asarray(pre2post_list, dtype=object),
                                  type='connection')
    pre2post_list.value = pre2post_list_nb
  return pre2post_list


def post2pre(i, j, num_post=None):
  """Get post2pre connections from `i` and `j` indexes.

  Parameters
  ----------
  i : list, np.ndarray
      The pre-synaptic neuron indexes.
  j : list, np.ndarray
      The post-synaptic neuron indexes.
  num_post : int, None
      The number of the post-synaptic neurons.

  Returns
  -------
  conn : list
      The conn list of post2pre.
  """

  if len(i) != len(j):
    raise errors.BrainPyError('The length of "i" and "j" must be the same.')
  if num_post is None:
    logger.warning('WARNING: "num_post" is not provided, the result may not be accurate.')
    num_post = math.max(j)

  post2pre_list = [[] for _ in range(num_post)]
  for pre_id, post_id in zip(i, j):
    post2pre_list[post_id].append(pre_id)
  post2pre_list = [math.array(l, dtype=math.int_) for l in post2pre_list]

  if _numba_backend():
    post2pre_list_nb = nb.typed.List()
    for post_id in range(num_post):
      post2pre_list_nb.append(post2pre_list[post_id])
    post2pre_list = math.Variable(math.asarray(post2pre_list, dtype=object),
                                  type='connection')
    post2pre_list.value = post2pre_list_nb
  return post2pre_list


def pre2syn(i, num_pre=None):
  """Get pre2syn connections from `i` and `j` indexes.

  Parameters
  ----------
  i : list, np.ndarray
      The pre-synaptic neuron indexes.
  num_pre : int
      The number of the pre-synaptic neurons.

  Returns
  -------
  conn : list
      The conn list of pre2syn.
  """
  if num_pre is None:
    logger.warning('WARNING: "num_pre" is not provided, the result may not be accurate.')
    num_pre = math.max(i)

  pre2syn_list = [[] for _ in range(num_pre)]
  for syn_id, pre_id in enumerate(i):
    pre2syn_list[pre_id].append(syn_id)
  pre2syn_list = [math.array(l, dtype=math.int_) for l in pre2syn_list]

  if _numba_backend():
    pre2syn_list_nb = nb.typed.List()
    for pre_ids in pre2syn_list:
      pre2syn_list_nb.append(pre_ids)
    pre2syn_list = math.Variable(math.asarray(pre2syn_list, dtype=object),
                                 type='connection')
    pre2syn_list.value = pre2syn_list_nb
  return pre2syn_list


def post2syn(j, num_post=None):
  """Get post2syn connections from `i` and `j` indexes.

  Parameters
  ----------
  j : list, np.ndarray
      The post-synaptic neuron indexes.
  num_post : int
      The number of the post-synaptic neurons.

  Returns
  -------
  conn : list
      The conn list of post2syn.
  """
  if num_post is None:
    logger.warning('WARNING: "num_post" is not provided, the result may not be accurate.')
    num_post = math.max(j)

  post2syn_list = [[] for _ in range(num_post)]
  for syn_id, post_id in enumerate(j):
    post2syn_list[post_id].append(syn_id)
  post2syn_list = [math.array(l, dtype=math.int_) for l in post2syn_list]

  if _numba_backend():
    post2syn_list_nb = nb.typed.List()
    for pre_ids in post2syn_list:
      post2syn_list_nb.append(pre_ids)
    post2syn_list = math.Variable(math.asarray(post2syn_list, dtype=object),
                                  type='connection')
    post2syn_list.value = post2syn_list_nb

  return post2syn_list


def pre_slice(i, j, num_pre=None):
  """Get post slicing connections by pre-synaptic ids.

  Parameters
  ----------
  i : list, np.ndarray
      The pre-synaptic neuron indexes.
  j : list, np.ndarray
      The post-synaptic neuron indexes.
  num_pre : int
      The number of the pre-synaptic neurons.

  Returns
  -------
  conn : list
      The conn list of post2syn.
  """
  # check
  if len(i) != len(j):
    raise errors.BrainPyError('The length of "i" and "j" must be the same.')
  if num_pre is None:
    logger.warning('WARNING: "num_pre" is not provided, the result may not be accurate.')
    num_pre = math.max(i)

  # pre2post connection
  pre2post_list = [[] for _ in range(num_pre)]
  for pre_id, post_id in zip(i, j):
    pre2post_list[pre_id].append(post_id)
  pre_ids, post_ids = [], []
  for pre_i, posts in enumerate(pre2post_list):
    post_ids.extend(posts)
    pre_ids.extend([pre_i] * len(posts))
  post_ids = math.array(post_ids, dtype=math.int_)
  pre_ids = math.array(pre_ids, dtype=math.int_)

  # pre2post slicing
  slicing = []
  start = 0
  for posts in pre2post_list:
    end = start + len(posts)
    slicing.append([start, end])
    start = end
  slicing = math.array(slicing, dtype=math.int_)

  return pre_ids, post_ids, slicing


def post_slice(i, j, num_post=None):
  """Get pre slicing connections by post-synaptic ids.

  Parameters
  ----------
  i : list, np.ndarray
      The pre-synaptic neuron indexes.
  j : list, np.ndarray
      The post-synaptic neuron indexes.
  num_post : int
      The number of the post-synaptic neurons.

  Returns
  -------
  conn : list
      The conn list of post2syn.
  """
  if len(i) != len(j):
    raise errors.BrainPyError('The length of "i" and "j" must be the same.')
  if num_post is None:
    logger.warning('WARNING: "num_post" is not provided, the result may not be accurate.')
    num_post = math.max(j)

  # post2pre connection
  post2pre_list = [[] for _ in range(num_post)]
  for pre_id, post_id in zip(i, j):
    post2pre_list[post_id].append(pre_id)
  pre_ids, post_ids = [], []
  for _post_id, _pre_ids in enumerate(post2pre_list):
    pre_ids.extend(_pre_ids)
    post_ids.extend([_post_id] * len(_pre_ids))
  post_ids = math.array(post_ids, dtype=math.int_)
  pre_ids = math.array(pre_ids, dtype=math.int_)

  # post2pre slicing
  slicing = []
  start = 0
  for pres in post2pre_list:
    end = start + len(pres)
    slicing.append([start, end])
    start = end
  slicing = math.array(slicing, dtype=math.int_)

  return pre_ids, post_ids, slicing


SUPPORTED_SYN_STRUCTURE = ['pre_ids', 'post_ids', 'conn_mat',
                           'pre2post', 'post2pre',
                           'pre2syn', 'post2syn',
                           'pre_slice', 'post_slice']


class Connector(abc.ABC):
  def __call__(self, *args, **kwargs):
    pass


class TwoEndConnector(Connector):
  """Abstract connector class for two end connections."""

  def __init__(self):
    # total size of the pre/post-synaptic neurons
    # useful for the construction of pre2post/pre2syn/etc.
    self.num_pre = None
    self.num_post = None

    # synaptic structures
    self.pre_ids = None
    self.post_ids = None
    self.conn_mat = None
    self.pre2post = None
    self.post2pre = None
    self.pre2syn = None
    self.post2syn = None
    self.pre_slice = None
    self.post_slice = None

    # synaptic weights
    self.weights = None

  def requires(self, *syn_requires):
    # get synaptic requires
    requires = []
    for n in syn_requires:
      if n in SUPPORTED_SYN_STRUCTURE:
        requires.append(n)
      else:
        raise ValueError(f'Unknown synapse structure {n}. We only support {SUPPORTED_SYN_STRUCTURE}.')

    # synaptic structure to handle
    needs = []
    if 'pre_slice' in requires and 'post_slice' in requires:
      raise errors.BrainPyError('Cannot use "pre_slice" and "post_slice" simultaneously. \n'
                                'We recommend you use "pre_slice + '
                                'post2syn" or "post_slice + pre2syn".')
    elif 'pre_slice' in requires:
      needs.append('pre_slice')
    elif 'post_slice' in requires:
      needs.append('post_slice')
    for n in requires:
      if n in ['pre_slice', 'post_slice', 'pre_ids', 'post_ids']:
        continue
      needs.append(n)

    # make synaptic data structure
    for n in needs:
      getattr(self, f'make_{n}')()

    # returns
    if len(requires) == 1:
      return getattr(self, requires[0])
    else:
      return tuple([getattr(self, r) for r in requires])

  def make_conn_mat(self):
    if self.conn_mat is None:
      self.conn_mat = ij2mat(self.pre_ids, self.post_ids, self.num_pre, self.num_post)

  def make_mat2ij(self):
    if self.pre_ids is None or self.post_ids is None:
      self.pre_ids, self.post_ids = mat2ij(self.conn_mat)

  def make_pre2post(self):
    self.pre2post = pre2post(self.pre_ids, self.post_ids, self.num_pre)

  def make_post2pre(self):
    self.post2pre = post2pre(self.pre_ids, self.post_ids, self.num_post)

  def make_pre2syn(self):
    self.pre2syn = pre2syn(self.pre_ids, self.num_pre)

  def make_post2syn(self):
    self.post2syn = post2syn(self.post_ids, self.num_post)

  def make_pre_slice(self):
    self.pre_ids, self.post_ids, self.pre_slice = \
      pre_slice(self.pre_ids, self.post_ids, self.num_pre)

  def make_post_slice(self):
    self.pre_ids, self.post_ids, self.post_slice = \
      post_slice(self.pre_ids, self.post_ids, self.num_post)

  def __call__(self, pre_size, post_size):
    """Create the concrete connections between two end objects.

    Parameters
    ----------
    pre_size : int, tuple of int, list of int
        The size of the pre-synaptic group.
    post_size : int, tuple of int, list of int
        The size of the post-synaptic group.

    Returns
    -------
    conn : TwoEndConnector
        Return the self.
    """
    pass
