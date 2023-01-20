from ctypes import Structure, Array, c_double, c_char, c_int

# Classes BD

class Ident(Array):
	_length_ = 36
	_type_ = c_char

class Cliente(Structure):
	_fields_ = [
		('nome', Ident),
		('email', Ident),
		('senha', Ident)
	]

	def __repr__(self):
		return f"{self.__class__.__name__}({', '.join(['='.join([key, str(val)]) for key, val in self.as_dict.items()])})"


class Produto(Structure):
	_fields_ = [
		('titulo', Ident),
		('descricao', Ident),
		('quantidade', c_int),
		('preco', c_double)
	]

	def __repr__(self):
		return f"{self.__class__.__name__}({', '.join(['='.join([key, str(val)]) for key, val in self.as_dict.items()])})"

class Pedido(Structure):
	_fields_ =[
		('OID', Ident),
		('quantidade', c_int),
		('custo', c_double),
		('PID', Ident),
		('CID', Ident)
	]

	def __repr__(self):
		return f"{self.__class__.__name__}({', '.join(['='.join([key, str(val)]) for key, val in self.as_dict.items()])})"

class AsDictMixin:
    @property
    def as_dict(self):
        d = {}
        for (key, _) in self._fields_:
            if isinstance(getattr(self, key), AsDictMixin):
                d[key] = getattr(self, key).as_dict
            elif isinstance(getattr(self, key), bytes):
                d[key] = getattr(self, key).decode()
            else:
                d[key] = getattr(self, key)
        return d