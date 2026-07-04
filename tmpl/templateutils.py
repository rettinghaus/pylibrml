import logging
import pathlib

from model.librml import LibRML

logger = logging.getLogger(__name__)


def from_template(templateid: str, itemid: str, tenant: str | None = None, **kwargs) -> LibRML:
    from tmpl.TemplateManager import TemplateManager
    from jinja2 import Template

    tm = TemplateManager()
    t_meta = tm.getTemplateMeta(templateid)
    if t_meta:
        t_path = pathlib.Path('sample-templates') / (templateid + '.jinja')
        with open(t_path, 'r') as f:
            t_content = f.read()

        template = Template(t_content)
        rendered = template.render(**kwargs)
        librml = LibRML.from_jsonstr(rendered)
        librml.id = itemid
        if tenant:
            librml.tenant = tenant
        return librml
    else:
        raise ValueError(f"Template {templateid} not found")
