from django.utils.html import format_html

# widgets: 
    # "Media",
    # "MediaDefiningClass",
    # "Widget",
    # "TextInput",
    # "NumberInput",
    # "EmailInput",
    # "URLInput",
    # "PasswordInput",
    # "HiddenInput",
    # "MultipleHiddenInput",
    # "FileInput",
    # "ClearableFileInput",
    # "Textarea",
    # "DateInput",
    # "DateTimeInput",
    # "TimeInput",
    # "CheckboxInput",
    # "Select",
    # "NullBooleanSelect",
    # "SelectMultiple",
    # "RadioSelect",
    # "CheckboxSelectMultiple",
    # "MultiWidget",
    # "SplitDateTimeWidget",
    # "SplitHiddenDateTimeWidget",
    # "SelectDateWidget",

BULMA_COMMON_FIELD_CONTAINER = '''<div class="field">
    <label class="label" for="{field_id}">{label}</label>
    <div class="control">
        {control}
    </div>
    {hint}
</div>'''

BULMA_CHECKBOX_FIELD_CONTAINER = '''<div class="field">
    <div class="control">
        <label class="checkbox">
            {control} {label}
        </label>
    </div>
    {hint}
</div>'''

BULMA_FIELD_HINT = '<p class="help is-info">{text}</p>'

def make_field_id(name):
    return 'id-' + name

def render_attrs(attrs):
    html = ''
    for k,v in attrs.items():
        if v == True:
            html += ' {k}'.format(k=k)
        else:
            html += ' {k}="{v}"'.format(k=k, v=v)
    return html

def bulma_render_form(form):
    hidden_fields = ''
    fields = ''
    for name in form.fields:
        bf = form[name]
        value = bf.value()
        if value is None:
            value = ''
        field = bf.field
        widget_class = type(field.widget).__name__
        if bf.is_hidden:
            control = '<input type="hidden" name="{name}" value="{value}">'
            hidden_fields += control.format(name=name, value=value)
        else:
            control = 'CONTROL'
            field_id = make_field_id(name)
            field_attrs = dict(field.widget.attrs)
            field_attrs['id'] = field_id
            field_attrs['name'] = name
            field_attrs['value'] = value

            v = getattr(field, 'required')
            if v == True:
                field_attrs['required'] = True

            container = BULMA_COMMON_FIELD_CONTAINER
            if widget_class == 'PasswordInput':
                control = '<div class="control"><input class="input" type="password"{field_attrs}></div>'
            elif widget_class == 'TextInput':
                control = '<div class="control"><input class="input" type="text"{field_attrs}></div>'
            elif widget_class == 'Textarea':
                del field_attrs['value']
                control = '<div class="control"><textarea class="textarea"{field_attrs}>{value}</textarea></div>'
            elif widget_class == 'Select':
                control = '<div class="select"><select{field_attrs}>'
                options = ''
                for option_value, option_label in field.choices:
                    options += '<option value="{value}">{label}</option>'.format(value=option_value, label=option_label)
                control += options.replace('{', '{{').replace('}', '}}') + '</select></div>'
            elif widget_class == 'CheckboxInput':
                field_attrs['value'] = 'true'
                container = BULMA_CHECKBOX_FIELD_CONTAINER
                try:
                    del field_attrs['required']
                except KeyError:
                    pass
                if value == True:
                    field_attrs['checked'] = True
                control = '<input type="checkbox"{field_attrs}>'
            else:
                control = 'NOT SUPPORTED WIDGET CLASS {0}'.format(widget_class)

            control = control.format(name=name, field_attrs=render_attrs(field_attrs), value=value).replace('{', '{{').replace('}', '}}')

            hint = ''
            if type(getattr(form, 'hints', None)) is dict and name in form.hints:
                hint = BULMA_FIELD_HINT.format(text=form.hints[name].replace('{', '{{').replace('}', '}}'))

            fields += container.format(label=field.label, control=control, field_id=field_id, hint=hint)
    return format_html(hidden_fields + '\n' + fields)


def bulma_render_form_submit_error(form):
    ''' Process form submit result and return JSON objects with errors and messages.
    '''
    resp = {
        'success': False,
        'errors': []
    }
    for name in form.fields:
        bf = form[name]
        for x in bf.errors:
            resp['errors'].append({
                'field': name,
                'field_id': make_field_id(name),
                'error_text': x
                })
    return resp


def bulma_render_submit_error(message):
    resp = {
        'success': False,
        'errors': [{
            'field': '',
            'field_id': '',
            'error_text': message
        }]
    }
    return resp