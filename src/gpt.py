import os
from datetime import datetime
from io import BytesIO
import asyncio

from PIL import Image
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import AsyncYCloudML


class Generator:
    def __init__(self):
        self.sys_prompt = ('Напиши конкретно сколько времени потратит очень медленный студент на выполнение этого '
                           'задания в зависимости от его оценок на курсе.'
                           'Если 2 или 3 - увеличивай время в 2 раза, если оно по той тематике. Если 5 - уменьшай. НЕ '
                           'НАДО РАСПИСЫВАТЬ. Только'
                           'время и единица измерения,'
                           'не более. Сначала я покажу оценки студента, а потом задание')
        self.sdk = AsyncYCloudML(
            folder_id=os.getenv("YANDEX_FOLDER_ID"),
            auth=os.getenv("YANDEX_API_KEY"))

    async def load_sdk_image(self):
        model = self.sdk.models.image_generation('yandex-art')
        model.configure(seed=int(round(datetime.now().timestamp())))
        return model

    async def load_sdk_text(self):
        model = self.sdk.models.completions('yandexgpt-lite')
        model.configure(
            temperature=0.001,
            max_tokens=2000,
        )
        return model

    def load_classify(self):
        model = self.sdk.models.text_classifiers("yandexgpt").configure(
            task_description="Выбери тип текста",
            labels=['норм', 'скучно']
        )
        return model

    async def gen_summary(self, user_prompt: str, system_prompt: str = None):
        model = await self.load_sdk_text()
        if not system_prompt:
            system_prompt = self.sys_prompt

        messages = [
            {'role': 'system', 'text': system_prompt},
            {'role': 'user', 'text': user_prompt},
        ]

        operation = await model.run_deferred(messages)
        result = await operation.wait()
        return result.text

    async def gen_image(self, prompt):
        model = await self.load_sdk_image()

        messages = [{"weight": 1, "text": prompt}]
        operation = await model.run_deferred(messages)
        result = await operation.wait()

        image = Image.open(BytesIO(result.image_bytes))
        return image


async def main():
    load_dotenv()

    gen = Generator()
    await gen.load_sdk_text()
    xd = ['hello world на python', 'скачать обновление для доты', 'сделать 1000 приседаний', 'посмотреть двухчасовую '
                                                                                             'лекцию']
    texts = []
    for x in xd:
        text = await gen.gen_summary(x)
        texts.append(text)

    print(texts)

if __name__ == '__main__':
    asyncio.run(main())
