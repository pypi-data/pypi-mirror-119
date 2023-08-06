# Copyright 2018, Qualita Seguranca e Saude Ocupacional. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import os

import esocial

from esocial import xml
from esocial import client
from esocial.utils import pkcs12_data

here = os.path.dirname(os.path.abspath(__file__))
there = os.path.dirname(os.path.abspath(esocial.__file__))

def ws_factory():
    employer_id = {
        'tpInsc': 1,
        'nrInsc': '12345678901234'
    }
    return client.WSClient(
        pfx_file=os.path.join(there, 'certs', 'libesocial-cert-test.pfx'),
        pfx_passw='cert@test',
        employer_id=employer_id,
    )

def test_S2220_xml():
    evt2220 = xml.load_fromfile(os.path.join(here, 'xml', 'S-2220-v{}.xml'.format(esocial.__esocial_version__)))
    xml.XMLValidate(evt2220).validate()


def test_xml_sign():
    evt2220_not_signed = xml.load_fromfile(os.path.join(here, 'xml', 'S-2220-v{}-not_signed.xml'.format(esocial.__esocial_version__)))
    xmlschema = xml.XMLValidate(evt2220_not_signed)
    isvalid = xmlschema.isvalid()
    assert (not isvalid), str(xmlschema.last_error)

    # Test signing
    cert_data = pkcs12_data(
        cert_file=os.path.join(there, 'certs', 'libesocial-cert-test.pfx'),
        password='cert@test'
    )
    evt2220_signed = xml.sign(evt2220_not_signed, cert_data)
    xml.XMLValidate(evt2220_signed).validate()


def test_xml_send_batch():
    evt2220 = xml.load_fromfile(os.path.join(here, 'xml', 'S-2220-v{}-not_signed.xml'.format(esocial.__esocial_version__)))
    employer_id = {
        'tpInsc': 2,
        'nrInsc': '12345678901234'
    }
    ws = client.WSClient(
        pfx_file=os.path.join(there, 'certs', 'libesocial-cert-test.pfx'),
        pfx_passw='cert@test',
        employer_id=employer_id,
    )
    ws.add_event(evt2220)
    batch_to_send = ws._make_send_envelop(1)
    ws.validate_envelop('send', batch_to_send)


def test_xml_retrieve_batch():
    ws = client.WSClient()        
    protocol_number = '1.2.202109.0000000000000000001'
    batch_to_retrieve = ws._make_retrieve_envelop(protocol_number)
    ws.validate_envelop('retrieve', batch_to_retrieve)


def test_xml_employer_events_id():
    ws = ws_factory()
    events_ids = ws._make_employer_events_ids_evelop(params={
        'tpEvt': 'S-2210',
        'perApur': '2021-09'
    })
    ws.validate_envelop('view_employer_event_id', events_ids)


def test_xml_table_events_id():
    ws = ws_factory()
    table_ids = ws._make_table_events_ids_evelop(params={
        'tpEvt': 'S-1005',
        'chEvt': 'tpInsc=1;nrInsc=12345678901234'
    })
    ws.validate_envelop('view_table_event_id', table_ids)


def test_xml_employee_events_id():
    ws = ws_factory()
    employee_ids = ws._make_employee_events_ids_envelop(params={
        'cpfTrab': '12345678901',
        'dtIni': '2021-09-10T17:00:00',
        'dtFim': '2021-09-10T18:00:00'
    })
    ws.validate_envelop('view_employee_event_id', employee_ids)


def test_xml_download_by_id():
    ws = ws_factory()
    down_envelop = ws._make_download_id_envelop(['ID1053893860000002021090810513500001'])
    # xml.dump_tofile(down_envelop, 'download_by_id.xml', xml_declaration=False, pretty_print=True)
    ws.validate_envelop('event_download_id', down_envelop)


def test_xml_download_by_receipt():
    ws = ws_factory()
    down_envelop = ws._make_download_receipt_envelop(['1.2.202109.0000000000000000001'])
    # xml.dump_tofile(down_envelop, 'download_by_id.xml', xml_declaration=False, pretty_print=True)
    ws.validate_envelop('event_download_receipt', down_envelop)
