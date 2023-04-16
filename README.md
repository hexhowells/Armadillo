<img src="https://github.com/hexhowells/Armadillo/blob/main/logo.png" width=50%>

# Armadillo

Armadillo is a static HTML page generator based from the armadillo syntax.

- ```parser.py``` parses the template file into a syntax tree and symbol table
- ```compiler.py``` complies the syntax tree and data json file and compiles them into a static HTML page

<br>

## Language Definition

All variables are made using the double curly brace notation

> ``` html
> <tag>{{title}}</tag>
> ```

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

The following extensions are currently supported:
- upper
- lower
- quotes
- single-quotes
- escape

---

Blocks of HTML can be repeated using a loop. items from within the block are accessed using the ```.``` operator.

> ```html
> <ul>
> {{#foreach item}}
> <li class={{item.class:quotes}}>{{item.itemname}}</li>
> {{#end}}
> </ul>
> ```

Keywords in Armadillo are indicated by a preceding ```#``` operator

---

**(NOT YET IMPLEMENTED)** HTML can be imported from another file and included in the template 

> ```html
> {{#import header}}
> <p>{{information}}</p>
> {{#import footer}}
> ```

---

<br>

## Example Armadillo file

Below is an example armadillo file demonstrating the main features.
```html
<!doctype html>

<html lang="en">
<head>
  <title>Example Armadillo Page</title>
</head>

<body>
  <h1>{{title}}</h1>

  <h2>List of webpages</h2>
  <ul class="big-list">
    {{#foreach webpages}}
    <li><a href={{webpages.link:quotes}}>{{webpages.title:upper}}</a></li>
    {{#end}}
  </ul>
  <p>Article by {{author:upper}}</p>
</body>
</html>
```

The variables declared in the template can be assigned using a .json data file.
```json
{
  "year": "2023",
  "webpages":
  [
    {
      "link": "https://www.google.com/",
      "title": "Google search engine"
    },
    {
      "link": "https://github.com/",
      "title": "Github webpage"
    },
    {
      "link": "https://news.ycombinator.com/news",
      "title": "Hacker News forum"
    }
  ],
  "author": "HexHowells"
}

```

This produces the following:
```html
<!doctype html>

<html lang="en">
<head>
  <title>Example Armadillo Page</title>
</head>

<body>
  <h1>Web links for 2023</h1>

  <h2>List of Web Links</h2>
  <ul class="big-list">
    <li><a href="https://www.google.com/">GOOGLE SEARCH ENGINE</a></li>
    <li><a href="https://github.com/">GITHUB WEBPAGE</a></li>
    <li><a href="https://news.ycombinator.com/news">HACKER NEWS FORUM</a></li>
  </ul>
  <p>Article by HEXHOWELLS</p>
</body>
</html>
```
