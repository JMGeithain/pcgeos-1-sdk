#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

from pcgeos1 import target

class TargetProfileTests(unittest.TestCase):
    def setUp(self):
        self.payloads={
            'SPINTEXT.GEO':b'spin-template',
            'NOTEPAD.GEO':b'notepad-template',
            'VIEWER.GEO':b'viewer-template',
            'TERM.GEO':b'term-template',
        }
        hashes={k:hashlib.sha256(v).hexdigest() for k,v in self.payloads.items()}
        self.profile={'hashes':hashes,'format_version':1,'kernel_protocol':[622,3],'ui_protocol':[693,0]}
        self.profile_patch=patch.dict(target.PROFILES,{'test-profile':self.profile})
        self.profile_patch.start()
        self.parse_patch=patch.object(target,'parse',side_effect=self.fake_parse)
        self.parse_patch.start()
        self.tmp=tempfile.TemporaryDirectory()
        self.archive=Path(self.tmp.name)/'target.zip'

    def tearDown(self):
        self.parse_patch.stop()
        self.profile_patch.stop()
        self.tmp.cleanup()

    @staticmethod
    def fake_parse(data,label):
        return {'format_version':1,'kernel_protocol':[622,3],'imports':[{'name':'ui','protocol':[693,0]}]}

    def write_archive(self, omit=None, duplicate=None, overrides=None):
        omit=set(omit or [])
        overrides=overrides or {}
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',UserWarning)
            with zipfile.ZipFile(self.archive,'w') as z:
                for name,data in self.payloads.items():
                    if name not in omit:
                        path=target.PATHS[name].lstrip('/')
                        z.writestr('GEOWORKS/'+path,overrides.get(name,data))
                if duplicate:
                    name=duplicate
                    path=target.PATHS[name].lstrip('/')
                    z.writestr('DUPLICATE/'+path,self.payloads[name])
        return self.archive

    def test_valid_named_profile(self):
        self.write_archive()
        result=target.load_templates(self.archive,profile='test-profile')
        self.assertEqual(set(result),set(self.payloads))

    def test_wrong_hash_is_rejected(self):
        self.write_archive(overrides={'SPINTEXT.GEO':b'wrong'})
        with self.assertRaisesRegex(ValueError,'Unsupported SPINTEXT.GEO'):
            target.load_templates(self.archive,profile='test-profile')

    def test_missing_member_is_rejected(self):
        self.write_archive(omit={'TERM.GEO'})
        with self.assertRaisesRegex(ValueError,'Expected exactly one archive member'):
            target.load_templates(self.archive,profile='test-profile')

    def test_duplicate_member_is_rejected(self):
        self.write_archive(duplicate='VIEWER.GEO')
        with self.assertRaisesRegex(ValueError,'Expected exactly one archive member'):
            target.load_templates(self.archive,profile='test-profile')

    def test_unknown_profile_is_rejected(self):
        self.write_archive()
        with self.assertRaisesRegex(ValueError,'Unknown target profile'):
            target.load_templates(self.archive,profile='not-registered')

    def test_wrong_kernel_protocol_is_rejected(self):
        self.write_archive()
        with patch.object(target,'parse',return_value={'format_version':1,'kernel_protocol':[622,2]}):
            with self.assertRaisesRegex(ValueError,'kernel protocol'):
                target.load_templates(self.archive,profile='test-profile')

    def test_wrong_ui_protocol_is_rejected(self):
        self.write_archive()
        with patch.object(target,'parse',return_value={'format_version':1,'kernel_protocol':[622,3],'imports':[{'name':'ui','protocol':[692,0]}]}):
            with self.assertRaisesRegex(ValueError,'UI import protocol'):
                target.load_templates(self.archive,profile='test-profile')

    def test_default_profile_keeps_original_hashes(self):
        self.assertEqual(target.PROFILES['geoworks-pro-1.2']['hashes'],target.KNOWN)

if __name__=='__main__':
    unittest.main()
