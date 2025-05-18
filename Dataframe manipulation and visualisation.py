import matplotlib.pyplot as plt
import pandas as pd
import os

import pandas.errors

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


print('Welcome to The DataFrame Statistician!')
print('Programmed by David Northey')

MAIN_MENU = '''Please choose from the following options:
     1 - Load data from a file
     2 - View data
     3 - Clean data
     4 - analyse data
     5 - Visualise data
     6 - Save data to a file
     7 - Exit'''

CLEANING_DATA = '''cleaning data:
    1 - Drop rows with missing values
    2 - Fill missing values
    3 - Drop duplicate rows
    4 - Drop column
    5 - Rename column
    6 - Finish Cleaning'''


def main():

    print(MAIN_MENU)
    menu_choice = input(">>> ")
    dataframe = None
    set_index = None
    while menu_choice != '7':
        if menu_choice == '1':
            dataframe, set_index = load_data()
        elif menu_choice == '2':
            view_data(dataframe)
        elif menu_choice == '3':
            dataframe = clean_dataframe(dataframe)
        elif menu_choice == '4':
            analyse_data(dataframe)
        elif menu_choice == '5':
            visualise_data(dataframe)
        elif menu_choice == '6':
            save_data(dataframe, set_index)
        else:
            print("Invalid selection!")

        print(MAIN_MENU)
        menu_choice = input(">>> ")

    print("Goodbye")



def load_data():

    file = input("What is the name of your file?: ")

    try:
        df = pd.read_csv(file, na_values=['NULL', "none"])
        print("Data has been loaded successfully.")
        column_list = df.columns.tolist()
        option_string = "\n".join([f'\t{column}' for column in column_list])
        set_index = input(f"Which column do you want to set as index? (leave blank for none): \n {option_string}\n>>> ")

        while set_index != '' and set_index not in column_list:
            print("Invalid option")
            set_index = input(f"Which column do you want to set as index? (leave blank for none): \n {option_string}\n>>> ")

        if set_index != "":
            df = df.set_index(set_index)
            print("Index set to", set_index)

        return df, set_index

    except FileNotFoundError:
        print("File not found.")
        return None, None

    except pandas.errors.EmptyDataError:
        print("Unable to load data.")
        return None, None


def view_data(dataframe):

    if dataframe is None:
        print("No data to display.")
    elif dataframe.empty:
        print("No data to display.")
    else:
        print(dataframe)


def clean_dataframe(dataframe):


    if dataframe is None:
        print("No data loaded.")
    else:
        clean_menu_choice = None
        print("Cleaning...")
        print(dataframe)
        while clean_menu_choice != '6':

            print(CLEANING_DATA)
            clean_menu_choice = input(">>> ")

            if clean_menu_choice == '1':
                dataframe = drop_rows_threshold(dataframe)
            elif clean_menu_choice == '2':
                dataframe = fill_missing_values(dataframe)
            elif clean_menu_choice == '3':
                dataframe = drop_duplicate_rows(dataframe)
            elif clean_menu_choice == '4':
                dataframe = drop_column(dataframe)
            elif clean_menu_choice == '5':
                dataframe = rename_column(dataframe)
            elif clean_menu_choice != '6':
                print("Invalid selection!")

    return dataframe


def drop_rows_threshold(dataframe):


    threshold_value = get_valid_integer("What is your threshold value?: (must be non negative integer): ", "Invalid selection!, please enter a non-negative integer: ")
    dataframe = dataframe.dropna(thresh=threshold_value)
    print(dataframe)
    return dataframe


def fill_missing_values(dataframe):


    replacement_value = get_valid_integer("Enter the replacement value (must be non negative integer): ", "Invalid selection!, please enter a non-negative integer: ")
    dataframe = dataframe.fillna(replacement_value)
    print(dataframe)
    return dataframe


def drop_duplicate_rows(dataframe):


    original_rows = len(dataframe)
    dataframe = dataframe.drop_duplicates()
    dropped_rows = original_rows - len(dataframe)
    print(f"{dropped_rows} rows dropped.")
    print(dataframe)
    return dataframe


def drop_column(dataframe):


    selected_column = display_column_list(dataframe, "Enter the name of the column you would like to drop? (leave blank for none): ")

    if selected_column == '':
        print("No column dropped")
        print(dataframe)
        return dataframe

    dataframe = dataframe.drop(selected_column, axis=1)
    print(f"{selected_column} dropped.")
    print(dataframe)
    return dataframe


