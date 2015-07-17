import pandas

class SignalData(object):
  def __init__(self, signal, filename=None):
    self.signal = signal
    self.filename = filename
  
  @classmethod
  def from_csv(self, *args, **kwargs):
    if len(args):
      filename = args[0]
    elif len(kwargs):
      filename = kwargs['path']
    else:
      raise IOError('Please provide a file path')
    signal = pandas.DataFrame.from_csv(*args, **kwargs)
    return SignalData(signal, filename)
