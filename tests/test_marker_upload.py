"""Exercise upload handling without installing ML frameworks or downloading weights."""
import ast
import asyncio
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class HTTPError(Exception):
    def __init__(self,status,detail):self.status_code=status;super().__init__(detail)

class Upload:
    def __init__(self,data,filename='../../outside.pdf'):
        self.data=data;self.filename=filename;self.closed=False
    async def read(self,size):
        result,self.data=self.data[:size],self.data[size:];return result
    async def close(self):self.closed=True

class MarkerUploads(unittest.IsolatedAsyncioTestCase):
    def prepare(self,converter,limit=32*1024*1024):
        tree=ast.parse((ROOT/'templates/marker/main.py').read_text())
        function=next(n for n in tree.body if isinstance(n,ast.AsyncFunctionDef) and n.name=='upload')
        function.decorator_list=[]
        async def run(function,path):return function(path)
        context={'UploadFile':Upload,'File':lambda *args,**kw:None,'busy':asyncio.Lock(),
                 'tempfile':tempfile,'Path':Path,'LIMIT':limit,'HTTPException':HTTPError,
                 'run_in_threadpool':run,'convert':converter}
        exec(compile(ast.Module(body=[function],type_ignores=[]),'marker-upload','exec'),context)
        return context
    async def test_traversal_filename_never_used_and_temp_deleted(self):
        paths=[]
        def convert(path):
            paths.append(path)
            self.assertTrue(Path(path).read_bytes().startswith(b'%PDF-'))
            self.assertNotIn('outside',path)
            return {'markdown':'converted'}
        ctx=self.prepare(convert);file=Upload(b'%PDF-1.7 test')
        self.assertEqual(await ctx['upload'](file),{'markdown':'converted'})
        self.assertTrue(file.closed)
        self.assertFalse(Path(paths[0]).exists())
    async def test_converter_failure_still_deletes_file(self):
        paths=[]
        def convert(path):paths.append(path);raise RuntimeError('conversion failed')
        ctx=self.prepare(convert);file=Upload(b'%PDF-1.7 test')
        with self.assertRaises(RuntimeError):await ctx['upload'](file)
        self.assertTrue(file.closed)
        self.assertFalse(Path(paths[0]).exists())
    async def test_oversized_and_non_pdf_never_reach_converter(self):
        def fail(path):self.fail('converter must not run')
        for content,status in [(b'plain text',415),(b'%PDF-'+b'x'*100,413)]:
            ctx=self.prepare(fail,limit=20);file=Upload(content)
            with self.assertRaises(HTTPError) as caught:await ctx['upload'](file)
            self.assertEqual(caught.exception.status_code,status)
            self.assertTrue(file.closed)
    async def test_second_job_is_rejected(self):
        ctx=self.prepare(lambda path:None)
        async with ctx['busy']:
            with self.assertRaises(HTTPError) as caught:await ctx['upload'](Upload(b'%PDF-1.7'))
            self.assertEqual(caught.exception.status_code,429)
if __name__=='__main__':unittest.main()
