# Armadillo

Armadillo is a static HTML page generator based from the armadillo syntax.

## Language Definition

---

All variables are made using the double curly brace notation

> ``` html
> <tag>{{title}}</tag>
> ```

Keywords in Armadillo are indicated by a preceding ```#``` operator

---
Variables can be modified using extensions

To turn the text to upper case: 

```html
<tag>{{title:upper}}</tag>
```

To wrap the text in quotes: 

```html
<tag>{{title:quotes}}</tag>
```

To escape the string:

```html
<tag>{{title:escape}}</tag>
```

Extensions can be chained together:

```html
<tag>{{title:upper:quotes}}</tag>
```

---

Blocks of HTML can be repeated using a loop. items from within the block are accessed using the ```.``` operator.

> ```html
> <ul>
> {{#foreach item}}
> <li class={{item-class:quotes}}>{{item.itemname}}</li>
> {{#end}}
> </ul>
> ```

---

HTML can be imported from another file and included in the template

> ```html
> {{#import header}}
> <p>{{information}}</p>
> {{#import footer}}
> ```

---

Required variables can be specified using the ```!``` operator

> ```html
> <tag>{{!title}}</tag>
> ```
