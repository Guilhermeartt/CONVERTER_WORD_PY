def clear_css_script():
  for style_tag in soup.find_all('style'):
    style_tag.extract()
  for script_tag in soup.find_all('script'):
    script_tag.extract()
    return soup