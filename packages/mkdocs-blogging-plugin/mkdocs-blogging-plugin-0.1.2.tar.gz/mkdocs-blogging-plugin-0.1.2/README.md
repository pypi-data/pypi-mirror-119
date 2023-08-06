# mkdocs-blogging-plugin

A mkdocs plugin that generates a blog page listing selected pages by time.

![preview](https://i.loli.net/2021/09/08/AiawUNjfgbFRuJx.png)

## Installation

```shell
pip3 install mkdocs-blogging-plugin
```

## Prerequisites

- Only `material` theme is adapted by far.

- `navigation.instant` feature cannot be enabled if blog paging is on.

## Usage

Add `blogging` in `plugins` and specify the directories to be included:

```yml
plugins:
  - blogging:
      dirs: # The directories to be included
        - blog
```

In the page you want to insert the blog content, just add a line `{{ blog_content }}` into your desired position:

```markdown
# Blogs

{{ blog_content }}
```

In articles, add meta tags providing article title and description, which will appear on the post list:

```markdown
---
title: Lorem ipsum dolor sit amet
description: Nullam urna elit, malesuada eget finibus ut, ac tortor.
---
```

To exclude certain pages from the blog collection, add a meta tag `exculde_from_blog` in the meta section in the markdown file:

```markdown
---
exculde_from_blog: true
---
```

And it's done! You can open the page where you insert `{{ blog_content }}` and see how it is working.

### Customization

Optionally, you can customize some behaviours of the plugin:

```yml
size: 5            # Number of articles in one page, default: 10
locale: en         # The locale for time localizations, default: system's locale
sort: 
  from: new        # Sort from new to old, default
  # or old         # Sort from old to new
  by: creation     # Sort by the first commit time, default
  # or revision    # Sort by the latest commit time
paging: false	   # Disable paging
show_total: false  # Remove 'total pages' label
```
