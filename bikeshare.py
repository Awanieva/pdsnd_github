# Importing Neccessary Libraries
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Function to filter data
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
     # Define valid cities
    valid_cities = ['chicago', 'new york city', 'washington']

    while True:
        # Get user input for city
        city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()

        # Check if the input is a valid city
        if city in valid_cities:
            break  # Exit the loop if the input is valid
        else:
            print('Invalid input. Please choose a valid city.')


    # Get user input for month
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        month = input('Which month would you like to filter by (all, january, february, march, april, may, june)? ').lower()

        if month in valid_months:
            break
        else:
            print('Invalid input. Please choose a valid month.')

    # Get user input for day of the week
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        day = input('Which day of the week would you like to filter by (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)? ').lower()

        if day in valid_days:
            break
        else:
            print('Invalid input. Please choose a valid day.')

    print('-' * 40)
    return city, month, day


# Loading the Month and Day
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load the data from the CSV file based on the selected city
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' for filtering
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Apply filters for the specified month and day
    if month != 'all':
        # Convert the input month to its corresponding integer value
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1  # +1 to match the month values in the DataFrame
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df



# Function to display time statistics
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Check if the DataFrame is empty
    if df.empty:
        print("No data available for the selected filters.")
    else:
        # Display the most common month
        common_month = df['month'].value_counts().idxmax()
        print(f"The most common month for travel is: {common_month}")

        # Display the most common day of the week
        common_day = df['day_of_week'].value_counts().idxmax()
        print(f"The most common day of the week for travel is: {common_day}")

        # Extract and display the most common start hour
        df['Hour'] = df['Start Time'].dt.hour
        common_hour = df['Hour'].value_counts().idxmax()
        print(f"The most common start hour for travel is: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# Function to display station statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    # Check if the 'Start Station' column exists in the DataFrame
    if 'Start Station' not in df:
        print("The 'Start Station' column does not exist in the DataFrame.")
        return

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode().iloc[0]  # Use iloc[0] to access the first value
    print(f"The most commonly used start station is: {common_start_station}")

    # Check if the 'End Station' column exists in the DataFrame
    if 'End Station' not in df:
        print("The 'End Station' column does not exist in the DataFrame.")
        return

    # Display most commonly used end station
    common_end_station = df['End Station'].mode().iloc[0]  # Use iloc[0] to access the first value
    print(f"The most commonly used end station is: {common_end_station}")

    # Calculate and display the most frequent combination of start station and end station trip
    if 'Start Station' in df and 'End Station' in df:
        df['Combined Stations'] = df['Start Station'] + ' to ' + df['End Station']
        common_trip = df['Combined Stations'].mode().iloc[0]  # Use iloc[0] to access the first value
        print(f"The most frequent combination of start and end station is: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



# Function to display trip duration statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is: {total_travel_time} seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# Function to display user statistics
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    # Check if the 'User Type' column exists in the DataFrame
    if 'User Type' not in df:
        print("The 'User Type' column does not exist in the DataFrame.")
        return

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:\n", user_types)

    # Check if the 'Gender' column exists in the DataFrame
    if 'Gender' in df:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:\n", gender_counts)
    else:
        print("\nGender information is not available in this dataset.")

    # Check if the 'Birth Year' column exists in the DataFrame
    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode().iloc[0])  # Use iloc[0] to access the first value

        print("\nEarliest Birth Year:", earliest_birth_year)
        print("Most Recent Birth Year:", most_recent_birth_year)
        print("Most Common Birth Year:", common_birth_year)
    else:
        print("\nBirth year information is not available in this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# Function to display raw data
def display_raw_data(df):
    start_index = 0
    while True:
        # Prompt the user if they want to see 5 lines of raw data
        raw_data_request = input('Would you like to see 5 lines of raw data? Enter yes or no: ')
        if raw_data_request.lower() == 'yes':
            end_index = start_index + 5
            if end_index >= len(df):
                print("No more raw data to display.")
                break
            # Display 5 lines of raw data
            print(df.iloc[start_index:end_index])
            start_index = end_index
        elif raw_data_request.lower() == 'no':
            break
        else:
            print("Invalid Input. Please choose a valid answer (Yes or No).")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart the Program? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
