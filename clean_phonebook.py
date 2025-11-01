from pprint import pprint
import re
import csv

# Читаем адресную книгу
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

print("=== ИСХОДНЫЕ ДАННЫЕ ===")
pprint(contacts_list)

# Функция для форматирования телефона
def format_phone(phone):
    if not phone:
        return ''
    
    # Ищем цифры телефона
    phone_digits = re.sub(r'[^\d]', '', phone)
    
    # Если номер начинается с 8, меняем на +7
    if phone_digits.startswith('8') or phone_digits.startswith('7'):
        if phone_digits.startswith('8'):
            phone_digits = '7' + phone_digits[1:]
        
        # Форматируем основной номер
        if len(phone_digits) == 11:
            main_number = f"+7({phone_digits[1:4]}){phone_digits[4:7]}-{phone_digits[7:9]}-{phone_digits[9:11]}"
            
            # Ищем добавочный номер
            extension_match = re.search(r'доб\.?\s*(\d+)', phone)
            if extension_match:
                extension = extension_match.group(1)
                return f"{main_number} доб.{extension}"
            else:
                return main_number
    
    return phone

# ОБРАБОТКА ДАННЫХ
# 1. Приводим в порядок ФИО
print("\n=== ОБРАБАТЫВАЕМ ФИО ===")
for contact in contacts_list[1:]:  # пропускаем заголовок
    # Объединяем ФИО в одну строку и разбиваем заново
    full_name = ' '.join(contact[:3])
    name_parts = full_name.split()
    
    # Распределяем по полям
    if len(name_parts) >= 1:
        contact[0] = name_parts[0]  # фамилия
    if len(name_parts) >= 2:
        contact[1] = name_parts[1]  # имя
    if len(name_parts) >= 3:
        contact[2] = name_parts[2]  # отчество

# 2. Форматируем телефоны
print("\n=== ФОРМАТИРУЕМ ТЕЛЕФОНЫ ===")
for contact in contacts_list:
    if len(contact) > 5:  # проверяем, что есть поле с телефоном
        contact[5] = format_phone(contact[5])

# 3. Объединяем дубликаты
print("\n=== ОБЪЕДИНЯЕМ ДУБЛИКАТЫ ===")
unique_contacts = {}
headers = contacts_list[0]

for contact in contacts_list[1:]:
    key = (contact[0], contact[1])  # ключ - фамилия + имя
    
    if key in unique_contacts:
        # Объединяем данные
        existing = unique_contacts[key]
        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]
    else:
        unique_contacts[key] = contact

# Создаем итоговый список
final_contacts = [headers] + list(unique_contacts.values())

print("\n=== РЕЗУЛЬТАТ ===")
pprint(final_contacts)

# Сохраняем в файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(final_contacts)

print(f"\n✅ Готово! Обработано {len(final_contacts)-1} контактов")
print("📁 Результат сохранен в 'phonebook.csv'")
