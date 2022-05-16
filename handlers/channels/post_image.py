from aiogram import types, md
from aiogram.dispatcher import FSMContext

from filters import IsPrivate
from integrations.telegraph import FileUploader
from keyboards.inline.channel_keyboards import quit_keyboard
from loader import dp
from states import Post


@dp.message_handler(IsPrivate(), content_types=types.ContentTypes.PHOTO, state=Post.Image)
async def handle_photo_upload(message: types.Message, file_uploader: FileUploader, state: FSMContext):
    # Возвращает ссылку на изображение с хостинга
    photo = message.photo[-1]
    uploaded_photo = await file_uploader.upload_photo(photo)

    await state.update_data(url=uploaded_photo.link)
    await message.answer('✅ Отлично, теперь пришли мне название книги', reply_markup=quit_keyboard)
    await Post.Book.set()



@dp.message_handler(content_types=types.ContentType.ANY, state=Post.Image)
async def get_post_image(message: types.Message, state: FSMContext):
    checkbox = 'https://telegra.ph//file/a9ee572a27b50032a86ae.jpg'  # Скриншот с установленной галочкой
    url = md.hide_link(checkbox)

    if message.content_type == 'document':
        await message.answer(f'Изображение должно быть не в виде документа!\n'
                             f'Убедись что установлена соответствующая галочка {url}', reply_markup=quit_keyboard)
    else:
        await message.answer('Пожалуйста, пришли изображение книги\n'
                             'Изображение должно быть в формате JPEG, JPG или PNG', reply_markup=quit_keyboard)

    await Post.Image.set()
