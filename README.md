===============================
Django Better Templates
===============================

Features
========

Adds an ``{% includeblock <template_name> ... %}`` template tag. 

The includeblock tag works identically to the ``{% include <template_name ... %}`` template tag built into Django, except that it allows for the definition of blocks *inside* the includeblock tag, which can be referenced in the included template.

This allows for a flatter template design, keeping purely layout-related HTML scruff seperate from template logic and shrinking template file sizes.

The includeblock templatetag re-uses django template rendering code and should be thread-safe, although thread safety has not been fully tested yet.

Compatible with: Django >= 1.5 (up to Django 1.8)


Installation
============

Install this django app (no pypi yet, sorry) and add the app to your installed_apps:

```

INSTALLED_APPS = (
    ...
    'bettertemplates',
    ...
)
```



Example
=======

### Main Template 

```
{% includeblock 'example/includable_template.html' with myvar='Inline context variables' %}

    {% block myblock %}
        <div style="border: 1px solid orange; padding: 10px;"> 
           <p>This inner block is rendered in a template variable in the included template.</p>
           <p>(The variable must have the same name as the block.)</p>
           {% with inner_var='django filters' %}
               <p>It is identical with regular django templates and supports everything like <b>{% trans "Template Tags" %}</b> and <b>{{ inner_var|upper }}</b>.</p>
           {% endwith %}
           <p>Note also how <u>{{ myvar }}</u> are supported.
        </div>
    {% endblock myblock %}
    
    {% block mysecondblock %}
        <div style="border: 1px solid green; padding: 10px;"> 
           A second Block.
        </div>
    {% endblock mysecondblock %}
    
    {% block anotherblock %}
        This content is never rendered because the inner block is not referenced in the included template!
    {% endblock %}
    
    <b>This content is never rendered because it appears outside inner blocks!</b>
        
{% endincludeblock %}
```


### Included Template

```
<div style="border: 1px solid blue; padding: 10px;">
    <table width="99%">
        <tr>
            <td width="33%">
                {{ myblock }}
            </td>
            <td width="33%">
                {{ mysecondblock }}
            </td>
            <td width="33%">
                {{ mysecondblock }}
            </td>
        </tr>
    </table>
</div>
```

### Rendered HTML
    
<div style="border: 1px solid blue; padding: 10px;">
    <table width="99%">
        <tr>
            <td width="33%">
                
            <div style="border: 1px solid orange; padding: 10px;"> 
               <p>This inner block is rendered in a template variable in the included template.</p>
               <p>(The variable must have the same name as the block.)</p>
               
                   <p>It is identical with regular django templates and supports everything like <b>Template Tags</b> and <b>DJANGO FILTERS</b>.</p>
               
               <p>Note also how <u>Inline context variables</u> are supported.
            </div>
        
            </td>
            <td width="33%">
                
            <div style="border: 1px solid green; padding: 10px;"> 
               A second Block.
            </div>
        
            </td>
            <td width="33%">
                
            <div style="border: 1px solid green; padding: 10px;"> 
               A second Block.
            </div>
        
            </td>
        </tr>
    </table>
</div>
