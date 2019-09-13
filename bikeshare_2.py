import time
import pandas as pd
import numpy as np

class Error(Exception):
    pass

class InvalidCityError(Error):
    pass

class InvalidMonthError(Error):
    pass

class InvalidDayError(Error):
    pass

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_input():
    while True:
        try:
            city = input("Please input the name of a city! You can choose from Chicago, New York City, or Washington: ").lower()
            if(city not in CITY_DATA.keys()):
                raise InvalidCityError
            month = input("Please input a month to analyze. You can type the name of the month between January and June, or 'all' for all months: ").lower()
            if(month not in months):
                raise InvalidMonthError
            day = input("Please input a day of the week to analyze. You can type the name of the day, or 'all' for all days: ").lower()
            if(day not in days):
                raise InvalidDayError
        except InvalidCityError:
            print("Sorry, that is not a valid city. Please try again!")
        except InvalidMonthError:
            print("Sorry, that is not a valid month. Please try again!")
        except InvalidDayError:
            print("Sorry, that is not a valid day. Please try again!")
        else:
            print("\nYou chose: {}, {}, {}".format(city.title(), month.title(), day.title()))
            break

    print('-'*40)

    return city, month, day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')    
    return get_input()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into df
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time col to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to make new cols
    df['Month'] = df['Start Time'].dt.month
    df['Day_Of_Week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use index of months list to get corresponding int
        month = months.index(month.lower())+1

        # filter by month to create new dataframe
        df = df.loc[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create new dataframe
        df = df.loc[df['Day_Of_Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = start-timer()

    # display the most common month
    print("The most common month is {}".format(months[df['Month'].mode()[0]].title()))

    # display the most common day of week
    print("The most common day of the week is {}".format(df['Day_Of_Week'].mode()[0]))

    # display the most common start hour
    print("The most common start hour is {}".format((df['Start Time'].dt.hour).mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = start-timer()

    # display most commonly used start station
    print("The most common start station is {}".format(df['Start Station'].mode()[0]))


    # display most commonly used end station
    print("The most common end station is {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df2 = pd.DataFrame(df.groupby(['Start Station', 'End Station']).size().nlargest(1).reset_index(name = 'Count'))
    print("The most common combination of start and end stations is {} (start) and {} (end)".format(df2['Start Station'][0], df2['End Station'][0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = start-timer()

    total_trip_sec = int(df['Trip Duration'].sum())
    mean_trip_sec = int(df['Trip Duration'].mean())

    # display total travel time
    print("The total travel time is {} seconds, or {} minutes".format(total_trip_sec, int(total_trip_sec/60)))


    # display mean travel time
    print("The mean travel time is {} seconds, or {} minutes".format(mean_trip_sec, int(mean_trip_sec/60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def start-timer():
    start_time = time.time()
    return start_time


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = start-timer()

    # Display counts of user types
    df_users = df.groupby(['User Type']).size().reset_index(name='Count')
    print("User Type Statistics:")
    print(df_users.to_string(index=False), '\n\n')

    if 'Gender' in df:
        # Display counts of gender
        df_gender = df.groupby(['Gender']).size().reset_index(name='Count')
        print("Gender Statistics:")
        print(df_gender.to_string(index=False), '\n\n')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("Birth Year Statistics:")
        print("The earliest year of birth is {}".format(int(df['Birth Year'].min())))
        print("The most recent year of birth is {}".format(int(df['Birth Year'].max())))
        print("The most common year of birth is {}".format(int(df['Birth Year'].mode()[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you for using this program!")
            break


if __name__ == "__main__":
	main()
