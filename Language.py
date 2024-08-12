class Language:
    """Class to handle the text strings in different languages."""

    def __init__(self, language='en'):
        self.language = language
        self.texts = {
            'en': {
                'select_directory': 'Please select a directory to search for PSD files',
                'select_output_directory': 'Please choose an output directory',
                'convert_psd_to_image': 'Convert PSD to Image',
                'conversion_settings': 'Conversion Settings',
                'select_output_format': 'Select the desired output format:',
                'jpeg_quality': 'Specify the quality for JPEG output:',
                'log_errors': 'Log errors to a file',
                'theme_selection': 'Theme Selection',
                'light_theme': 'Light Theme',
                'dark_theme': 'Dark Theme',
                'language_selection': 'Language Selection',
                'conversion_completed': 'Conversion Completed',
                'conversion_successful': 'The conversion was completed successfully!',
                'errors_occurred': 'Some errors occurred during the conversion process'
            },
            'ru': {
                'select_directory': 'Пожалуйста, выберите директорию для поиска файлов PSD',
                'select_output_directory': 'Пожалуйста, выберите директорию для сохранения',
                'convert_psd_to_image': 'Конвертировать PSD в изображение',
                'conversion_settings': 'Настройки конвертации',
                'select_output_format': 'Выберите желаемый формат вывода:',
                'jpeg_quality': 'Укажите качество для вывода в формате JPEG:',
                'log_errors': 'Сохранять ошибки в файл',
                'theme_selection': 'Выбор темы',
                'light_theme': 'Светлая тема',
                'dark_theme': 'Темная тема',
                'language_selection': 'Выбор языка',
                'conversion_completed': 'Конвертация завершена',
                'conversion_successful': 'Конвертация успешно завершена!',
                'errors_occurred': 'Во время конвертации произошли некоторые ошибки'
            },
            'uk': {
                'select_directory': 'Будь ласка, виберіть каталог для пошуку файлів PSD',
                'select_output_directory': 'Будь ласка, оберіть каталог для збереження файлів',
                'convert_psd_to_image': 'Конвертувати PSD у зображення',
                'conversion_settings': 'Налаштування конвертації',
                'select_output_format': 'Оберіть бажаний формат виведення:',
                'jpeg_quality': 'Вкажіть якість для виведення у форматі JPEG:',
                'log_errors': 'Записувати помилки у файл',
                'theme_selection': 'Вибір теми',
                'light_theme': 'Світла тема',
                'dark_theme': 'Темна тема',
                'language_selection': 'Вибір мови',
                'conversion_completed': 'Конвертація завершена',
                'conversion_successful': 'Конвертацію успішно завершено!',
                'errors_occurred': 'Під час конвертації виникли деякі помилки'
            }
        }

    def get_text(self, key):
        return self.texts.get(self.language, {}).get(key, '')

    def set_language(self, language):
        if language in self.texts:
            self.language = language
