# coding=utf8


class Field:
    def __init__(self, name=None, length=None, required=True):
        # length -> digit
        self.name = name
        self.length = length
        if self.name:
            self.fmt = '{' + '0' + ':0' + str(length) + 'd}'
            self.value = None
        else:
            self.fmt = None
            self.value = '0' * length
        self.required = required

    def resolve(self, value=None, short=False):
        if self.name:
            if short and not self.required:
                return ''  # Short Field
            else:
                return self.fmt.format(value)  # Full Field
        else:
            return self.value  # Const

    def __str__(self):
        if self.name:
            return '<Field:{}>'.format(self.name)
        else:
            return '<Const:{}>'.format(self.value)


f_schema = Field(name='schema', length=1)
f_year = Field(name='year', length=4, required=False)
f_month = Field(name='month', length=2)
f_day = Field(name='day', length=2)
f_reverse = Field(name='reverse', length=1)
f_index = Field(name='index', length=2)
f_leap = Field(name='leap', length=1)


class EncoderMixin:
    fields = []

    @classmethod
    def decode(cls, raw, short=False):
        i = 0
        data = {}
        for field in cls.fields:
            if short and not field.required:
                continue
            if field.name:
                data[field.name] = int(raw[i:i + field.length])
            i += field.length
        return cls(**data)

    def encode(self, short=False):
        ds = []
        for field in self.fields:
            if field.name:
                value = getattr(self, field.name)
            else:
                value = None
            ds.append(field.resolve(value, short))
        return ''.join(ds)
