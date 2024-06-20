import os
import yadisk
from dotenv import load_dotenv
from fastapi import UploadFile
load_dotenv()

class DiskService:
    def __init__(self, token: str = os.getenv('YANDEX_TOKEN')):
        self.y = yadisk.AsyncClient(token=token)
        self.dir_model = 'model'
        self.dir_encoder = 'encoder'
        self.dir_tokenizer = 'tokenizer'
        self.dir_sub_model = 'sub_model'


    async def init_dirs(self):
        if not await self.y.exists(self.dir_model):
            await self.y.mkdir(self.dir_model)
        if not await self.y.exists(self.dir_encoder):
            await self.y.mkdir(self.dir_encoder)
        if not await self.y.exists(self.dir_tokenizer):
            await self.y.mkdir(self.dir_tokenizer)
        if not await self.y.exists(self.dir_sub_model):
            await self.y.mkdir(self.dir_sub_model)

    async def upload(self, file: UploadFile, file_path: str):
        await self.y.upload(file.file, file_path, timeout=100000)

    async def download(self, file_name: str, file_path: str):
        await self.y.download(file_name, file_path)