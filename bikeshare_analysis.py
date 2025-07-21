import time
import pandas as pd
import numpy as np
import calendar

# Global constants for available cities, months, and days
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['all'] + [month.lower() for month in calendar.month_name[1:7]]
DAYS = ['all'] + [day.lower() for day in calendar.day_name]


def get_filters() -> tuple[str, str, str]:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        tuple[str, str, str]: (city, month, day) - chosen city, month, and day
        for analysis.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get city input from user
    while True:
        city = input("Enter city (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        print("Invalid city. Please choose from Chicago, New York City, or Washington.")

    # Get month input from user
    while True:
        month = input("Enter month (January to June) or 'all': ").strip().lower()
        if month in MONTHS:
            break
        print("Invalid month. Please enter a month from January to June, or 'all'.")

    # Get day of week input from user
    while True:
        day = input("Enter day of week (e.g., Monday, Tuesday) or 'all': ").strip().lower()
        if day in DAYS:
            break
        print("Invalid day. Please enter a valid day of the week, or 'all'.")

    print('-' * 50)
    return city, month, day


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): Name of the city to analyze.
        month (str): Name of the month to filter by, or "all" to apply no month filter.
        day (str): Name of the day of week to filter by, or "all" to apply no day filter.

    Returns:
        pd.DataFrame: Pandas DataFrame containing city data filtered by month and day.
    """
    # Load city data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' column to datetime objects
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time'
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour # Extract hour for later use

    # Filter by month if specified
    if month != 'all':
        month_num = MONTHS.index(month)
        df = df[df['month'] == month_num]

    # Filter by day of week if specified
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df: pd.DataFrame):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (pd.DataFrame): The filtered DataFrame.
    """
    print('\n📅 Calculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # Display the most common month
    # Using int() to get a scalar value from mode() output
    popular_month_num = int(df['month'].mode()[0])
    popular_month = calendar.month_name[popular_month_num]
    print(f"  Most Popular Month: {popular_month}")

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0].title()
    print(f"  Most Popular Day of Week: {popular_day}")

    # Display the most common start hour
    popular_hour = int(df['hour'].mode()[0])
    print(f"  Most Popular Start Hour: {popular_hour}:00")

    print(f"\nThis took {(time.time() - start_time):.2f} seconds.")
    print('-' * 50)


def station_stats(df: pd.DataFrame):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df (pd.DataFrame): The filtered DataFrame.
    """
    print('\n🚏 Calculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f"  Most Popular Start Station: {popular_start_station}")

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f"  Most Popular End Station: {popular_end_station}")

    # Display most frequent combination of start and end station trip
    # idxmax() returns the index of the first occurrence of the maximum value
    popular_trip_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"  Most Frequent Trip: {popular_trip_combo[0]} → {popular_trip_combo[1]}")

    print(f"\nThis took {(time.time() - start_time):.2f} seconds.")
    print('-' * 50)


def trip_duration_stats(df: pd.DataFrame):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df (pd.DataFrame): The filtered DataFrame.
    """
    print('\n🛣️ Calculating Trip Duration...')
    start_time = time.time()

    # Display total travel time
    total_duration_seconds = int(df['Trip Duration'].sum())
    total_hours = total_duration_seconds // 3600
    total_minutes = (total_duration_seconds % 3600) // 60
    total_seconds = total_duration_seconds % 60
    print(f"  Total Trip Duration: {total_hours} hours, {total_minutes} minutes, {total_seconds} seconds")

    # Display mean travel time
    average_duration_seconds = int(df['Trip Duration'].mean())
    avg_minutes = average_duration_seconds // 60
    avg_seconds = average_duration_seconds % 60
    print(f"  Average Trip Duration: {avg_minutes} minutes, {avg_seconds} seconds")

    print(f"\nThis took {(time.time() - start_time):.2f} seconds.")
    print('-' * 50)


def user_stats(df: pd.DataFrame):
    """
    Displays statistics on bikeshare users.

    Args:
        df (pd.DataFrame): The filtered DataFrame.
    """
    print('\n👥 Calculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    print("  User Types:")
    user_type_counts = df['User Type'].value_counts()
    for user_type, count in user_type_counts.items():
        print(f"    {user_type}: {count}")

    # Display counts of gender (if available in the DataFrame)
    if 'Gender' in df.columns:
        print("\n  Gender Distribution:")
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            print(f"    {gender}: {count}")
    else:
        print("\n  Gender data not available for this city.")

    # Display earliest, most recent, and most common birth year (if available)
    if 'Birth Year' in df.columns:
        print("\n  Birth Year Statistics:")
        print(f"    Earliest Birth Year: {int(df['Birth Year'].min())}")
        print(f"    Most Recent Birth Year: {int(df['Birth Year'].max())}")
        print(f"    Most Common Birth Year: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\n  Birth Year data not available for this city.")

    print(f"\nThis took {(time.time() - start_time):.2f} seconds.")
    print('-' * 50)

def display_raw_data(df: pd.DataFrame):
    """
    Displays raw data 5 rows at a time upon user request.

    Args:
        df (pd.DataFrame): The filtered DataFrame.
    """
    index = 0
    while True:
        show_data = input("Would you like to see 5 lines of raw data? Enter 'yes' or 'no': ").strip().lower()
        if show_data == 'yes':
            if index < len(df):
                print(df.iloc[index:index+5])
                index += 5
            else:
                print("No more data to display.")
                break
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    """
    Main function to run the bikeshare data analysis.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()