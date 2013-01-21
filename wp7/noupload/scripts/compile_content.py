import os
from jinja2 import Template, FileSystemLoader, Environment
from scss import Scss

VERSIONS = ('app', 'web')
# VERSIONS = ('web',)
TEMPLATE_DIR = "../content"
DUMP_DIRSTEM = {
    'web' : "../../",
    'app' : "../../../../../WindowsPhone/WindowsPhoneFPIAHGuide/WindowPhoneDevelopmentFPIAH/HTML/",
}
BASE_FILESTEM = "%s/base.tmpl"
ACCENTS = (
    ('mango'  , '#F09609'),
    ('lblue'  , '#1BA1E2'),
    ('red'    , '#E51400'),
    ('purple' , '#A200FF'),
    ('brown'  , '#A05000'),
    ('green'  , '#339933'),
    ('pink'   , '#E671B8'),
    ('olive'  , '#A2C139'),
    ('teal'   , '#00ABA9'),
    ('dpurple', '#D80073'),
    ('blue'   , '#004C9A'),
)
# Number refers to accent colour
PAGE_ORDER = (
    'index',    
    'overview', 
    'mvvm',     
    'tools',    
    'project',  
    'skeleton', 
    'design',   
    'xaml',     
    'csharp',   
    'binding',  
    'linqtosql',
    'lifecycle',
    'end',      
)
ACCENT_INDS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 0)
MAIN_ACCENT_PAGES = (
    'index',
    'glossary',
    'end'
)
MAIN_ACCENT = 0
CSS_DIR = 'styles'
CSS_FILE = 'styles.css'

# Compile HTML

env = Environment(loader = FileSystemLoader(TEMPLATE_DIR))

for fn in os.listdir(TEMPLATE_DIR):
    if not fn.endswith('.tmpl'):
        continue
    if fn[:-5] in MAIN_ACCENT_PAGES:
        accent_name, accent_hex = ACCENTS[MAIN_ACCENT]
    else:
        accent_name, accent_hex = ACCENTS[ACCENT_INDS[PAGE_ORDER.index(fn[:-5])]]
    prev_page = None
    next_page = None
    if fn[:-5] in PAGE_ORDER:
        i = PAGE_ORDER.index(fn[:-5])
        if (i - 1) >= 0:
            prev_page = PAGE_ORDER[i-1]
        if (i + 1) != len(PAGE_ORDER):
            next_page = PAGE_ORDER[i + 1]
    t = env.get_template(fn)
    for version in VERSIONS:
        src = t.render(base_template=BASE_FILESTEM % version, \
            accent_name=accent_name, accent_hex=accent_hex, \
            prev_page=prev_page, next_page=next_page, version=version)
        out_fn = os.path.join(DUMP_DIRSTEM[version], fn[:-5] + '.html')
        out_fh = open(out_fn, 'w')
        out_fh.write(src)
        out_fh.close()
    print fn


# Now compile CSS

for version in VERSIONS:
    css = Scss()
    css_template_dir = os.path.join(TEMPLATE_DIR, CSS_DIR)
    out_str = ''
    for fn in os.listdir(css_template_dir):
        fp = os.path.join(css_template_dir, fn)
        if (not fn.endswith('.css')) and (not fn.endswith('.scss')):
            continue
        fh = open(fp)
        fstr = fh.read()
        fh.close()
        if fn.endswith('.css'):
            out_str = out_str + fstr
        if fn.endswith('.scss'):
            out_str = out_str + css.compile(fstr)
        
    out_fn = os.path.join(DUMP_DIRSTEM[version], CSS_DIR, CSS_FILE)
    print out_fn
    out_fh = open(out_fn, 'w')
    out_fh.write(out_str)
    out_fh.close()
