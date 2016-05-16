# coding: utf-8
from pyquery import PyQuery as q
from collections import OrderedDict
from tools import *
import logging


logging.basicConfig(format='%(levelname)s %(type)s %(href)s\n  %(message)s')
log = logging.LoggerAdapter(logging.getLogger(), {'type': '', 'href': ''})

PROPERTIES_REFERENCE = BASE + 'aws-product-property-reference.html'


def property_name_from_href(href):
    href = str(href)
    href, _ = href.rsplit(".", 1)
    _, href = href.rsplit("/", 1)
    return href


def property_ref_from_href(href):
    return {
        '$ref':
        '#/definitions/property_types/%s' % property_name_from_href(href)
    }


def get_type(dd_):
    dd = dd_('p').filter(lambda x: q(this).text().startswith('Type'))
    t = dd.text().lower()
    if 'type : string' in t:
        return {'type': 'string'}
    if 'list of strings' in t:
        return {'type': 'array', 'items': {'type': 'string'}}
    if 'type : integer' in t:
        return {'type': 'integer'}
    if 'type : boolean' in t:
        return {'type': 'boolean'}
    if 'list of key-value pairs' in t:
        return OrderedDict((
            ('type', 'array'),
            ('items', OrderedDict((
                ('type', 'array'),
                ('items', [
                    {
                        "type": "string"
                    },
                    {
                        "type": "string"
                    },
                ])
            ))),
        ))
    if dd('a'):
        return property_ref_from_href(dd('a').attr('href'))
    if dd_('.type') and len(dd_('.type')):
        if (dd_('.type').text() == 'AWS::EC2::SecurityGroup' and
                'list of' in t):
            return {'type': 'array', 'items': {'type': 'string'}}

    log.warning('Could not parse resource property type: "%s"', dd_.html())
    return {}

all_properties = all_resource_properties_hrefs()


def set_resource_properties(schema, res_type):
    log.extra['type'] = res_type
    all_ = all_resource_hrefs()
    type_href = all_[res_type]
    log.extra['href'] = type_href
    h = get_pq(type_href)
    dl = h('#main-col-body .variablelist dl').eq(0)
    resources = resources_dict(schema)
    pairs = zip(dl('dt'), dl('dd'))
    pairs = [(q(dt), q(dd)) for dt, dd in pairs]
    shortcut = resources[res_type]['properties']
    shortcut['Properties'] = OrderedDict()
    shortcut['Properties']['properties'] = OrderedDict(
        (dt.text(), get_type(dd))
        for dt, dd in pairs
    )
    required = [
        k.text()
        for k, v
        in pairs
        if v('p').filter(lambda i: 'Required : Yes' in q(this).text())
    ]
    if required:
        shortcut['Properties']['required'] = required
        resources[res_type]['required'] = ['Properties']
    return schema


def all_res_properties():
    h = get_pq(PROPERTIES_REFERENCE)
    res = OrderedDict(
        (
            property_name_from_href(q(a).attr("href")),
            {
                "title": " ".join(a.text.split()),
                "description": q(a).attr("href")
            }
        ) for a in h('#main-col-body li a'))
    return res
