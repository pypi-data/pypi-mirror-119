

from collections.abc import Mapping
from .arguments import Argument
from redengine.core.utils import is_pickleable
from redengine.pybox.io import read_yaml

class Parameters(Mapping): # Mapping so that mytask(**Parameters(...)) would work

    """Parameter set for tasks.

    Parameter set is a mapping (similar as dictionary).
    The parameter set materializes the arguments so that
    those can be inputted to the tasks.
    """
    #! TODO: Do we need extra class for Parameters?

    _params: dict

    def __init__(self, _param:dict=None, type_=None, **params):
        if _param is not None:
            # We get original values if _param has Private or other arguments that are 
            # hidden
            _param = _param._params if isinstance(_param, Parameters) else _param
            params.update(_param)

        if type_ is not None:
            params = {
                name: type_(value) 
                for name, value in params.items()
            }
        self._params = params
    
# For mapping interface
    def get(self, item, default=None):
        try:
            return self[item]
        except KeyError:
            return default

    def __iter__(self):
        return iter(self._params)

    def __len__(self):
        return len(self._params)

    def __getitem__(self, item):
        "Materializes the parameters and hide private"
        value = self._params[item]
        return value if not isinstance(value, Argument) else value.get_repr()

    def materialize(self):
        """Materialize the parameters and include private
        Should only be used when absolute necessary (by 
        the task)
        """
        
        return {
            key: 
                value 
                if not isinstance(value, Argument) 
                else value.get_value()
            for key, value in self._params.items()
        }

    def represent(self):
        """Materialize the parameters but hide private
        """
        return {
            key: 
                value 
                if not isinstance(value, Argument) 
                else value.get_repr()
            for key, value in self._params.items()
        }

    def __setitem__(self, key, item):
        "Set parameter value"
        self._params[key] = item

    def update(self, params):
        params = params._params if isinstance(params, Parameters) else params
        self._params.update(params)

    def __or__(self, other):
        "| operator is union"
        left = self._params
        right = other._params if isinstance(other, Parameters) else other
        
        params = {**left, **right}
        return type(self)(**params)

    def __eq__(self, other):
        "Whether parameters are equal"
        if isinstance(other, Parameters):
            return self._params == other._params
        else:
            return False

    def __ne__(self, other):
        "Whether parameters are equal"
        if isinstance(other, Parameters):
            return self._params != other._params
        else:
            return True

# Pickling
    def __getstate__(self):
        # capture what is normally pickled
        state = self.__dict__.copy()

        # Remove unpicklable parameters
        state["_params"] = {
            key: val
            for key, val in state["_params"].items()
            if is_pickleable(val)
        }
        return state

#    def __setstate__(self, newstate):
#        self.__dict__.update(newstate)

    def items(self):
        return self._params.items()

    def clear(self):
        "Empty the parameters"
        self._params = {}

    def to_dict(self):
        return self._params

    @classmethod
    def from_yaml(cls, path, type_=None):
        return cls(read_yaml(path), type_=type_)