import asyncio
import datetime
import uuid

from app.db.SpiderDocument import SpiderDocument
from app.db.base.BaseFeat import CRUDBase


class SpiderDocumentCrud(CRUDBase[SpiderDocument]):
    async def save_doc(self, doc: SpiderDocument):
        if doc.id is not None and doc.id != "":
            await self.update(doc)
        else:
            doc.id = uuid.uuid4().hex
            await self.add(doc)

    async def get_doc_by_url(self, article_url: str):
        return await self.get_one(self.select().filter(SpiderDocument.article_url == article_url))

#     按read_count倒序查询，取前100条
    async def get_doc_sort_by_read_count(self, limit=100):
        return await self.list(self.select().order_by(SpiderDocument.read_count.desc()).limit(limit))


    # 按id集合查询文章
    async def get_doc_by_ids(self, ids: [str]):
        return await self.list(self.select().where(SpiderDocument.id.in_(ids)))


#     查询总数量
    async def get_doc_count(self):
        return await self.count(self.select_count())



spiderDocumentCrud = SpiderDocumentCrud(SpiderDocument)

# asyncio.run(spiderDocumentCrud.get_doc_by_ids(["1", "2"]))

#
# asyncio.run(spiderDocumentCrud.save_doc(doc))

