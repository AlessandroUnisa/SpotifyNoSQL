import csv


def remove_columns( input_file, output_file, columns_to_remove ):
    with open(input_file, 'r', newline='') as csvfile_in, \
            open(output_file, 'w', newline='') as csvfile_out:
        reader = csv.reader(csvfile_in)
        writer = csv.writer(csvfile_out)

        # Ottieni gli indici delle colonne da rimuovere
        headers = next(reader)
        column_indices = [i for i, header in enumerate(headers) if header not in columns_to_remove]

        # Scrivi l'intestazione nel file di output
        writer.writerow([headers[i] for i in column_indices])

        # Copia solo le colonne desiderate nel file di output
        for row in reader:
            writer.writerow([row[i] for i in column_indices])

    print(f"Colonne rimosse con successo da {input_file}. Il nuovo file è stato salvato come {output_file}.")


# Esempio di utilizzo
input_file = 'data_by_artist.csv'  # Il nome del file CSV di input
output_file = 'output.csv'  # Il nome del file CSV di output
columns_to_remove = ['type', 'value']  # Le colonne da rimuovere

remove_columns(input_file, output_file, columns_to_remove)
