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
</div>'''

BULMA_CHECKBOX_FIELD_CONTAINER = '''<div class="field">
    <div class="control">
        <label class="checkbox">
            {control} {label}
        </label>
    </div>
'''

def make_field_id(name):
    return 'id-' + name

def render_attrs(attrs):
    html = ''
    for k,v in attrs.items():
        if v is None:
            html += ' {k}'.format(k=k)
        else:
            html += ' {k}="{v}"'.format(k=k, v=v)
    return html

def bulma_render_form(form):
    hidden_fields = ''
    fields = ''
    for name in form.fields:
        bf = form[name]
        field = bf.field
        widget_class = type(field.widget).__name__
        value = 'xxx'
        if bf.is_hidden:
            control = '<input type="hidden" name="{name}" value="{value}">'
            hidden_fields += control.format(name=name, value=bf.value())
        else:
            print(field.widget.attrs)
            control = 'CONTROL'
            field_id = make_field_id(name)
            field_attrs = dict(field.widget.attrs)
            field_attrs['id'] = field_id

            v = getattr(field, 'required')
            if v == True:
                field_attrs['required'] = None

            container = BULMA_COMMON_FIELD_CONTAINER
            if widget_class == 'PasswordInput':
                control = '<div class="control"><input class="input" type="password" name="{name}"{field_attrs}></div>'
            elif widget_class == 'TextInput':
                control = '<div class="control"><input class="input" type="text" name="{name}"{field_attrs}></div>'
            elif widget_class == 'Textarea':
                control = '<div class="control"><textarea class="textarea" name="{name}"{field_attrs}></textarea></div>'
            elif widget_class == 'CheckboxInput':
                container = BULMA_CHECKBOX_FIELD_CONTAINER
                try:
                    del field_attrs['required']
                except KeyError:
                    pass
                control = '<input type="checkbox" name="{name}"{field_attrs}>'
            else:
                control = 'NOT SUPPORTED WIDGET CLASS {0}'.format(widget_class)

            control = control.format(name=name, field_attrs=render_attrs(field_attrs))

            fields += container.format(label=field.label, control=control, field_id=field_id)
    return format_html(hidden_fields + '\n' + fields)


def bulma_render_form_submit(form):
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