def rename_column(dataframe):


    selected_column = display_column_list(dataframe,"Enter the name of the column you would like to drop? (leave blank for none): ")
    column_list = dataframe.columns.tolist()

    new_name = input("Enter the new name of the column: ")

    while new_name in column_list or new_name == '':
        print("Column name must be unique and non_blank")
        new_name = input("Enter the new name of the column: ")

    dataframe.rename(columns={selected_column:new_name}, inplace=True)
    print(f"{selected_column} renamed to {new_name}.")
    print(dataframe)
    return dataframe


def analyse_data(dataframe):


    for column in dataframe.columns:
        column_data = dataframe[column].dropna()
        # print(dataframe)
        print(column)
        print('-' * len(column))
        print("number of values (n): ".rjust(24), len(column_data))
        print(f"minimum:".rjust(23), f" {column_data.min():.2f}")
        print(f"maximum:".rjust(23), f" {column_data.max():.2f}")
        print(f"mean:".rjust(23), f" {column_data.mean():.2f}")
        print(f"median:".rjust(23), f" {column_data.median():.2f}")
        print(f"standard deviation:".rjust(23), f" {column_data.std():.2f}")
        print(f"std. err. of mean:".rjust(23), f" {column_data.sem():.2f}")
        print()

    print(dataframe.corr())
    print()


def visualise_data(dataframe):


    if dataframe is None:
        print("No data to display.")
    elif dataframe.empty:
        print("No data to display.")
    else:
        graph_selection = input("Would you like a bar graph(bar), line graph(line) or boxplot(box)?: ")
        while graph_selection != "bar" and graph_selection != "line" and graph_selection != "box":
            print("Invalid selection, please select either bar, line or box")
            graph_selection = input("Would you like a bar graph(bar), line graph(line) or boxplot(box)?: ")
        subplots = input("Would you like to use subplots?(y/n): ")
        while subplots != 'y' and subplots != 'n':
            print("Invalid selection, please enter either 'y' or 'n'.")
            subplots = input("Would you like to use subplots?(y/n): ")

        title = input("Please enter the title for the plot (leave blank for no title): ")
        x_label = input("Please enter the x-axis label (leave blank for no label): ")
        y_label = input("Please enter the y-axis label (leave blank for no label): ")


        graph_type(graph_selection, subplots, dataframe, title, x_label, y_label)


def get_valid_integer(prompt, error_message):


    valid_input = False
    while not valid_input:
        try:
            result = int(input(prompt))
            if result >= 0:
                valid_input = True
            else:
                print(error_message)
        except ValueError:
            print("Invalid input, please enter a valid integer")
    return result


def display_column_list(dataframe, prompt):


    column_list = dataframe.columns.tolist()
    option_string = "\n".join([f'\t{column}' for column in column_list])

    selected_column = input(f"{prompt}\n {option_string}\n>>> ")

    while selected_column not in column_list and selected_column != '':
        print("Invalid option")
        selected_column = input(f"{prompt}\n {option_string}\n>>> ")

    return selected_column


def graph_type(graph_selection, subplots, dataframe, title, x_label, y_label):


    if graph_selection == "bar":
        if subplots == 'y':
            dataframe.plot.bar(subplots=True, title=title, xlabel=x_label, ylabel=y_label)
        else:
            dataframe.plot.bar(title=title, xlabel=x_label, ylabel=y_label)


    elif graph_selection == "line":
        if subplots == 'y':
            dataframe.plot.line(subplots=True, title=title, xlabel=x_label, ylabel=y_label)
        else:
            dataframe.plot.line(title=title, xlabel=x_label, ylabel=y_label)


    elif graph_selection == "box":
        if subplots == 'y':
            dataframe.plot.box(subplots=True, title=title, xlabel=x_label, ylabel=y_label)
        else:
            dataframe.plot.box(title=title, xlabel=x_label, ylabel=y_label)
    else:
        print("Invalid selection, please type either 'bar', 'line', or 'box'")

    plt.show()


def save_data(dataframe, set_index):


    save = input("Enther the filename, including extension: ")
    try:
        if set_index:
            dataframe.index.name = set_index
            dataframe.to_csv(save, index=set_index)
            print(f"Data saved to {save}")
        else:
            dataframe.to_csv(save, index=False)
            print(f"Data saved to {save}")

    except FileNotFoundError:
        print("Cancelling save operation.")

main()