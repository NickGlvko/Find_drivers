import subprocess


def main():
    output_file = "driverquery_output.txt"
    print("Запуск утилиты driverquery")

    try:
        result = subprocess.run(
            ["driverquery", "/fo", "csv", "/v"],
            capture_output=True,
            check=True
        )

        try:
            output_text = result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            try:
                output_text = result.stdout.decode('cp866')
            except UnicodeDecodeError:
                output_text = result.stdout.decode('cp866', errors='replace')


        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_text)
 

        with open(output_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            print("Файл пуст.")
            return


        headers = lines[0].strip().strip('"').split('","')
        driver_type_index = None
        for i, h in enumerate(headers):
            if "Driver Type" in h or "Тип драйвера" in h:
                driver_type_index = i
                break

        if driver_type_index is None:
            print("Не найдена колонка 'Driver Type")


        print("\nДрайверы с типом 'File System':\n" + "-" * 50)


        found = False
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            fields = line.strip('"').split('","')
            if len(fields) <= driver_type_index:
                continue
            if fields[driver_type_index].strip().lower() == "file system":
                found = True
                module = fields[0] if fields else "???"
                name = fields[1] if len(fields) > 1 else "???"
                print(f"Модуль: {module} | Имя: {name}")

        if not found:
            print("Не найдено драйверов типа 'File System'.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения driverquery: {e}")
        print("stderr:", e.stderr.decode('cp866', errors='replace') if e.stderr else "пусто")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()